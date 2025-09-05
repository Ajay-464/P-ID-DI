# PID_SCHEMA_V2 = {
#     "type": "object",
#     "properties": {
#         "metadata": {
#             "type": "object",
#             "properties": {
#                 "drawing_title": {"type": "string"},
#                 "drawing_number": {"type": "string"},
#                 "revision": {"type": "string"},
#                 "standards_referenced": {"type": "array", "items": {"type": "string"}}
#             },
#             "additionalProperties": True
#         },
#         "equipment": {
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "required": ["tag", "type", "bounding_box"],
#                 "properties": {
#                     "tag": {"type": "string"},
#                     "type": {"type": "string"},
#                     "description": {"type": ["string", "null"]},
#                     "bounding_box": {
#                         "type": "array",
#                         "items": {"type": "number"},
#                         "minItems": 4,
#                         "maxItems": 4
#                     },
#                     "size_nominal": {"type": ["string", "number", "null"]},
#                     "service": {"type": ["string", "null"]},
#                     "spec": {"type": ["string", "null"]},
#                     "standard_reference": {
#                         "type": ["string", "null"],
#                         "enum": ["ISO 15926", None]
#                     },
#                     "iso15926_class": {"type": ["string", "null"]},
#                     "confidence": {"type": ["number", "null"]},
#                     "flags": {"type": "array", "items": {"type": "string"}}
#                 },
#                 "additionalProperties": True
#             }
#         },
#         "valves": {
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "required": ["type", "bounding_box"],
#                 "properties": {
#                     "tag": {"type": ["string", "null"]},
#                     "type": {"type": "string"},
#                     "installed_on_line_tag": {"type": ["string", "null"]},
#                     "fail_position": {
#                         "type": ["string", "null"],
#                         "enum": ["FO", "FC", "FL", "Unknown", None]
#                     },
#                     "bounding_box": {
#                         "type": "array",
#                         "items": {"type": "number"},
#                         "minItems": 4,
#                         "maxItems": 4
#                     },
#                     "standard_reference": {
#                         "type": ["string", "null"],
#                         "enum": ["ISA-5.1", "ISO 10628", "ISO 14617", None]
#                     },
#                     "isa_symbol_code": {"type": ["string", "null"]},
#                     "confidence": {"type": ["number", "null"]},
#                     "flags": {"type": "array", "items": {"type": "string"}}
#                 },
#                 "additionalProperties": True
#             }
#         },
#         "instrumentation": {
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "required": ["tag", "type", "bounding_box"],
#                 "properties": {
#                     "tag": {"type": "string"},
#                     "type": {"type": "string"},
#                     "measured_variable": {"type": ["string", "null"]},
#                     "isa_function": {"type": ["string", "null"]},
#                     "loop_id": {"type": ["string", "null"]},
#                     "connected_to_tag": {"type": ["string", "null"]},
#                     "bounding_box": {
#                         "type": "array",
#                         "items": {"type": "number"},
#                         "minItems": 4,
#                         "maxItems": 4
#                     },
#                     "standard_reference": {
#                         "type": ["string", "null"],
#                         "enum": ["ISA-5.1", None]
#                     },
#                     "confidence": {"type": ["number", "null"]},
#                     "flags": {"type": "array", "items": {"type": "string"}}
#                 },
#                 "additionalProperties": True
#             }
#         },
#         "lines": {
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "required": ["line_type"],
#                 "properties": {
#                     "line_number_tag": {"type": ["string", "null"]},
#                     "source_tag": {"type": ["string", "null"]},
#                     "destination_tag": {"type": ["string", "null"]},
#                     "line_type": {
#                         "type": "string",
#                         "enum": [
#                             "process",
#                             "instrument_signal",
#                             "electrical_signal",
#                             "electrical",
#                             "Pneumatic Signal",
#                             "pneumatic",
#                             "hydraulic",
#                             "utility",
#                             "unknown",
#                             "vent"
#                         ]
#                     },
#                     "style_hint": {"type": ["string", "null"]},
#                     "nominal_size": {"type": ["string", "number", "null"]},
#                     "spec": {"type": ["string", "null"]},
#                     "service": {"type": ["string", "null"]},
#                     "polyline": {"type": ["array", "null"]},
#                     "standard_reference": {
#                         "type": ["string", "null"],
#                         "enum": ["ISO 10628", None]
#                     },
#                     "confidence": {"type": ["number", "null"]},
#                     "flags": {"type": "array", "items": {"type": "string"}}
#                 },
#                 "additionalProperties": True
#             }
#         },
#         "junctions": {
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "required": ["junction_id", "bounding_box"],
#                 "properties": {
#                     "junction_id": {"type": "string"},
#                     "connected_lines": {"type": "array", "items": {"type": "string"}},
#                     "off_page": {"type": ["boolean", "null"]},
#                     "page_ref": {"type": ["string", "null"]},
#                     "bounding_box": {
#                         "type": "array",
#                         "items": {"type": "number"},
#                         "minItems": 4,
#                         "maxItems": 4
#                     },
#                     "standard_reference": {
#                         "type": ["string", "null"],
#                         "enum": ["ISO 10628", None]
#                     },
#                     "confidence": {"type": ["number", "null"]},
#                     "flags": {"type": "array", "items": {"type": "string"}}
#                 },
#                 "additionalProperties": True
#             }
#         },
#         "control_relationships": {
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "required": ["source_tag", "destination_tag", "relationship_type"],
#                 "properties": {
#                     "source_tag": {"type": "string"},
#                     "destination_tag": {"type": "string"},
#                     "relationship_type": {
#                         "type": "string",
#                         "enum": ["measures", "controls", "drives", "signals"]
#                     },
#                     "loop_id": {"type": ["string", "null"]},
#                     "standard_reference": {
#                         "type": ["string", "null"],
#                         "enum": ["ISA-5.1", None]
#                     },
#                     "confidence": {"type": ["number", "null"]}
#                 },
#                 "additionalProperties": True
#             }
#         },
#         "annotations": {
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "required": ["text", "bounding_box"],
#                 "properties": {
#                     "text": {"type": "string"},
#                     "associated_tag": {"type": ["string", "null"]},
#                     "category": {
#                         "type": ["string", "null"],
#                         "enum": ["stream_label", "equipment_note", "direction", "other", None]
#                     },
#                     "bounding_box": {
#                         "type": "array",
#                         "items": {"type": "number"},
#                         "minItems": 4,
#                         "maxItems": 4
#                     }
#                 },
#                 "additionalProperties": True
#             }
#         },
#         "safety_devices": {
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "required": ["type", "bounding_box"],
#                 "properties": {
#                     "tag": {"type": ["string", "null"]},
#                     "type": {"type": "string"},
#                     "location": {"type": ["string", "null"]},
#                     "installed_on_tag": {"type": ["string", "null"]},
#                     "bounding_box": {
#                         "type": "array",
#                         "items": {"type": "number"},
#                         "minItems": 4,
#                         "maxItems": 4
#                     },
#                     "standard_reference": {
#                         "type": ["string", "null"],
#                         "enum": ["ISO 14617", "ISA-5.1", None]
#                     },
#                     "confidence": {"type": ["number", "null"]},
#                     "flags": {"type": "array", "items": {"type": "string"}}
#                 },
#                 "additionalProperties": True
#             }
#         },
#         "unrecognized_symbols": {
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "required": ["description", "bounding_box", "flag_for_review"],
#                 "properties": {
#                     "description": {"type": "string"},
#                     "bounding_box": {
#                         "type": "array",
#                         "items": {"type": "number"},
#                         "minItems": 4,
#                         "maxItems": 4
#                     },
#                     "flag_for_review": {"type": "boolean", "const": True}
#                 },
#                 "additionalProperties": True
#             }
#         }
#     },
#     "required": [],
#     "additionalProperties": True
# }

