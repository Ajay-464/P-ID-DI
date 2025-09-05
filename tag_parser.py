import re
ISA_INSTRUMENT_TAG_REGEX = re.compile(r'([A-Z]{2,4})-?(\d+)([A-Z]?)')
ISA_EQUIPMENT_TAG_REGEX = re.compile(r'([A-Z])-?(\d+)([A-Z]?/?B?)')

def parse_instrument_tag(tag):
    """
    Parses a standard ISA instrument tag using regex and extracts its components.
    Returns a dictionary with the parts or None if the tag is non-standard.
    """
    if not isinstance(tag, str):
        return None
        
    match = ISA_INSTRUMENT_TAG_REGEX.match(tag.strip())
    if not match:
        return None
    
    return {
        "function": match.group(1),
        "loop_id": match.group(2),
        "suffix": match.group(3)
    }

def parse_equipment_tag(tag):
    """
    Parses a standard ISA equipment tag using regex.
    Returns a dictionary with the parts or None if the tag is non-standard.
    """
    if not isinstance(tag, str):
        return None

    match = ISA_EQUIPMENT_TAG_REGEX.match(tag.strip())
    if not match:
        return None
    
    return {
        "class": match.group(1),
        "area_or_unit": match.group(2),
        "suffix": match.group(3)
    }

def validate_loop_integrity(instrument_list):
    """
    Groups instruments by their loop ID to help validate control loop integrity.
    Returns a dictionary where keys are loop IDs and values are lists of instrument tags.
    """
    loops = {}
    if not isinstance(instrument_list, list):
        return loops

    for instrument in instrument_list:
        tag = instrument.get('tag')
        parsed = parse_instrument_tag(tag)
        if parsed and parsed['loop_id']:
            loop_id = parsed['loop_id']
            if loop_id not in loops:
                loops[loop_id] = []
            loops[loop_id].append(tag)
            
    return loops

