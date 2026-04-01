from sqlalchemy import Column, Integer, String, Text, ForeignKey
from backend.database.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    direction = Column(String)
    message_text = Column(Text)
    raw_payload = Column(Text, nullable=True)