# schema.py

# PID_SCHEMA_V2 = {
#     "type": "object",
#     "properties": {
#         "metadata": {
#             "type": "object",
#             "properties": {
#                 "drawing_title": {"type": "string"},
#                 "drawing_number": {"type": "string"},
#                 "revision": {"type": "string"},
#                 "standards_referenced": {
#                     "type": "array",
#                     "items": {"type": "string"},
#                     "description": "e.g., ['ISA-5.1', 'ISO 10628', 'ISO 14617', 'ISO 15926']"
#                 }
#             },
#             "additionalProperties": True
#         },

#         "equipment": {
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "required": ["tag", "type", "bounding_box"],
#                 "properties": {
#                     "tag": {"type": "string"},
#                     "type": {"type": "string"},
#                     "description": {"type": ["string", "null"]},
#                     "bounding_box": {
#                         "type": "array",
#                         "items": {"type": "number"},
#                         "minItems": 4,
#                         "maxItems": 4
#                     },
#                     "size_nominal": {"type": ["string", "number", "null"]},
#                     "service": {"type": ["string", "null"]},
#                     "spec": {"type": ["string", "null"]},
#                     "standard_reference": {"type": ["string", "null"], "enum": ["ISO 15926", None]},
#                     "iso15926_class": {"type": ["string", "null"]},
#                     "confidence": {"type": ["number", "null"]},
#                     "flags": {"type": "array", "items": {"type": "string"}}
#                 },
#                 "additionalProperties": True
#             }
#         },

