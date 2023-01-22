from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from decouple import config

router = APIRouter(
    prefix=f"{config('BASE_URL')}",
    tags=['Default']
)

@router.get("/home", response_class=HTMLResponse)
async def root():
    return """
        <html>
            <head>
                <title>QRA</title>
            </head>
            <body>
                <h3><i>QRCode Tool API</i></h3>
            </body>
        </html>
    """