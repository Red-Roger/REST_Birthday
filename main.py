from typing import List
from fastapi import FastAPI, Depends, HTTPException, status, Path
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from src.db.db import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.sql import extract, expression, or_
from src.db.models import Contact, User
from src.schemas import ContactModel, ContactResponse, UpdateModel
from datetime import datetime, timedelta, date
from src.routes import auth
from src.routes import users
from src.services.auth import auth_service
import redis.asyncio as redis
from src.conf.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = [ 
    "http://localhost:3000"
    ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')

@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")

@app.get("/contacts", response_model = List[ContactResponse], tags = ['contacts'])
async def get_contacts(current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contacts = db.query(Contact).filter(Contact.user_id == current_user.id)
    return contacts

@app.get("/contacts/{contact_id}", response_model = ContactResponse, tags = ['contacts'])
async def get_contact(contact_id: int = Path(ge = 1), current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(id=contact_id, user_id = current_user.id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact

@app.get("/contacts/name/{nm}", response_model = ContactResponse, tags = ['contacts'])
async def get_contact_by_name(nm: str = Path(),  current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(name=nm, user_id = current_user.id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact

@app.get("/contacts/lastname/{l_name}", response_model = ContactResponse, tags = ['contacts'])
async def get_contact_by_lastname(l_name: str = Path(), current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(lastname=l_name, user_id = current_user.id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact

@app.get("/contacts/email/{eml}", response_model = ContactResponse, tags = ['contacts'])
async def get_contact_by_emal(eml: str = Path(), current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(email=eml, user_id = current_user.id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact

@app.get("/birthdays", response_model = List[ContactResponse], tags = ['contacts'])
async def get_birthdays(current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    
    today_doy = datetime.today().timetuple().tm_yday 
    days_per_year, leap_delta = (366, 1) if datetime.now().year%4 == 0 and datetime.now().year%400 == 0 else (365, 0)
    start_doy = today_doy + leap_delta
    next_doy = today_doy + 7

    if next_doy > days_per_year :
        start_doy = leap_delta
        next_doy -= days_per_year

    contacts = db.query(Contact).filter(or_(
        expression.between(extract('doy', Contact.birthday), start_doy, next_doy-1),
        expression.between(extract('doy', Contact.birthday), today_doy, today_doy+6),
        )).all()
    return contacts

@app.post("/contacts", response_model = ContactResponse, tags = ['contacts'])
async def create_contact(body: ContactModel, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = Contact (name = body.name, lastname = body.lastname, email = body.email,
                       phone = body.phone, birthday = body.birthday, additional = body.additional, user = current_user)
    contact.contact_date = datetime.now()
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

@app.delete("/contacts/{cont_id}", status_code=status.HTTP_204_NO_CONTENT, tags = ['contacts'])
async def remove_contact(cont_id: int = Path(ge = 1), current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(id=cont_id, user_id = current_user.id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    db.delete(contact)
    db.commit()
    return contact

@app.patch("/contacts/{cont_id}/update", response_model = UpdateModel, tags = ['contacts'])
async def update_contact(body: UpdateModel, cont_id: int = Path(ge = 1), current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = db.query(Contact).filter_by(id=cont_id, user_id = current_user.id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    contact.email = body.email
    contact.phone = body.phone
    contact.additional = body.additional
    contact.contact_date = datetime.now()
    db.commit()
    return contact