#         "valves": {
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "required": ["type", "bounding_box"],
#                 "properties": {
#                     "tag": {"type": ["string", "null"]},
#                     "type": {"type": "string"},
#                     "installed_on_line_tag": {"type": ["string", "null"]},
#                     "fail_position": {
#                         "type": ["string", "null"],
#                         "enum": ["FO", "FC", "FL", "Unknown", None]
#                     },
#                     "bounding_box": {
#                         "type": "array",
#                         "items": {"type": "number"},
#                         "minItems": 4,
#                         "maxItems": 4
#                     },
#                     "standard_reference": {
#                         "type": ["string", "null"],
#                         "enum": ["ISA-5.1", "ISO 10628", "ISO 14617", None]
#                     },
#                     "isa_symbol_code": {"type": ["string", "null"]},
#                     "confidence": {"type": ["number", "null"]},
#                     "flags": {"type": "array", "items": {"type": "string"}}
#                 },
#                 "additionalProperties": True
#             }
#         },

#         "instrumentation": {
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "required": ["tag", "type", "bounding_box"],
#                 "properties": {
#                     "tag": {"type": "string"},
#                     "type": {"type": "string"},
#                     "measured_variable": {"type": ["string", "null"]},
#                     "isa_function": {"type": ["string", "null"]},
#                     "loop_id": {"type": ["string", "null"]},
#                     "connected_to_tag": {"type": ["string", "null"]},
#                     "bounding_box": {
#                         "type": "array",
#                         "items": {"type": "number"},
#                         "minItems": 4,
#                         "maxItems": 4
#                     },
#                     "standard_reference": {"type": ["string", "null"], "enum": ["ISA-5.1", None]},
#                     "confidence": {"type": ["number", "null"]},
#                     "flags": {"type": "array", "items": {"type": "string"}}
#                 },
#                 "additionalProperties": True
#             }
#         },

#         "lines": {
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "required": ["line_type"],
#                 "properties": {
#                     "line_number_tag": {"type": ["string", "null"]},
#                     "source_tag": {"type": ["string", "null"]},
#                     "destination_tag": {"type": ["string", "null"]},
#                     "line_type": {
#                         "type": "string",
#                         "enum": [
#                             "process", "instrument_signal", "electrical_signal", "electrical", "Pneumatic Signal", 
#                             "pneumatic", "hydraulic", "utility", "unknown", "vent"
#                         ]
#                     },
#                     "style_hint": {"type": ["string", "null"]},
#                     "nominal_size": {"type": ["string", "number", "null"]},
#                     "spec": {"type": ["string", "null"]},
#                     "service": {"type": ["string", "null"]},
#                     "polyline": {"type": ["array", "null"]},
#                     "standard_reference": {"type": ["string", "null"], "enum": ["ISO 10628", None]},
#                     "confidence": {"type": ["number", "null"]},
#                     "flags": {"type": "array", "items": {"type": "string"}}
#                 },
#                 "additionalProperties": True
#             }
#         },

#         "junctions": {
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "required": ["junction_id", "bounding_box"],
#                 "properties": {
#                     "junction_id": {"type": "string"},
#                     "connected_lines": {"type": "array", "items": {"type": "string"}},
#                     "off_page": {"type": ["boolean", "null"]},
#                     "page_ref": {"type": ["string", "null"]},
#                     "bounding_box": {
#                         "type": "array",
#                         "items": {"type": "number"},
#                         "minItems": 4,
#                         "maxItems": 4
#                     },
#                     "standard_reference": {"type": ["string", "null"], "enum": ["ISO 10628", None]},
#                     "confidence": {"type": ["number", "null"]},
#                     "flags": {"type": "array", "items": {"type": "string"}}
#                 },
#                 "additionalProperties": True
#             }
#         },

