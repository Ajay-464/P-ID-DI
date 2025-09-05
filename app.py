import streamlit as st
import os
import pandas as pd
import json
import streamlit.components.v1 as components
from jsonschema import validate, ValidationError
from analyzer import analyze_pid
from schema import PID_SCHEMA_V2 as PID_SCHEMA
from visualizer import draw_bounding_boxes
from intelligence_builder import build_knowledge_graph_from_tables
from postprocessing import postprocess_pid_data
from exporter import save_to_xml
import tempfile

st.set_page_config(page_title="P&ID to Digital Intelligence", layout="wide")

if "extracted_data" not in st.session_state:
    st.session_state.extracted_data = None
if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

st.title("P&ID >>> Digital Intelligence")
st.write(
    "Upload any P&ID (CAD, scanned, or hand-drawn) to generate a structured data model "
    "and an interactive process flow graph."
)

uploaded_file = st.file_uploader("Choose a P&ID image file", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    if uploaded_file.name != st.session_state.uploaded_file_name:
        st.session_state.extracted_data = None
        st.session_state.uploaded_file_name = uploaded_file.name

    col1, col2, col3, _ = st.columns([1, 1, 1, 3])
    with col1:
        if st.button("Analyze P&ID", use_container_width=True):
            temp_dir = "temp_uploads"
            os.makedirs(temp_dir, exist_ok=True)
            temp_path = os.path.join(temp_dir, uploaded_file.name)

            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner("Analyzing the P&ID image..."):
                try:
                    raw_data = analyze_pid(temp_path)

                    if raw_data:
                        data = postprocess_pid_data(raw_data)
                        validate(instance=data, schema=PID_SCHEMA)
                        st.session_state.extracted_data = data
                        st.success(" Analysis Complete, Standardized & Schema Validated!")
                    else:
                        st.error("***** Analysis failed. AI returned no data.")

                except ValidationError as e:
                    st.session_state.extracted_data = None
                    st.error(f"***** Schema Validation Error: {e.message}")
                    st.subheader("Invalid Data (after postprocessing):")
                    st.json(data if 'data' in locals() else raw_data)

                except Exception as e:
                    st.session_state.extracted_data = None
                    st.error(f"***** An unexpected error occurred: {e}")

                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)

    with col2:
        if st.session_state.extracted_data and st.button("Clear Results", use_container_width=True):
            st.session_state.extracted_data = None
            st.rerun()

if st.session_state.extracted_data:
    data = st.session_state.extracted_data

    st.write("---")
    st.header("Visual AI Detections")

    vis_col1, vis_col2 = st.columns(2)
    with vis_col1:
        st.subheader("Original Image")
        st.image(uploaded_file, caption="Original P&ID", use_container_width=True)

    with vis_col2:
        st.subheader("AI Detections")
        annotated_image_path = draw_bounding_boxes(uploaded_file, data)
        if annotated_image_path:
            st.image(
                annotated_image_path,
                caption="P&ID with AI Detections",
                use_container_width=True,
            )
            os.remove(annotated_image_path)

    st.write("---")
    st.header("Analysis Results")
    tab1, tab2 = st.tabs(["---- Detailed Data Tables", "---- Interactive Knowledge Graph"])

    with tab1:
        # Metadata
        if "metadata" in data and data["metadata"]:
            st.subheader("Metadata")
            metadata_content = data["metadata"]
            display_object = (
                metadata_content[0]
                if isinstance(metadata_content, list) and metadata_content
                else metadata_content if isinstance(metadata_content, dict)
                else None
            )
            if display_object:
                st.json(display_object)
                json_string_meta = json.dumps(display_object, indent=4).encode("utf-8")
                st.download_button(
                    "Download Metadata as JSON",
                    json_string_meta,
                    f"{os.path.splitext(st.session_state.uploaded_file_name)[0]}_metadata.json",
                    "application/json",
                    key="json_meta"
                )
            st.write("---")

        # Tables
        category_mapping = {
            "equipment": "Equipment",
            "instrumentation": "Instrumentation",
            "lines": "Piping Lines",
            "valves": "Valves",
            "junctions": "Junctions",
            "control_relationships": "Control Relationships",
            "annotations": "Annotations",
            "safety_devices": "Safety Devices",
            "unrecognized_symbols": "Unrecognized Symbols"
        }

        for key, label in category_mapping.items():
            if key in data and data[key]:
                st.subheader(f"Detected {label}")
                if isinstance(data[key], list):
                    df = pd.DataFrame(data[key])
                    st.dataframe(df, use_container_width=True)

                    btn_col1, btn_col2, btn_col3 = st.columns(3)
                    with btn_col1:
                        csv = df.to_csv(index=False).encode("utf-8")
                        st.download_button(
                            f"Download {label} as CSV",
                            csv,
                            f"{os.path.splitext(st.session_state.uploaded_file_name)[0]}_{key}.csv",
                            "text/csv",
                            key=f"csv_{key}",
                            use_container_width=True
                        )
                    with btn_col2:
                        json_string = json.dumps(data[key], indent=4).encode("utf-8")
                        st.download_button(
                            f"Download {label} as JSON",
                            json_string,
                            f"{os.path.splitext(st.session_state.uploaded_file_name)[0]}_{key}.json",
                            "application/json",
                            key=f"json_{key}",
                            use_container_width=True
                        )
                    with btn_col3:
                        tmp_xml_path = os.path.join(tempfile.gettempdir(), f"{key}.xml")
                        save_to_xml({key: data[key]}, tmp_xml_path)
                        with open(tmp_xml_path, "r", encoding="utf-8") as f:
                            xml_string = f.read()
                        st.download_button(
                            f"Download {label} as XML",
                            xml_string,
                            f"{os.path.splitext(st.session_state.uploaded_file_name)[0]}_{key}.xml",
                            "application/xml",
                            key=f"xml_{key}",
                            use_container_width=True
                        )
                        os.remove(tmp_xml_path)

                    st.write("---")

    with tab2:
        st.info("You can drag nodes, zoom, and hover over components to see their details.")
        graph_path = build_knowledge_graph_from_tables(data)
        if graph_path and os.path.exists(graph_path):
            with open(graph_path, "r", encoding="utf-8") as f:
                source_code = f.read()
                components.html(source_code, height=800, scrolling=True)
            os.remove(graph_path)
        else:
            st.warning("***** Could not generate an interactive graph from the extracted data.")
