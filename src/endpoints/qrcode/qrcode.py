from fastapi import APIRouter, Request, status, HTTPException
import qrcode
from PIL import Image # pip install pillow
import secrets
from decouple import config
from tools.convert import get_base64_encoded_image, get_image_decoded_base64
from models.qrcode import QRData
from tools.logging import qlogging


generate_router = APIRouter(
    prefix=f"{config('API_URL')}",
    tags=['QRCode Generator']
)


@generate_router.post("/generate/encode/base64", status_code = status.HTTP_201_CREATED)
async def encode64(qrdata: QRData, request: Request):
    """
    This function implements the router in order to receive 
    data and returns a qrcode image in base64 format
    """

    if not qrdata or not qrdata.data:
        message = "QRData cannot be empty"
        await qlogging("error", str(request.url), str(request.client), str(dict(request.headers)), "400", message)
        raise HTTPException(
            status_code=400, 
            detail=message, 
            headers={"content-type": "application/json"},
        )

    qrdata_dict = qrdata.data
    qrdata_content = ''

    for item in qrdata_dict:
        _data = str(qrdata_dict[item])
        qrdata_content = " ".join([qrdata_content, _data])

    # check if there is a predefine image name
    if qrdata.name:
        image_name = qrdata.name + f"{config('IMG_FORMAT')}"
    else:
        image_name = secrets.token_hex(15) + f"{config('IMG_FORMAT')}"

    fullname = f"{config('QR_PATH_IMAGE')}" + image_name

    #Creating an instance of qrcode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=f"{config('BOX_SIZE')}",
        border=f"{config('BORDER_SIZE')}",
    )

    qr.add_data(qrdata_content)
    qr.make(fit=True)

    img = qr.make_image(fill=f"{config('FILL_COLOR')}", back_color=f"{config('BACK_COLOR')}").convert('RGB')

        # check if a log should be added
    if qrdata.logo64:
        full_name = f"{config('QR_PATH_LOGO')}" + secrets.token_hex(15) + f"{config('IMG_FORMAT')}"
        await get_image_decoded_base64(full_name)
        logo_display = Image.open(full_name)
        logo_display.thumbnail((f"{config('LOGO_X')}", f"{config('LOGO_Y')}"))
        logo_pos = ((img.size[0] - logo_display.size[0]) // 2, (img.size[1] - logo_display.size[1]) // 2)
        img.paste(logo_display, logo_pos)

    img.save(fullname)

    res = await get_base64_encoded_image(fullname)
    message = "QRCode has been created: " + image_name
    await qlogging("access", str(request.url), str(request.client), str(dict(request.headers)), "201", message)

    return {"name": image_name, "content": res}