#         "control_relationships": {
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "required": ["source_tag", "destination_tag", "relationship_type"],
#                 "properties": {
#                     "source_tag": {"type": "string"},
#                     "destination_tag": {"type": "string"},
#                     "relationship_type": {
#                         "type": "string",
#                         "enum": ["measures", "controls", "drives", "signals"]
#                     },
#                     "loop_id": {"type": ["string", "null"]},
#                     "standard_reference": {"type": ["string", "null"], "enum": ["ISA-5.1", None]},
#                     "confidence": {"type": ["number", "null"]}
#                 },
#                 "additionalProperties": True
#             }
#         },

#         "annotations": {
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "required": ["text", "bounding_box"],
#                 "properties": {
#                     "text": {"type": "string"},
#                     "associated_tag": {"type": ["string", "null"]},
#                     "category": {
#                         "type": ["string", "null"],
#                         "enum": ["stream_label", "equipment_note", "direction", "other", None]
#                     },
#                     "bounding_box": {
#                         "type": "array",
#                         "items": {"type": "number"},
#                         "minItems": 4,
#                         "maxItems": 4
#                     }
#                 },
#                 "additionalProperties": True
#             }
#         },

#         "safety_devices": {
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "required": ["type", "bounding_box"],
#                 "properties": {
#                     "tag": {"type": ["string", "null"]},
#                     "type": {"type": "string"},
#                     "location": {"type": ["string", "null"]},
#                     "installed_on_tag": {"type": ["string", "null"]},
#                     "bounding_box": {
#                         "type": "array",
#                         "items": {"type": "number"},
#                         "minItems": 4,
#                         "maxItems": 4
#                     },
#                     "standard_reference": {"type": ["string", "null"], "enum": ["ISO 14617", "ISA-5.1", None]},
#                     "confidence": {"type": ["number", "null"]},
#                     "flags": {"type": "array", "items": {"type": "string"}}
#                 },
#                 "additionalProperties": True
#             }
#         },

#         "unrecognized_symbols": {
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "required": ["description", "bounding_box", "flag_for_review"],
#                 "properties": {
#                     "description": {"type": "string"},
#                     "bounding_box": {
#                         "type": "array",
#                         "items": {"type": "number"},
#                         "minItems": 4,
#                         "maxItems": 4
#                     },
#                     "flag_for_review": {"type": "boolean", "const": True}
#                 },
#                 "additionalProperties": True
#             }
#         }
#     },
#     "required": [],
#     "additionalProperties": True
# }


# schema.py

