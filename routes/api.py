from fastapi import APIRouter
from src.endpoints import home
from src.endpoints.qrcode import qrbillmin
from src.endpoints.barcode import barcode

router = APIRouter()
router.include_router(home.router)
router.include_router(qrbillmin.router) # Suisse QRBill Min Payment Slips
router.include_router(barcode.router) # Barcode image creation
