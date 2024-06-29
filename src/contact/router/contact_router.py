from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from fastapi.responses import JSONResponse, ORJSONResponse
from fastapi.encoders import jsonable_encoder
from src.contact.params.contact_params import *
from src.contact.interactions.create_contact import create_contact
from src.contact.interactions.identify import identify
from traceback import format_exc
contact_router = APIRouter()


@contact_router.post('/create_contact')
def create_contact_api(
        request: CreateContactRequest
):
    """API to create contact """
    try:
        data = create_contact(request.model_dump(exclude_none=True))
        data = jsonable_encoder(data)['__data__']
        return JSONResponse(status_code=201, content=jsonable_encoder(data))
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        return JSONResponse(status_code=500, content={'success': False, "error": str(e), "traceback": format_exc()})
    
    
@contact_router.post('/identify')
def identify_api(
        request: IdentifyRequest
):
    """API to identify and keep track of a customer's identity across multiple purchases. """
    try:
        data = identify(request.model_dump(exclude_none=True))
        return JSONResponse(status_code=200, content=jsonable_encoder(data))
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        return JSONResponse(status_code=500, content={'success': False, "error": str(e), "traceback": format_exc()})