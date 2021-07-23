import jsonschema

_SCHEMA = {
    "type": "object",
    "properties": {
        "schemas": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "fields": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "type": {"type": "string"}
                            },
                            "additionalProperties": False,
                            "required": ["name", "type"]
                        }
                    }
                },
                "additionalProperties": False,
                "required": ["name", "fields"]
            }
        },
        "sinks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "additionalProperties": False,
                "required": ["name"]
            }
        },
        "sources": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "config": {"type": "object"},
                    "schema": {"type": "string"}
                },
                "additionalProperties": False,
                "required": ["name", "config"]
            }
        },
        "streams": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "sql": {"type": "string"},
                    "schema": {"type": "string"}
                },
                "additionalProperties": False,
                "required": ["name", "sql"]
            }
        },
        "tables": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "sql": {"type": "string"},
                    "schema": {"type": "string"}
                },
                "additionalProperties": False,
                "required": ["name", "sql"]
            }
        }
    }
}


def validate(doc: dict) -> None:
    try:
        jsonschema.validate(doc, _SCHEMA)
    except jsonschema.ValidationError as e:
        path = "/".join([str(item) for item in e.path])
        raise ValueError(f"File format is not valid in path [{path}]: error {e.message}")
    _assert_no_empty_spec(doc)


def _assert_no_empty_spec(doc: dict) -> None:
    for key, val in doc.items():
        if val:
            return
    raise ValueError("Configuration does not define any resource")
