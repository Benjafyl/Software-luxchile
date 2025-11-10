# app/api/stock.py
from fastapi import APIRouter, Depends
from app.models.schemas import ConsultaSKU
from app.services.stock_service import consultar_stock_sku
from app.core.security import require_role

router = APIRouter()

@router.post("/consultar")
def consultar_stock(data: ConsultaSKU, user=Depends(require_role("admin"))):
    return consultar_stock_sku(data.sku)
    
