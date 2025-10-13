from fastapi import APIRouter
from app.models.schemas import ConsultaSKU
from app.services.stock_service import consultar_stock_por_sku

router = APIRouter(prefix="/stock", tags=["stock"])

@router.post("/consultar")
def consultar_stock(body: ConsultaSKU):
    res = consultar_stock_por_sku(body.sku)
    return res or {"mensaje": f"No se encontró el SKU {body.sku}"}