from src.contact.models.contact import Contact
from fastapi import HTTPException
from src.contact.interactions.create_contact import create_contact
from src.libs.enums import LinkPrecedenceType
from src.contact.params.contact_params import IdentifyResponse, ContactResponse
from fastapi.encoders import jsonable_encoder

def identify(request):
    with Contact._meta.database.atomic():
        try:
            identify_response = identify_helper(request)
            return identify_response
        except:
            raise

def identify_helper(request):
    email = request.get('email')
    phone_number = request.get('phoneNumber')
    if not email and not phone_number:
        raise HTTPException(status_code=400, detail="Both email and phoneNumber cannot be empty")
    
    query_conditions = []
    if email:
        query_conditions.append(Contact.email == email)
    if phone_number:
        query_conditions.append(Contact.phoneNumber == phone_number)

    combined_conditions = query_conditions[0]
    for condition in query_conditions[1:]:
        combined_conditions |= condition

    contacts = Contact.select().where(combined_conditions)
    email_entry, primary_email_contact = get_email_entries(contacts, email, request)
    phone_number_entry, primary_phone_contact = get_phone_number_entries(contacts, phone_number, request)

    ancestor = None

    if primary_phone_contact:
        ancestor = primary_phone_contact
    if primary_email_contact:
        ancestor = primary_email_contact
    if primary_email_contact and primary_phone_contact:
        if primary_email_contact.created_at < primary_phone_contact.created_at:
            ancestor = primary_email_contact
        else:
            ancestor = primary_phone_contact

    if ancestor and ancestor == primary_phone_contact:
        params = []
        
        for entry in email_entry:
            entry.linkedId = ancestor.id
            entry.linkPrecedence = LinkPrecedenceType.SECONDARY.value
            params.append(entry)
        Contact.bulk_update(model_list=email_entry,fields=[Contact.linkedId, Contact.linkPrecedence], batch_size=20)
    
    if ancestor and ancestor == primary_email_contact:
        params = []
        for entry in phone_number_entry:
            entry.linkedId = ancestor.id
            entry.linkPrecedence = LinkPrecedenceType.SECONDARY.value
            params.append(entry)
        Contact.bulk_update(model_list=phone_number_entry,fields=[Contact.linkedId, Contact.linkPrecedence],batch_size=20)

    if not ancestor:
        Contact.delete().where(Contact.id == email_entry[0].id)
        email_entry = []
        ancestor = phone_number_entry[0]
    identify_response = response_format(email_entry, phone_number_entry, ancestor)

    return identify_response

def get_email_entries(contacts, email, request):
    res = []
    primary_contact = None
    for contact in contacts:
        if contact.email == email:
            res.append(contact)
            if contact.linkPrecedence == LinkPrecedenceType.PRIMARY.value:
                primary_contact = contact
    
    if len(res) == 0:
        request = {
            'email': email,
            'phoneNumber': request.get('phoneNumber')
        }
        contact = create_contact(request)
        res.append(contact)

    return res, primary_contact

def get_phone_number_entries(contacts, phone_number, request):
    res = []
    primary_contact = None
    for contact in contacts:
        if contact.phoneNumber == phone_number:
            res.append(contact)
            if contact.linkPrecedence == LinkPrecedenceType.PRIMARY.value:
                primary_contact = contact
    
    if len(res) == 0:
        request = {
            'email': request.get('email'),
            'phoneNumber': phone_number
        }
        contact = create_contact(request)
        res.append(contact)

    return res, primary_contact

def get_set_emails(email_entry, phone_number_entry):
    emails = []
    for c in email_entry:
        emails.append(c.email)

    for c in phone_number_entry:
        emails.append(c.email)

    emails = list(set(emails))
    return emails

def get_set_phone_numbers(email_entry, phone_number_entry):
    phone_numbers = []
    for c in email_entry:
        phone_numbers.append(c.phoneNumber)

    for c in phone_number_entry:
        phone_numbers.append(c.phoneNumber)

    phone_numbers = list(set(phone_numbers))
    return phone_numbers

def get_set_secondary_ids(email_entry, phone_number_entry):
    seconary_ids = []
    for c in email_entry:
        seconary_ids.append(c.id)

    for c in phone_number_entry:
        seconary_ids.append(c.id)

    seconary_ids = list(set(seconary_ids))
    return seconary_ids

def response_format(email_entry, phone_number_entry, ancestor):
    result_emails = get_set_emails(email_entry, phone_number_entry)
    result_phones = get_set_phone_numbers(email_entry, phone_number_entry)
    result_secondary_ids = get_set_secondary_ids(email_entry, phone_number_entry)
    result_secondary_ids = [x for x in result_secondary_ids if x != ancestor.id]
    identify_response = IdentifyResponse(contact=ContactResponse(
        primaryContactId = ancestor.id,
        emails = result_emails,
        phoneNumbers = result_phones,
        secondaryContactIds = result_secondary_ids
    ))
    identify_response = jsonable_encoder(identify_response)
    return identify_response
    