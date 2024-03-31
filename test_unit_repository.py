import unittest
from unittest.mock import MagicMock

from sqlalchemy.sql import extract, expression, or_
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date
from src.schemas import ContactModel, ContactResponse, UpdateModel

from src.db.models import Contact, User
from src.schemas import UserDb, UserResponse, TokenModel, RequestEmail
from main import (
    get_contacts,
    get_contact,
    get_contact_by_name,
    get_contact_by_lastname,
    get_contact_by_emal,
    get_birthdays,
    create_contact,
    remove_contact,
    update_contact,
)


class TestQuotes(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)


    async def test_get_contact(self):
        contact = Contact()
        self.session.query().filter_by(id=1, user_id=1).first.return_value = contact
        result = await get_contact(contact_id=1, current_user=self.user, db=self.session)
        self.assertEqual(result, contact)


    async def test_get_contact_by_name(self):
        contact = Contact()
        self.session.query().filter_by(name="Ivan", user_id=1).first.return_value = contact
        result = await get_contact_by_name(nm="Ivan", current_user=self.user, db=self.session)
        self.assertEqual(result, contact)


    async def test_get_contact_by_lastname(self):
        contact = Contact()
        self.session.query().filter_by(lastname="Ivanoff", user_id=1).first.return_value = contact
        result = await get_contact_by_lastname(l_name="Ivanoff", current_user=self.user, db=self.session)
        self.assertEqual(result, contact)
    

    async def test_get_contact_by_email(self):
        contact = Contact()
        self.session.query().filter_by(email="ivanoff@example.com", user_id=1).first.return_value = contact
        result = await get_contact_by_emal(eml="ivanoff@example.com", current_user=self.user, db=self.session)
        self.assertEqual(result, contact)


    async def test_create_contact(self):
        body = ContactModel(name="Test", lastname="Test Lastname", email="test@test.com", phone="+123456789", birthday="2004-03-11", additional="no")
        contact = Contact (name = body.name, lastname = body.lastname, email = body.email,
                       phone = body.phone, birthday = body.birthday, additional = body.additional, user = self.user)
        contact.contact_date = datetime.now()
        result = await create_contact(body=body, current_user=self.user, db=self.session)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.lastname, body.lastname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.additional, body.additional)


    async def test_remove_contact(self):
        contact = Contact()
        self.session.query().filter_by(id=1, user_id = 1).first.return_value = contact
        result = await remove_contact(cont_id=1, current_user=self.user, db=self.session)
        self.assertEqual(result, contact)


    async def test_update_contact(self):
        body = UpdateModel(email="test@test.com", phone="+123456789", additional="no")
        contact = Contact (email = body.email, phone = body.phone, additional = body.additional, user = self.user)
        contact.contact_date = datetime.now()
        result = await update_contact(body=body, current_user=self.user, db=self.session)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.additional, body.additional)


"""
 
    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query(Contact).all == contacts
        result = await get_contacts(current_user=self.user, db=self.session)
        self.assertEqual(result, contacts)

        

    async def test_get_birthdays(self):

        today_doy = datetime.today().timetuple().tm_yday 
        days_per_year, leap_delta = (366, 1) if datetime.now().year%4 == 0 and datetime.now().year%400 == 0 else (365, 0)
        start_doy = today_doy + leap_delta
        next_doy = today_doy + 7

        if next_doy > days_per_year :
            start_doy = leap_delta
            next_doy -= days_per_year


        contacts = [Contact(), Contact(), Contact()]
        self.session.query(Contact).filter(or_(
        expression.between(extract('doy', Contact.birthday), start_doy, next_doy-1),
        expression.between(extract('doy', Contact.birthday), today_doy, today_doy+6),
        )).all() == contacts
        result = await get_birthdays(current_user=self.user, db=self.session)
        self.assertEqual(result, contacts)


"""


if __name__ == '__main__':
    unittest.main()

