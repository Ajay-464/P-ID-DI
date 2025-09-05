Design & Implementation Document
Theme: P&ID to Digital Intelligence Platform
Team Details: 
1.	Abdullah [727723EUMT002]
2.	Swathi S [727723EUCB060]
3.	Ajay S [727722EUMT007]
4.	Deepak A [727722EUMT028]

Submission Links
•	Working Prototype Link: https://pid-digitizer.streamlit.app/
•	Demo Video Link: https://youtu.be/agXSbII2XJg?si=KLV8gIA9LAVgEKgI

Introduction: The Industrial Challenge & Our Solution
In capital-intensive industries such as energy, chemicals, and manufacturing, Piping and Instrumentation Diagrams (P&IDs) are the foundational language of plant design, operation, and maintenance. However, these critical documents are traditionally static, visual artifacts. The manual process of extracting data from them is notoriously slow, labor-intensive, and prone to human error, creating a significant bottleneck in project timelines and a barrier to digital transformation.
The P&ID to Digital Intelligence Platform is a working prototype designed to solve this fundamental challenge. It is a smart, AI-driven solution that ingests any P&ID whether a clean CAD export, a noisy scanned document, or even a hand-drawn sketch and intelligently converts it into a structured, interconnected, machine-readable digital model.
By leveraging a powerful multimodal AI at its core and wrapping it in a robust multi-stage processing pipeline, our platform moves beyond simple symbol recognition. It understands context, maps process flows, validates data against industry standards, and flags inconsistencies for human review. This transforms the P&ID from a static drawing into a dynamic digital asset, providing a robust foundation for faster project execution, enhanced safety, and the creation of true digital twins in the Industry 4.0 era.


Architecture & Workflow
Think of our system as a smart assembly line for processing P&ID drawings. Instead of one single step, we break the problem down into a series of specialized stages to ensure high quality and accuracy. 
The workflow is as follows:
1.	Image Cleanup (Preprocessing): When a user uploads a P&ID, it first goes to a "cleanup station." This part of our software automatically straightens crooked scans, removes random noise or "dirt," and makes the lines and text sharper. This is essential for helping the AI read messy or old drawings accurately.
2.	AI Analysis (The Brain): The clean image is then sent to the main "brain" of our system. This is where we use Google's powerful Gemini 2.5 Pro AI model. We give the AI a very detailed set of instructions, called a "master prompt," which tells it to act like an expert engineer. It looks at the drawing, finds all the symbols (like pumps and valves), reads all the text (like equipment tags), and understands how everything is connected.
3.	Quality Check (Validation): The data from the AI comes back as a single block of structured text (JSON). Before we do anything else, this data goes through a "quality check." We have a rulebook (schema.py) that makes sure the AI's output is formatted correctly. If it's not, the system flags an error instead of crashing.
4.	Final Polish (Postprocessing & Review): The validated data then goes to a "finishing station." This step automatically standardizes the data to match industry conventions (like ISA-5.1) and runs another check to find potential mistakes the AI might have made, such as a pump that isn't connected to any pipes. These potential mistakes are then flagged for a human to review.
5.	Display and Export: Finally, the clean, validated, and reviewed data is presented to the user in the application.

