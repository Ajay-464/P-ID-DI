# analyzer.py
import vertexai
from vertexai.generative_models import GenerativeModel, Part, HarmCategory, HarmBlockThreshold
import json
import re
import os
from preprocessing import preprocess_image 

# --- CONFIGURATION ---
PROJECT_ID = "p-id-digitizer-project"
LOCATION = "us-central1" 
MODEL_ID = "gemini-2.5-pro"

def extract_json_from_response(text):
    """Finds and parses the first valid JSON block from a string."""
    json_match = re.search(r'```json\s*(\{.*?\})\s*```|(\{.*?\})', text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1) if json_match.group(1) else json_match.group(2)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    return None

def analyze_pid(image_file_path):
    """
    Analyzes a P&ID using the optimized master prompt for high recall and precision.
    """
    print("🧠 Starting analysis pipeline...")
    processed_image_path = preprocess_image(image_file_path)

    vertexai.init(project=PROJECT_ID, location=LOCATION)
    model = GenerativeModel(MODEL_ID)

    # --- OPTIMIZED MASTER PROMPT (for High Recall and Precision) ---
    prompt = """
    Your SOLE task is to generate a single, valid JSON object based on the provided P&ID image. 
    Do not provide any commentary, introduction, or text outside of the JSON structure.

    You are an expert AI process engineer. Analyze this P&ID drawing thoroughly, extracting ALL relevant components and their details.

    **CRITICAL INSTRUCTIONS:**
    1.  **Comprehensive Detection:** Identify EVERY visible component. Prioritize high recall (finding everything) while maintaining precision.
    2.  **JSON Format ONLY:** Your entire response must be a single, valid JSON object.
    3.  **Bounding Box Precision:** For *every* detected item, provide a `bounding_box` as `[x1, y1, x2, y2]` (integers only). Coordinates are normalized 0-1000 for width and height. The box MUST be TIGHTLY fitted to the detected symbol or text. Minimize overlap with unrelated symbols.
    4.  **Labeling:** Every detected object MUST have a `label`. Use `tag` > `line_number_tag` > `junction_id` > `text` > `type` > `category_name` as priority. Never leave `label` empty or use generic terms like "Unknown".
    5.  **Null for Missing:** Use `null` for any field where information is not found. Do not use empty strings.

    **Extraction Categories:**

    **1. metadata (object):**
    * `drawing_title`: String or null.
    * `drawing_number`: String or null.
    * `revision`: String or null.
    * `standards_referenced`: Array of strings (e.g., ["ISA-5.1", "ISO 10628"]) or empty array.

    **2. legends_and_notes (array of objects):**
    * `title`: String (e.g., "UTILITY CONNECTIONS").
    * `items`: Array of objects, each with `key` and `value` (strings).
    * `bounding_box`: [x1, y1, x2, y2].

    **3. equipment (array of objects):**
    * `tag`: String (e.g., "P-101", "V-201").
    * `type`: String (e.g., "Centrifugal Pump", "Vertical Vessel", "Heat Exchanger").
    * `description`: String or null.
    * `bounding_box`: [x1, y1, x2, y2].
    * `category_name`: "equipment".
    * `label`: String.

    **4. instrumentation (array of objects):**
    * `tag`: String (e.g., "FI-120", "PT-101").
    * `type`: String (e.g., "Flow Indicator", "Pressure Transmitter").
    * `measured_variable`: String (e.g., "Flow", "Pressure").
    * `loop_id`: String (e.g., "120", "101").
    * `connected_to_tag`: String (tag of connected equipment/line) or null.
    * `bounding_box`: [x1, y1, x2, y2].
    * `category_name`: "instrumentation".
    * `label`: String.

    **5. valves (array of objects):**
    * `tag`: String or null (e.g., "FV-105", "XV-201").
    * `type`: String (e.g., "Gate Valve", "Control Valve", "Check Valve", "Globe Valve", "Relief Valve").
    * `installed_on_line_tag`: String (line number tag) or null.
    * `fail_position`: String ("FO", "FC", "FL", "Unknown") or null.
    * `bounding_box`: [x1, y1, x2, y2].
    * `category_name`: "valves".
    * `label`: String.

    **6. lines (array of objects):**
    * `line_number_tag`: String (e.g., "LINE-123-A-6").
    * `source_tag`: String (tag of originating component).
    * `destination_tag`: String (tag of terminating component).
    * `line_type`: String ("process", "instrument_signal", "electrical_signal", "utility", "pneumatic", "hydraulic", "vent", "drain", "jacketed", "unknown").
    * `routing`: Array of [x, y] coordinate pairs or null (simplified to bounding_box if polyline too complex).
    * `bounding_box`: [x1, y1, x2, y2] (overall bounding box for the line segment).
    * `category_name`: "lines".
    * `label`: String.

    **7. junctions (array of objects):**
    * `junction_id`: String (unique ID for the junction, e.g., "JUNC-001").
    * `connected_lines`: Array of strings (line_number_tags connected to this junction).
    * `off_page_connector`: Boolean.
    * `page_reference`: String or null (if `off_page_connector` is true).
    * `bounding_box`: [x1, y1, x2, y2].
    * `category_name`: "junctions".
    * `label`: String.

    **8. annotations (array of objects):**
    * `text`: String (the actual text).
    * `associated_tag`: String (tag of component it's related to) or null.
    * `category`: String ("stream_label", "equipment_note", "direction", "other") or null.
    * `bounding_box`: [x1, y1, x2, y2].
    * `category_name`: "annotations".
    * `label`: String.

    **9. safety_devices (array of objects):**
    * `tag`: String or null.
    * `type`: String (e.g., "PSV", "BDV").
    * `set_pressure`: String or null.
    * `installed_on_tag`: String (tag of equipment it's installed on) or null.
    * `bounding_box`: [x1, y1, x2, y2].
    * `category_name`: "safety_devices".
    * `label`: String.

    **10. unrecognized_symbols (array of objects):**
    * `description`: String (e.g., "unknown custom valve symbol").
    * `bounding_box`: [x1, y1, x2, y2].
    * `flag_for_review`: Boolean (always `true` for this category).
    * `review_reason`: String.
    * `category_name`: "unrecognized_symbols".
    * `label`: String.

    **Final Output:** The complete JSON object, nothing else.
    """
    
    file_extension = os.path.splitext(processed_image_path)[1].lower()
    mime_type = 'image/jpeg' if file_extension in ['.jpg', '.jpeg'] else 'image/png'
    with open(processed_image_path, "rb") as f: image_bytes = f.read()
    image = Part.from_data(data=image_bytes, mime_type=mime_type)

    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

    print(f"🚀 Sending request to {MODEL_ID} in {LOCATION}, please wait...")
    response = model.generate_content([image, prompt], safety_settings=safety_settings)

    if os.path.exists(processed_image_path) and processed_image_path != image_file_path:
        os.remove(processed_image_path)

    try:
        data = extract_json_from_response(response.text)
        if data:
            print("✅ Analysis Complete!")
            return data
        else:
            print("❌ Error: Could not find or parse JSON in the AI response.")
            print("--- Raw Response from API ---"); print(response.text)
            return None
    except Exception as e:
        print(f"❌ An error occurred during parsing: {e}")
        return None