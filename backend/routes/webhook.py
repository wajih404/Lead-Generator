from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.services.whatsapp_service import parse_incoming_message
from backend.services.lead_service import create_lead_from_message
from backend.services.qualification_service import get_next_question
from backend.models.lead import Lead
from backend.models.message import Message

router = APIRouter(prefix="/webhook", tags=["webhook"])


class WebhookPayload(BaseModel):
    from_: str = Field(..., alias="from")
    text: str

    class Config:
        populate_by_name = True


@router.get("/360dialog")
async def verify_webhook():
    return {"message": "360dialog webhook GET working"}


@router.post("/360dialog")
async def receive_webhook(payload: WebhookPayload, db: Session = Depends(get_db)):
    print("WEBHOOK HIT")

    raw_payload = payload.model_dump(by_alias=True)

    # Convert Swagger/body model into the format your existing services expect
    incoming_payload = {
        "from": payload.from_,
        "text": payload.text
    }

    # Step 1: Parse incoming WhatsApp payload
    message = parse_incoming_message(incoming_payload)

    # message is expected to contain:
    # {
    #   "phone_number": "...",
    #   "message_text": "..."
    # }

    phone_number = message.get("phone_number")
    message_text = message.get("message_text")

    # Step 2: Create lead object from message using your existing service
    extracted_lead = create_lead_from_message(message)

    # Step 3: Find existing lead by phone number, otherwise create one
    db_lead = db.query(Lead).filter(Lead.phone_number == phone_number).first()

    if not db_lead:
        db_lead = Lead(
            phone_number=phone_number,
            property_type=extracted_lead.get("property_type"),
            location=extracted_lead.get("location"),
            budget=extracted_lead.get("budget"),
            timeline=extracted_lead.get("timeline"),
            status=extracted_lead.get("status", "NEW")
        )
        db.add(db_lead)
        db.commit()
        db.refresh(db_lead)
    else:
        # Only update fields if new values exist
        if extracted_lead.get("property_type"):
            db_lead.property_type = extracted_lead.get("property_type")
        if extracted_lead.get("location"):
            db_lead.location = extracted_lead.get("location")
        if extracted_lead.get("budget"):
            db_lead.budget = extracted_lead.get("budget")
        if extracted_lead.get("timeline"):
            db_lead.timeline = extracted_lead.get("timeline")
        if extracted_lead.get("status"):
            db_lead.status = extracted_lead.get("status")

        db.commit()
        db.refresh(db_lead)

    # Step 4: Save inbound message
    inbound_message = Message(
        lead_id=db_lead.id,
        direction="inbound",
        message_text=message_text,
        raw_payload=str(raw_payload)
    )
    db.add(inbound_message)
    db.commit()

    # Step 5: Decide what to ask next
    lead_for_question = {
        "phone_number": db_lead.phone_number,
        "property_type": db_lead.property_type,
        "location": db_lead.location,
        "budget": db_lead.budget,
        "timeline": db_lead.timeline,
        "status": db_lead.status
    }

    next_question = get_next_question(lead_for_question)

    # Step 6: Save outbound message
    outbound_message = Message(
        lead_id=db_lead.id,
        direction="outbound",
        message_text=next_question
    )
    db.add(outbound_message)
    db.commit()

    # Debug logs
    print("Incoming payload:", raw_payload)
    print("Parsed message:", message)
    print("Extracted lead:", extracted_lead)
    print("Saved DB lead ID:", db_lead.id)
    print("Next question:", next_question)

    return {
        "status": "received",
        "message": message,
        "lead": {
            "id": db_lead.id,
            "phone_number": db_lead.phone_number,
            "property_type": db_lead.property_type,
            "location": db_lead.location,
            "budget": db_lead.budget,
            "timeline": db_lead.timeline,
            "status": db_lead.status
        },
        "next_question": next_question
    }