import pandas as pd
from tag_parser import parse_instrument_tag, parse_equipment_tag

def generate_review_queue(data):
    """
    Analyzes the AI's graph data to flag potential errors and warnings for human review.

    Checks for:
    1. Items explicitly flagged for review by the AI.
    2. Low-confidence detections.
    3. Orphan nodes (components not connected to any lines).
    4. Non-standard tag formats.
    """
    print("🔍 Running Review Engine...")
    warnings = []
    
    nodes = data.get('nodes', [])
    if not nodes:
     
        return {"errors": [], "warnings": []}

    node_ids = {node.get('id') for node in nodes if node.get('id')}
    connected_nodes = set()
    for edge in data.get('edges', []):
        connected_nodes.add(edge.get('source'))
        connected_nodes.add(edge.get('target'))
    
    orphan_nodes = node_ids - connected_nodes
    
    for orphan_id in orphan_nodes:
        orphan_node_data = next((node for node in nodes if node.get('id') == orphan_id), {})
        warnings.append({
            "id": orphan_id,
            "issue_type": "Orphan Node",
            "details": f"Component '{orphan_id}' is not connected to any lines.",
            "bounding_box": orphan_node_data.get('attributes', {}).get('bounding_box')
        })


    for node in nodes:
        attributes = node.get('attributes', {})
        node_id = node.get('id')
        category = node.get('category')
        if attributes.get("flag_for_review") is True:
            warnings.append({
                "id": node_id,
                "issue_type": "AI Flagged",
                "details": attributes.get("review_reason", "AI detected a potential ambiguity."),
                "bounding_box": attributes.get('bounding_box')
            })

        
        confidence = attributes.get('confidence', 1.0)
        if confidence < 0.85:  
             warnings.append({
                "id": node_id,
                "issue_type": "Low Confidence",
                "details": f"Detection confidence is only {confidence:.2f}.",
                "bounding_box": attributes.get('bounding_box')
            })
            

        if category == 'Instrumentation' and not parse_instrument_tag(node_id):
            warnings.append({
                "id": node_id,
                "issue_type": "Invalid Tag Format",
                "details": f"Instrument tag '{node_id}' does not follow standard ISA-5.1 format.",
                "bounding_box": attributes.get('bounding_box')
            })
        elif category == 'Equipment' and not parse_equipment_tag(node_id):
             warnings.append({
                "id": node_id,
                "issue_type": "Invalid Tag Format",
                "details": f"Equipment tag '{node_id}' does not follow a standard format.",
                "bounding_box": attributes.get('bounding_box')
            })

    print(f"Review complete. Found {len(warnings)} potential issues.")
    return {"errors": [], "warnings": warnings}

