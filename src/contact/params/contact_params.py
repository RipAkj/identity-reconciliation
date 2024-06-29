from pydantic import BaseModel
from typing import Optional

class CreateContactRequest(BaseModel):
    phoneNumber: Optional[str] = None
    email: Optional[str] = None

class IdentifyRequest(BaseModel):
    email: Optional[str] = None
    phoneNumber: Optional[str] = None

class ContactResponse(BaseModel):
    primaryContactId: int 
    emails: list[str]
    phoneNumbers: list[str]
    secondaryContactIds: list[int] 

class IdentifyResponse(BaseModel):
    contact: ContactResponse
