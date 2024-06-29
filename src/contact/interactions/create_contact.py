from src.contact.models.contact import Contact
from src.libs.enums import LinkPrecedenceType

def create_contact(request):
    new_contact = Contact.create(
        email=request.get('email'),
        phoneNumber=request.get('phoneNumber'),
    )
    new_contact.save()
    return new_contact