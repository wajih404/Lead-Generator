import re


def detect_property_type(message_text: str):
    text = message_text.lower()

    if "villa" in text:
        return "Villa"
    elif "apartment" in text:
        return "Apartment"
    elif "townhouse" in text:
        return "Townhouse"
    elif "studio" in text:
        return "Studio"

    return None


def detect_location(message_text: str):
    text = message_text.lower()

    if "dubai marina" in text:
        return "Dubai Marina"
    elif "downtown" in text:
        return "Downtown"
    elif "jvc" in text:
        return "JVC"
    elif "dubai hills" in text:
        return "Dubai Hills"

    return None


def detect_budget(message_text: str):
    text = message_text.lower()

    # Match values like 2M, 2.5M, 3 million
    million_match = re.search(r'\b(\d+(?:\.\d+)?)\s*(m|million)\b', text)
    if million_match:
        return f"{million_match.group(1)}M AED"

    # Match values like 500000 AED or 500,000 AED
    aed_match = re.search(r'\b(\d[\d,]*)\s*aed\b', text)
    if aed_match:
        return f"{aed_match.group(1)} AED"

    return None


def detect_timeline(message_text: str):
    text = message_text.lower()

    timeline_match = re.search(
        r'\b(\d+)\s*(day|days|week|weeks|month|months|year|years)\b',
        text
    )
    if timeline_match:
        return f"{timeline_match.group(1)} {timeline_match.group(2)}"

    if "asap" in text:
        return "ASAP"
    elif "immediately" in text:
        return "Immediately"
    elif "urgent" in text:
        return "Urgent"

    return None


def create_lead_from_message(message: dict):
    message_text = message.get("message_text", "")

    property_type = detect_property_type(message_text)
    location = detect_location(message_text)
    budget = detect_budget(message_text)
    timeline = detect_timeline(message_text)

    return {
        "phone_number": message.get("phone_number"),
        "name": None,
        "budget": budget,
        "location": location,
        "property_type": property_type,
        "timeline": timeline,
        "status": "NEW"
    }