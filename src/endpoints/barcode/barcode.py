from fastapi import APIRouter, Request, status, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
import secrets
from decouple import config
import os
# import EAN13 from barcode module
from barcode import EAN13
# import ImageWriter to generate an image file
from barcode.writer import ImageWriter

from src.tools.submit_tasks import write_notification
from src.tools.read_config import read_configuration
from src.models.barcode.Barcode import BarcodeNumber

# Read yaml configuration file
configuration_file = read_configuration()

router = APIRouter(
    prefix=f"{config('BASE_URL')}" + configuration_file['CREATE_BARCODE_ROUTE'],
    responses={400: {"description": "Bad request"}},
    tags=['Barcode Creator Parameters EAN13, it includes 12 digits + 1 check digit and is used to encode GTIN-13']
)

@router.post("/number", status_code = status.HTTP_201_CREATED)
async def create_barcode_image_for_number(barcodeNumber: BarcodeNumber, request: Request, background_tasks: BackgroundTasks):
    """
    This function implements the router in order to receive 
    data and returns a barcode image
    """
    # convert request to dictionary
    barcode_dictionary = dict(barcodeNumber)
    # Make sure to pass the number as string
    if ('value' not in barcode_dictionary):
        message = "Barcode value objects not exist"
        raise HTTPException(
            status_code=400, 
            detail=message, 
            headers={"content-type": "application/json"},
        )
    number = barcode_dictionary['value']

    if ('name' in barcode_dictionary) and (barcode_dictionary['name'] is not None):
        barcode_name = barcode_dictionary['name']
    else:
        barcode_name = secrets.token_hex(15)

    format_type = configuration_file['IMG_FORMAT']
    fullname_no_ext = configuration_file('PATH_DOCUMENTS')
    fullname_no_ext += configuration_file('BARCODE_PATH') 
    fullname_no_ext += '/'
    fullname_no_ext += barcode_name

    # Create an object of EAN13 class and pass the number with the ImageWriter() as the writer
    my_code = EAN13(number, writer=ImageWriter())
    my_code.save(fullname_no_ext)
    fullname = fullname_no_ext 
    fullname += format_type

    if (os.path.exists(fullname)):
        return FileResponse(fullname, media_type="image/png")
    else:
        message = "Barcode image has not been created"
        raise HTTPException(
            status_code=501, 
            detail=message, 
            headers={"content-type": "application/json"},
        )