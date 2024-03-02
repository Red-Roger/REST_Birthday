from sqlalchemy import Column, Integer, String, DateTime, Date
from src.db.db import Base, engine


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    lastname = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    birthday = Column(Date)
    additional = Column(String)
    contact_date = Column(DateTime)
    
Base.metadata.create_all(bind=engine)