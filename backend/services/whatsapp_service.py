def parse_incoming_message(payload: dict):
    sender = payload.get("from")
    text = payload.get("text")

    return {
        "phone_number": sender,
        "message_text": text
    }