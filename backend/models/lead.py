from sqlalchemy import Column, Integer, String
from backend.database.database import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)

    phone_number = Column(String, index=True)
    property_type = Column(String)
    location = Column(String)
    budget = Column(String)
    timeline = Column(String)

    status = Column(String, default="NEW")