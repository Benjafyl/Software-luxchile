# app/api/stock.py
from fastapi import APIRouter, Depends, Query
from app.models.schemas import ConsultaSKU
from app.services.stock_service import consultar_stock_sku, obtener_listado_stock
from app.core.security import require_role

router = APIRouter()

@router.post("/consultar")
def consultar_stock(data: ConsultaSKU, user=Depends(require_role("admin"))):
    return consultar_stock_sku(data.sku)

@router.get("/listado")
def listar_stock(
    bodega: str | None = Query(None, description="Filtrar por bodega específica"),
    bajo_stock: bool | None = Query(None, description="Filtrar solo items con bajo stock"),
    search: str | None = Query(None, description="Buscar por SKU o nombre"),
    user=Depends(require_role("admin"))
):
    """
    Retorna el listado completo de inventario con filtros opcionales.
    """
    return obtener_listado_stock(bodega=bodega, bajo_stock=bajo_stock, search=search)
    
