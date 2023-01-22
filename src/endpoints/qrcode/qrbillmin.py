from fastapi import APIRouter, Request, status, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
import secrets
from decouple import config
import os
import warnings
from qrbill import QRBill
from src.models.qrcode.qrbillmin import QRBillmin
from src.tools.submit_tasks import write_notification
from src.tools.read_config import read_configuration

import tempfile
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg

# Read yaml configuration file
configuration_file = read_configuration()

router = APIRouter(
    prefix=f"{config('BASE_URL')}" + configuration_file['CREATE_QRCODE_ROUTE'] + configuration_file['CREATE_QRBILLMIN_SUISSE_ROUTE'],
    responses={400: {"description": "Bad request"}},
    tags=['Suisse QRbill min Creator Parameters for Payment Slips']
)

@router.post("/{dtype}", status_code = status.HTTP_201_CREATED)
async def create_min_qrbill(qrbillmin: QRBillmin, dtype : str, request: Request, background_tasks: BackgroundTasks):
    """
    This function implements the router in order to receive 
    data and returns a qrbill svg with basic only parameters 
    in base64 format by using the library qrbill
    """
    # type of document to receive back
    document_type = dtype.upper()
    # convert request to dictionary
    qrbillmin_dictionary = dict(qrbillmin)

    # Create QRbill with received parameters
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  
    if not qrbillmin:
        warnings.warn("Warning: The basic object cannot be empty")
        message = "QRbill basic info cannot be empty"
        raise HTTPException(
            status_code=400, 
            detail=message, 
            headers={"content-type": "application/json"},
        )

    # check if there is a predefine image name
    if ('name' in qrbillmin_dictionary) and (qrbillmin_dictionary['name'] is not None):
        image_name = qrbillmin_dictionary['name']
    else:
        image_name = secrets.token_hex(15)

    if ('account' not in qrbillmin_dictionary) or ('creditor' not in qrbillmin_dictionary) or ('debtor' not in qrbillmin_dictionary):
        message = "QRbill account parameter, creditor or debtor objects not exist"
        raise HTTPException(
            status_code=400, 
            detail=message, 
            headers={"content-type": "application/json"},
        )

    account = qrbillmin_dictionary['account']
    creditor_dictionary = dict(qrbillmin_dictionary['creditor'])
    debtor_dictionary = dict(qrbillmin_dictionary['debtor'])

    creditor_name = creditor_dictionary['creditor_name']
    creditor_postalcode = creditor_dictionary['creditor_postalcode']
    creditor_city = creditor_dictionary['creditor_city']
    creditor_country = creditor_dictionary['creditor_country']
    creditor_street = creditor_dictionary['creditor_street']
    creditor_housenumber = creditor_dictionary['creditor_housenumber']

    debtor_name = debtor_dictionary['debtor_name']
    debtor_postalcode = debtor_dictionary['debtor_postalcode']
    debtor_city = debtor_dictionary['debtor_city']
    debtor_country = debtor_dictionary['debtor_country']
    debtor_street = debtor_dictionary['debtor_street']
    debtor_housenumber = debtor_dictionary['debtor_housenumber']

    if 'amount' not in qrbillmin_dictionary:
        message = "QRbill amount parameter does not exist"
        raise HTTPException(
            status_code=400, 
            detail=message, 
            headers={"content-type": "application/json"},
        )
    else:
        amount = qrbillmin_dictionary['amount']

    if 'currency' not in qrbillmin_dictionary:
        message = "QRbill currency parameter does not exist"
        raise HTTPException(
            status_code=400, 
            detail=message, 
            headers={"content-type": "application/json"},
        )
    else:
        currency = qrbillmin_dictionary['currency']

    if 'due_date' not in qrbillmin_dictionary:
        message = "QRbill due_date parameter does not exist"
        raise HTTPException(
            status_code=400, 
            detail=message, 
            headers={"content-type": "application/json"},
        )
    else:
        due_date = qrbillmin_dictionary['due_date']

    if 'reference_number' not in qrbillmin_dictionary:
        message = "QRbill reference_number parameter does not exist"
        raise HTTPException(
            status_code=400, 
            detail=message, 
            headers={"content-type": "application/json"},
        )
    else:
        reference_number = qrbillmin_dictionary['reference_number']

    if 'language' not in qrbillmin_dictionary:
        message = "QRbill language parameter does not exist"
        raise HTTPException(
            status_code=400, 
            detail=message, 
            headers={"content-type": "application/json"},
        )
    else:
        language = qrbillmin_dictionary['language']

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # Create main class for QRBill from module

    try:
        req_bill = QRBill(
            account = account,
            creditor = {
                'name': creditor_name, 'pcode': creditor_postalcode, 'street': creditor_street, 
                'house_num': creditor_housenumber, 'city': creditor_city, 'country': creditor_country,
            },
            debtor = {
                'name': debtor_name, 'pcode': debtor_postalcode, 'street': debtor_street, 
                'house_num': debtor_housenumber, 'city': debtor_city, 'country': debtor_country,
            },
            amount = amount,
            currency = currency,
            due_date = due_date,
            ref_number = reference_number,
            language = language,
            top_line=True, 
            payment_line=True,
            font_factor=1.0,
            )
    except ValueError as err:
        message = "QRBill did not create due to an error: " + str(err)
        raise HTTPException(
            status_code=501, 
            detail=message, 
            headers={"content-type": "application/json"},
        ) 

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    if document_type == 'PDF':

        format_type = configuration_file['PDF_FORMAT']
        fullname = configuration_file['PATH_DOCUMENTS'] + configuration_file['QR_PATH_SUISSE'] + '/' + image_name + format_type
        with tempfile.TemporaryFile(encoding='utf-8', mode='r+') as temp:
            req_bill.as_svg(temp, full_page=True) # A5=False
            temp.seek(0)
            drawing = svg2rlg(temp)
        renderPDF.drawToFile(drawing, fullname, autoSize=1)

    elif document_type == 'SVG':

        format_type = configuration_file['SVG_FORMAT']
        fullname = configuration_file['PATH_DOCUMENTS'] + configuration_file['QR_PATH_SUISSE'] + '/' + image_name + format_type
        req_bill.as_svg(fullname)

    elif document_type == 'PNG':

        format_type = configuration_file['IMG_FORMAT']
        fullname = configuration_file['PATH_DOCUMENTS'] + configuration_file['QR_PATH_SUISSE'] + '/' + image_name + format_type
        with tempfile.TemporaryFile(encoding='utf-8', mode='r+') as temp:
            req_bill.as_svg(temp, full_page=True)
            temp.seek(0)
            drawing = svg2rlg(temp)
        renderPDF.drawToFile(drawing, fullname, fmt='PNG')

    else:
        message = "Error occured in QRbill format"
        raise HTTPException(
            status_code=400, 
            detail=message, 
            headers={"content-type": "application/json"},
        )

    if (os.path.exists(fullname)):
        message = "QRBill file has been created as: " + document_type
        return FileResponse(fullname, media_type="application/pdf")
    else:
        message = "QRBill file has not been created"
        raise HTTPException(
            status_code=501, 
            detail=message, 
            headers={"content-type": "application/json"},
        )
     