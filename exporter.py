import xml.etree.ElementTree as ET
from xml.dom import minidom
import os

def save_to_xml(data, xml_file_path):
    """
    Converts the AI's category-based JSON into a structured XML file,
    formatted in a way that aligns with ISO 15926 principles for data exchange.
    """
    print(f"-----------Exporting data to XML at {xml_file_path}...")
    
  
    root = ET.Element("PIDModel")
    root.set("standard", "ISA-5.1") 

    # --- Metadata Section 
    metadata = data.get("metadata", {})
    if metadata:
        meta_element = ET.SubElement(root, "Metadata")
        # Handle both list and object
        display_object = metadata[0] if isinstance(metadata, list) and metadata else metadata if isinstance(metadata, dict) else None
        if display_object:
            for key, value in display_object.items():
             
                tag_name = key.replace("_", " ").title().replace(" ", "")
                child = ET.SubElement(meta_element, tag_name)
                child.text = str(value)

    for category_name, items in data.items():
        if category_name == "metadata" or not isinstance(items, list):
            continue

        category_element = ET.SubElement(root, f"{category_name.capitalize()}List")
        
        for item in items:
     
            item_element = ET.SubElement(category_element, category_name.capitalize())
          
            for key, value in item.items():
              
                if key == "bounding_box" and isinstance(value, list):
                    bbox_el = ET.SubElement(item_element, "BoundingBox")
                    bbox_el.set("x1", str(value[0]))
                    bbox_el.set("y1", str(value[1]))
                    bbox_el.set("x2", str(value[2]))
                    bbox_el.set("y2", str(value[3]))
                else:
                    tag_name = key.replace("_", " ").title().replace(" ", "")
                    child = ET.SubElement(item_element, tag_name)
                    child.text = str(value)

    xml_str = ET.tostring(root, 'utf-8')

    parsed_str = minidom.parseString(xml_str)
    pretty_xml_str = parsed_str.toprettyxml(indent="  ")

 
    os.makedirs(os.path.dirname(xml_file_path), exist_ok=True)
    with open(xml_file_path, "w", encoding="utf-8") as f:
        f.write(pretty_xml_str)
    
    print("---/// Data successfully exported to XML.")

