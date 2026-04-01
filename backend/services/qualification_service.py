def get_next_question(lead: dict):
    if not lead.get("property_type"):
        return "Are you looking for a villa, apartment, or townhouse?"

    if not lead.get("location"):
        return "Which location in Dubai are you interested in?"

    if not lead.get("budget"):
        return "May I know your approximate budget for the property?"

    if not lead.get("timeline"):
        return "When are you planning to buy the property?"

    return None