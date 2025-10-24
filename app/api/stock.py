# app/api/stock.py
from fastapi import APIRouter
from app.models.schemas import ConsultaSKU
from app.services.stock_service import consultar_stock_sku

router = APIRouter()

@router.post("/consultar")
def consultar_stock(data: ConsultaSKU):
    return consultar_stock_sku(data.sku)
    