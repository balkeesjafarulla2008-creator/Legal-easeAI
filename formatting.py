def sanitize_text(text):
    if text is None:
        return ""
    return str(text).strip()