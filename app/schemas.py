from typing import Annotated, Optional, List
from annotated_types import Ge, Le
from pydantic import BaseModel, EmailStr, Field, StringConstraints, ConfigDict

NameStr = Annotated[str, StringConstraints(min_length=2, max_length=50)]
SurnameStr = Annotated[str, StringConstraints(min_length=2, max_length=50)]
phoneNoStr = Annotated[str, StringConstraints(min_length=10, max_length=12)]
booking_numberStr = Annotated[str, StringConstraints(min_length=2, max_length=50)]
nameOnCardStr = Annotated[str, StringConstraints(min_length=2, max_length=50)]
start_DateStr = Annotated[str, StringConstraints(min_length=2, max_length=50)]
end_DateStr = Annotated[str, StringConstraints(min_length=2, max_length=50)]
card_noStr = Annotated[str, StringConstraints(min_length=2, max_length=50)]
expiryStr = Annotated[str, StringConstraints(min_length=2, max_length=50)]
CVVStr = Annotated[str, StringConstraints(min_length=2, max_length=50)]
billing_addressStr = Annotated[str, StringConstraints(min_length=2, max_length=50)]

AgeInt = Annotated[int, Ge(0), Le(150)]




class UserCreate(BaseModel):
    first_name: NameStr
    surname: SurnameStr
    age: AgeInt
    email: EmailStr
    phoneNo: phoneNoStr
    booking_number: booking_numberStr

class UserRead(BaseModel):
    user_id: int
    first_name: NameStr
    surname: SurnameStr
    age: AgeInt
    email: EmailStr
    phoneNo: phoneNoStr
    booking_number: booking_numberStr

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    first_name: Optional[NameStr] = None
    surname: Optional[SurnameStr] = None
    age: Optional[AgeInt]= None
    email: Optional[EmailStr] = None
    phoneNo: Optional[phoneNoStr] = None
    booking_number: Optional[booking_numberStr] = None

class BookingCreate(BaseModel):
    booking_id: int
    first_name: NameStr
    surname: SurnameStr
    start_Date: start_DateStr
    end_Date: end_DateStr

class BookingRead(BaseModel):
    booking_id: int
    first_name: NameStr
    surname: SurnameStr
    start_Date: start_DateStr
    end_Date: end_DateStr

    model_config = ConfigDict(from_attributes=True)

class PaymentCreate(BaseModel):
    payment_id: int
    card_no: card_noStr
    expiry: expiryStr
    nameOnCard: nameOnCardStr
    CVV: CVVStr
    billing_address: billing_addressStr

class PaymentRead(BaseModel):
    payment_id: int
    card_no: card_noStr
    expiry: expiryStr
    nameOnCard: nameOnCardStr
    CVV: CVVStr
    billing_address: billing_addressStr

    model_config = ConfigDict(from_attributes=True)