Core Modules & Technologies Used
This table outlines the essential components of the P&ID Digital Intelligence Platform, detailing the specific technologies used for each stage of the analysis pipeline and their purpose within the project.
Process Stage	Key Technologies & Libraries Used	Purpose & Function
1. Image Preprocessing	OpenCV (opencv-python)	To ensure robustness with varied P&ID formats (scanned, noisy), this module automatically cleans the input image. It applies grayscale conversion, denoising, and adaptive thresholding to create a high-contrast binary image, which significantly improves the AI's detection accuracy.
2. Core AI Analysis	Vertex AI – Google Gemini 2.5 Pro	This is the "brain" of the platform. The model performs the integrated tasks of Computer Vision (recognizing symbols), OCR (extracting text tags), and Natural Language Reasoning (understanding the context and relationships) from the pre-processed image.
3. AI Instruction Engine	Vertex - Training	A key innovation of this project. Instead of traditional model training, we use a highly detailed set of instructions to command the AI. This prompt enforces precision in bounding boxes, adherence to ISA/ISO standards, and structures the output into specific categories.
4. Data Validation	Json-schema	This module acts as a critical quality gate. It uses a flexible schema (schema.py) to validate the structure of the AI's JSON output, ensuring it is well-formed before being passed to the user interface. This prevents application crashes from unexpected AI responses.
5. User Interface (UI)	Streamlit	The entire user-facing application is built with Streamlit. It provides the file uploader, action buttons, data tables, and interactive tabs in a clean, professional web interface, all written in pure Python.
6. Data Structuring & Display	Pandas	The lists of extracted components (e.g., all equipment, all valves) are loaded into Pandas Data Frames, which are then rendered as the clean, sortable "Detailed Data Tables" in the UI.
7. Bounding Box Visualization	Pillow (PIL)	The visualizer.py module uses Pillow to draw coloured, precise bounding boxes and labels for every detected item onto a copy of the original P&ID. This provides immediate, intuitive visual feedback on the AI's performance.
8. Process Flow Mapping	Pyvis & NetworkX	The intelligence_builder.py module takes the extracted data (specifically the source_tag and destination_tag fields) and constructs a true process flow graph. This is then rendered as the "Interactive Knowledge Graph," a dynamic, hierarchical flowchart.

Key Library Versions:
The following open-source libraries and specific versions were used to build the platform's functionality:
Library	Version Used	Purpose in Project
streamlit	1.30.0	The web application framework for the entire user interface.
google-cloud-aiplatform	1.40.0	The official Google SDK for communicating with the Gemini API.
opencv-python	4.8.0	The computer vision library for image preprocessing (cleanup).
Pillow	10.0.1	The image processing library for drawing bounding boxes.
pandas	2.1.3	Used to create and display the structured data tables.
jsonschema	4.20.0	Used to validate the structure of the AI's JSON output.
pyvis	0.3.2	The library used to render the interactive knowledge graph.
networkx	3.2.1	Used to construct the underlying graph model of the P&ID.

Meeting the Core Requirements
The final platform was explicitly designed to meet and exceed all five core challenges:
•	Understand Industrial Symbols: This is achieved by the Gemini 2.5 Pro model, refined by our hyper-specific prompt. The preprocessing step ensures that the model can recognize symbols even on noisy or scanned drawings.
•	Extract Text and Labels: The model's integrated OCR capabilities are leveraged to read tags, line numbers, and other textual data. The postprocessing.py module then cleans and standardizes this text (e.g., ensuring consistent tag formats).
•	Map Connections Between Components: This is a central feature. The AI is instructed to identify the source_tag and destination_tag for all Lines. This relational data is then used by the intelligence_builder.py module to construct the "Interactive Knowledge Graph," which visually recreates the process flow.
•	Store Data in an Organized, Industry-Compliant Format: The AI generates a highly structured JSON output, which is validated by our schema.py. The UI provides download options for this JSON, for per-category CSVs, and for a structured XML file, which is a key step toward ISO 15926 compliance.
•	Handle Inconsistencies: This is handled by a two-pronged approach. First, the AI prompt instructs the model to flag ambiguous items. Second, our custom review_engine.py programmatically inspects the final data for issues like orphan nodes and low-confidence scores, presenting them in the "Quality & Review Panel" for human verification.
Process Flow:


Industrial Impact & Potential:
By successfully automating the P&ID digitization process, this platform has a significant and direct industrial impact:
•	Faster Project Execution: It drastically reduces the man-hours required for data take off in both greenfield and brownfield projects, accelerating engineering timelines.
•	Seamless Integration: The structured JSON, CSV, and XML outputs provide a clean data source that can be directly integrated with simulation software, asset management systems, and modern automation platforms.
•	Improved Accuracy and Consistency: It eliminates human error in data transcription and ensures a consistent interpretation of diagrams across an entire project.
•	A Foundation for Industry 4.0: This platform is the first essential step in creating a true "digital twin" of a physical plant. The structured, interconnected data it produces is the prerequisite for enabling smart monitoring, predictive maintenance, advanced operational analytics, and other smart plant initiatives.
