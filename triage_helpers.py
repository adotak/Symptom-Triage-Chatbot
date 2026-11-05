"""Pure helpers used by the MediGuide interfaces."""


HOSPITALS_BY_CITY = {
    "karachi": (
        "1. Aga Khan University Hospital\n"
        "2. Liaquat National Hospital\n"
        "3. Jinnah Postgraduate Medical Centre (JPMC)"
    ),
    "lahore": (
        "1. Shaukat Khanum Memorial Cancer Hospital\n"
        "2. Mayo Hospital\n"
        "3. Doctors Hospital & Medical Center"
    ),
    "islamabad": (
        "1. Shifa International Hospital\n"
        "2. Pakistan Institute of Medical Sciences (PIMS)\n"
        "3. Quaid-e-Azam International Hospital"
    ),
    "peshawar": (
        "1. Lady Reading Hospital\n"
        "2. Khyber Teaching Hospital\n"
        "3. Hayatabad Medical Complex"
    ),
    "quetta": (
        "1. Bolan Medical Complex Hospital\n"
        "2. Civil Hospital Quetta\n"
        "3. Akram Hospital"
    ),
}


def find_nearby_clinics(location: str) -> str:
    """Return known hospitals for a city, with a safe fallback for other areas."""
    normalized_location = location.strip().casefold()
    for city, hospitals in HOSPITALS_BY_CITY.items():
        if city in normalized_location:
            return f"Here are some major hospitals in {city.title()}:\n{hospitals}"

    return (
        f"I couldn't find specific hospitals in my database for '{location}'. "
        "Please search Google Maps for 'hospitals near me' or proceed to your "
        "nearest district hospital."
    )


def extract_message_parts(message) -> list[str]:
    """Extract non-empty text and uploaded file paths from Gradio input."""
    if isinstance(message, dict):
        parts = [message.get("text", "")]
        files = message.get("files", [])
    else:
        parts = [message]
        files = []

    for uploaded_file in files:
        if isinstance(uploaded_file, dict):
            uploaded_file = uploaded_file.get("path") or uploaded_file.get("name")
        elif hasattr(uploaded_file, "path"):
            uploaded_file = uploaded_file.path
        parts.append(uploaded_file)

    return [str(part).strip() for part in parts if part and str(part).strip()]
