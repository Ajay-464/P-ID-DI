# normalizer.py
import re
import copy

# --- ISA tag patterns: FT-101, TIC-203A, PSV-1001 etc.
TAG_RE = re.compile(r"^([A-Z]{1,4})[-\s]?(\d{2,5}[A-Z]?)$")

ISA_FUNCTION_MAP = {
    # leading letter(s) -> measured variable
    "F": "Flow", "T": "Temperature", "P": "Pressure", "L": "Level",
    # common combos
    "TI": "Temperature", "PI": "Pressure", "FI": "Flow", "LI": "Level",
    "TIC": "Temperature", "FIC": "Flow", "PIC": "Pressure", "LIC": "Level"
}

VALVE_TYPE_TO_ISA = {
    "Control Valve": "ISA-5.1",
    "Gate Valve": "ISO 14617",
    "Globe Valve": "ISO 14617",
    "Check Valve": "ISO 14617",
    "Relief Valve": "ISO 14617"
}

EQUIPMENT_TO_ISO15926 = {
    "Pump": "Pump",
    "Centrifugal Pump": "Pump",
    "Compressor": "Compressor",
    "Heat Exchanger": "Heat Exchanger",
    "Reboiler": "Heat Exchanger",
    "Vessel": "Vessel",
    "Column": "Column",
    "Tank": "Tank",
    "Filter": "Filter"
}

LINE_STYLE_TO_TYPE = {
    "solid": "process",
    "dash": "instrument_signal",
    "dashed": "instrument_signal",
    "dot-dash": "electrical_signal",
    "dotted": "pneumatic"  # tweak per your legend
}

def parse_tag(tag: str):
    if not tag or not isinstance(tag, str):
        return None, None
    m = TAG_RE.match(tag.strip())
    if not m:
        return None, None
    return m.group(1), m.group(2)  # (prefix, number)

def infer_measured_variable(tag_prefix: str):
    if not tag_prefix: return None
    # long → short matching
    if tag_prefix in ISA_FUNCTION_MAP:
        return ISA_FUNCTION_MAP[tag_prefix]
    # try first letter
    return ISA_FUNCTION_MAP.get(tag_prefix[0], None)

def normalize_instrument(inst):
    inst = copy.deepcopy(inst)
    prefix, loop = parse_tag(inst.get("tag",""))
    inst["loop_id"] = inst.get("loop_id") or loop
    if not inst.get("measured_variable"):
        inst["measured_variable"] = infer_measured_variable(prefix)
    inst["standard_reference"] = "ISA-5.1"
    # Guess ISA function (I/C/T) from tag letters if missing
    letters = prefix or ""
    if "isa_function" not in inst or not inst["isa_function"]:
        if "IC" in letters: inst["isa_function"] = "Indicating Controller"
        elif letters.endswith("I"): inst["isa_function"] = "Indicator"
        elif letters.endswith("T"): inst["isa_function"] = "Transmitter"
        else: inst["isa_function"] = None
    return inst

def normalize_valve(v):
    v = copy.deepcopy(v)
    v["standard_reference"] = VALVE_TYPE_TO_ISA.get(v.get("type",""), "ISA-5.1")
    if "fail_position" not in v: v["fail_position"] = None
    return v

def normalize_equipment(eq):
    eq = copy.deepcopy(eq)
    eq["standard_reference"] = "ISO 15926"
    eq["iso15926_class"] = EQUIPMENT_TO_ISO15926.get(eq.get("type",""), "Equipment")
    return eq

def normalize_line(ln):
    ln = copy.deepcopy(ln)
    ln["standard_reference"] = "ISO 10628"
    if not ln.get("line_type"):
        hint = (ln.get("style_hint") or "").lower()
        for k,v in LINE_STYLE_TO_TYPE.items():
            if k in hint:
                ln["line_type"] = v
                break
        if not ln.get("line_type"):
            ln["line_type"] = "unknown"
    return ln

def attach_flags(item):
    flags = []
    if "bounding_box" in item:
        bb = item["bounding_box"]
        if not (isinstance(bb, list) and len(bb) == 4):
            flags.append("invalid_bbox")
        else:
            x1,y1,x2,y2 = bb
            if x2 <= x1 or y2 <= y1:
                flags.append("bbox_not_tight")
    else:
        flags.append("missing_bbox")

    if "tag" in item and (item.get("tag") in [None,"","Unknown","UNK"]):
        flags.append("missing_tag")
    if flags:
        item["flags"] = sorted(list(set(item.get("flags", []) + flags)))
    return item

def normalize_all(data):
    data = copy.deepcopy(data)
    data["metadata"] = data.get("metadata", {})
    data["metadata"]["standards_referenced"] = ["ISA-5.1","ISO 10628","ISO 14617","ISO 15926"]

    data["equipment"] = [attach_flags(normalize_equipment(e)) for e in data.get("equipment", [])]
    data["valves"] = [attach_flags(normalize_valve(v)) for v in data.get("valves", [])]
    data["instrumentation"] = [attach_flags(normalize_instrument(i)) for i in data.get("instrumentation", [])]
    data["lines"] = [attach_flags(normalize_line(l)) for l in data.get("lines", [])]

    # Pass-through categories
    for k in ["junctions","control_relationships","annotations","safety_devices","unrecognized_symbols"]:
        data[k] = [attach_flags(x) for x in data.get(k, [])]

    return data

# --- ISO 15926 export (lean JSON) ---
def to_iso15926(data):
    """
    Minimal ISO 15926-like export:
    - equipment as physical objects with class
    - lines as pipeline segments
    - instruments/valves linked via 'installed_on'/'connected_to' where possible
    """
    out = {
        "context": "ISO 15926 (lean profile)",
        "equipment": [],
        "pipeline_segments": [],
        "instruments": [],
        "valves": []
    }
    tag_index = {e.get("tag"): e for e in data.get("equipment", []) if e.get("tag")}
    line_index = {l.get("line_number_tag"): l for l in data.get("lines", []) if l.get("line_number_tag")}

    for e in data.get("equipment", []):
        out["equipment"].append({
            "id": e.get("tag"),
            "class": e.get("iso15926_class","Equipment"),
            "description": e.get("description"),
            "service": e.get("service"),
            "spec": e.get("spec")
        })

    for l in data.get("lines", []):
        out["pipeline_segments"].append({
            "id": l.get("line_number_tag"),
            "type": l.get("line_type"),
            "size": l.get("nominal_size"),
            "spec": l.get("spec"),
            "service": l.get("service"),
            "from": l.get("source_tag"),
            "to": l.get("destination_tag")
        })

    for i in data.get("instrumentation", []):
        out["instruments"].append({
            "id": i.get("tag"),
            "variable": i.get("measured_variable"),
            "loop": i.get("loop_id"),
            "connected_to": i.get("connected_to_tag")
        })

    for v in data.get("valves", []):
        out["valves"].append({
            "id": v.get("tag"),
            "type": v.get("type"),
            "on_line": v.get("installed_on_line_tag"),
            "fail_position": v.get("fail_position")
        })
    return out