PID_SCHEMA_V2 = {
    "type": "object",
    "properties": {
        "metadata": {
            "type": "object",
            "properties": {
                "drawing_title": {"type": ["string", "null"]},
                "drawing_number": {"type": ["string", "null"]},
                "revision": {"type": ["string", "null"]},
                "standards_referenced": {"type": "array", "items": {"type": "string"}}
            },
            "additionalProperties": True
        },
        "equipment": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["tag", "type", "bounding_box"],
                "properties": {
                    "tag": {"type": "string"},
                    "type": {"type": "string"},
                    "description": {"type": ["string", "null"]},
                    "bounding_box": {"type": "array", "items": {"type": "number"}, "minItems": 4, "maxItems": 4},
                    "size_nominal": {"type": ["string", "number", "null"]},
                    "service": {"type": ["string", "null"]},
                    "spec": {"type": ["string", "null"]},
                    "standard_reference": {"type": ["string", "null"], "enum": ["ISO 15926", None]},
                    "iso15926_class": {"type": ["string", "null"]},
                    "confidence": {"type": ["number", "null"]},
                    "flags": {"type": "array", "items": {"type": "string"}}
                },
                "additionalProperties": True
            }
        },
        "valves": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["type", "bounding_box"],
                "properties": {
                    "tag": {"type": ["string", "null"]},
                    "type": {"type": "string"},
                    "installed_on_line_tag": {"type": ["string", "null"]},
                    "fail_position": {"type": ["string", "null"], "enum": ["FO", "FC", "FL", "Unknown", None]},
                    "bounding_box": {"type": "array", "items": {"type": "number"}, "minItems": 4, "maxItems": 4},
                    "standard_reference": {"type": ["string", "null"], "enum": ["ISA-5.1", "ISO 10628", "ISO 14617", None]},
                    "isa_symbol_code": {"type": ["string", "null"]},
                    "confidence": {"type": ["number", "null"]},
                    "flags": {"type": "array", "items": {"type": "string"}}
                },
                "additionalProperties": True
            }
        },
        "instrumentation": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["tag", "type", "bounding_box"],
                "properties": {
                    "tag": {"type": "string"},
                    "type": {"type": "string"},
                    "measured_variable": {"type": ["string", "null"]},
                    "isa_function": {"type": ["string", "null"]},
                    "loop_id": {"type": ["string", "null"]},
                    "connected_to_tag": {"type": ["string", "null"]},
                    "bounding_box": {"type": "array", "items": {"type": "number"}, "minItems": 4, "maxItems": 4},
                    "standard_reference": {"type": ["string", "null"], "enum": ["ISA-5.1", None]},
                    "confidence": {"type": ["number", "null"]},
                    "flags": {"type": "array", "items": {"type": "string"}}
                },
                "additionalProperties": True
            }
        },
        "lines": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["line_type"],
                "properties": {
                    "line_number_tag": {"type": ["string", "null"]},
                    "source_tag": {"type": ["string", "null"]},
                    "destination_tag": {"type": ["string", "null"]},
                    "line_type": {"type": "string", "enum": ["process", "instrument_signal", "electrical_signal", "electrical", "Pneumatic Signal", "pneumatic", "hydraulic", "utility", "unknown", "vent"]},
                    "style_hint": {"type": ["string", "null"]},
                    "nominal_size": {"type": ["string", "number", "null"]},
                    "spec": {"type": ["string", "null"]},
                    "service": {"type": ["string", "null"]},
                    "polyline": {"type": ["array", "null"]},
                    "standard_reference": {"type": ["string", "null"], "enum": ["ISO 10628", None]},
                    "confidence": {"type": ["number", "null"]},
                    "flags": {"type": "array", "items": {"type": "string"}}
                },
                "additionalProperties": True
            }
        },
        "junctions": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["junction_id", "bounding_box"],
                "properties": {
                    "junction_id": {"type": "string"},
                    "connected_lines": {"type": "array", "items": {"type": "string"}},
                    "off_page": {"type": ["boolean", "null"]},
                    "page_ref": {"type": ["string", "null"]},
                    "bounding_box": {"type": "array", "items": {"type": "number"}, "minItems": 4, "maxItems": 4},
                    "standard_reference": {"type": ["string", "null"], "enum": ["ISO 10628", None]},
                    "confidence": {"type": ["number", "null"]},
                    "flags": {"type": "array", "items": {"type": "string"}}
                },
                "additionalProperties": True
            }
        },
        "control_relationships": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["source_tag", "destination_tag", "relationship_type"],
                "properties": {
                    "source_tag": {"type": "string"},
                    "destination_tag": {"type": "string"},
                    "relationship_type": {"type": "string", "enum": ["measures", "controls", "drives", "signals"]},
                    "loop_id": {"type": ["string", "null"]},
                    "standard_reference": {"type": ["string", "null"], "enum": ["ISA-5.1", None]},
                    "confidence": {"type": ["number", "null"]}
                },
                "additionalProperties": True
            }
        },
        "annotations": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["text", "bounding_box"],
                "properties": {
                    "text": {"type": "string"},
                    "associated_tag": {"type": ["string", "null"]},
                    "category": {
                        "type": ["string", "null"],
                        # --- CORRECTED LINE ---
                        # Added "line_spec" to the list of allowed values
                        "enum": ["stream_label", "equipment_note", "direction", "line_spec", "other", None]
                    },
                    "bounding_box": {"type": "array", "items": {"type": "number"}, "minItems": 4, "maxItems": 4}
                },
                "additionalProperties": True
            }
        },
        "safety_devices": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["type", "bounding_box"],
                "properties": {
                    "tag": {"type": ["string", "null"]},
                    "type": {"type": "string"},
                    "location": {"type": ["string", "null"]},
                    "installed_on_tag": {"type": ["string", "null"]},
                    "bounding_box": {"type": "array", "items": {"type": "number"}, "minItems": 4, "maxItems": 4},
                    "standard_reference": {"type": ["string", "null"], "enum": ["ISO 14617", "ISA-5.1", None]},
                    "confidence": {"type": ["number", "null"]},
                    "flags": {"type": "array", "items": {"type": "string"}}
                },
                "additionalProperties": True
            }
        },
        "unrecognized_symbols": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["description", "bounding_box", "flag_for_review"],
                "properties": {
                    "description": {"type": "string"},
                    "bounding_box": {"type": "array", "items": {"type": "number"}, "minItems": 4, "maxItems": 4},
                    "flag_for_review": {"type": "boolean", "const": True}
                },
                "additionalProperties": True
            }
        }
    },
    "required": [],
    "additionalProperties": True
}