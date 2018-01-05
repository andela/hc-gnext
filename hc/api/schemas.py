check = {
    "properties": {
        "name": {"type": "string"},
        "tags": {"type": "string"},
        "is_high_priority": {"type": "string"},
        "user_emails": {"type": "string"},
        "timeout": {"type": "number", "minimum": 60, "maximum": 604800},
        "grace": {"type": "number", "minimum": 60, "maximum": 604800},
        "interval": {"type": "number", "minimum": 60, "maximum": 604800},
        "channels": {"type": "string"}
    }
}
