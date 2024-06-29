from datetime import datetime
from libs.enums import LinkPrecedenceType
from database.base_model import BaseModel
from playhouse.postgres_ext import (
    BigAutoField,
    CharField,
    DateTimeField,
    BigIntegerField,
)
from fastapi import HTTPException

class Contact(BaseModel):
    id = BigAutoField(primary_key=True)
    phoneNumber = CharField(null=True, index = True)
    email = CharField(null=True, index = True)
    linkedId = BigIntegerField(null=True)
    linkPrecedence = CharField(default=LinkPrecedenceType.PRIMARY.value)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    deleted_at = DateTimeField(null = True)

    class Meta:
        table_name = "contacts"
 
    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        self.validate_linkPrecedence()
        return super(Contact, self).save(*args, **kwargs)
    
    def validate_linkPrecedence(self):
        if self.linkPrecedence not in LinkPrecedenceType._value2member_map_:
            raise HTTPException(status_code=400, detail="Invalid linkPrecedence")