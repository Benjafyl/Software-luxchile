# app/services/stock_service.py
from app.db.conn import get_db

def consultar_stock_sku(sku: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT bodega, stock, estado FROM inventario WHERE sku = ?", (sku,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return {"mensaje": f"No se encontró el SKU {sku}", "sku": sku, "inventario": []}

    respuesta = []
    for r in rows:
        respuesta.append({"bodega": r["bodega"], "stock": r["stock"], "estado": r["estado"]})

    return {"sku": sku, "inventario": respuesta}


def obtener_listado_stock(bodega: str | None = None, bajo_stock: bool | None = None, search: str | None = None):
    """
    Obtiene el listado completo de inventario con filtros opcionales.
    
    Args:
        bodega: Filtrar por bodega específica
        bajo_stock: Si es True, retorna solo items con estado BAJO_STOCK
        search: Buscar por SKU o nombre del producto
    
    Returns:
        Dict con el listado de items del inventario
    """
    conn = get_db()
    cursor = conn.cursor()
    
    # Construir query SQL con filtros dinámicos
    query = "SELECT sku, bodega, stock, estado FROM inventario WHERE 1=1"
    params = []
    
    if bodega:
        query += " AND bodega = ?"
        params.append(bodega)
    
    if bajo_stock:
        query += " AND estado = 'BAJO_STOCK'"
    
    if search:
        query += " AND (sku LIKE ? OR bodega LIKE ?)"
        search_pattern = f"%{search}%"
        params.extend([search_pattern, search_pattern])
    
    query += " ORDER BY sku, bodega"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    # También obtener lista de bodegas únicas para filtros
    cursor.execute("SELECT DISTINCT bodega FROM inventario ORDER BY bodega")
    bodegas = [row["bodega"] for row in cursor.fetchall()]
    
    conn.close()
    
    # Formatear respuesta
    items = []
    total_items = 0
    total_stock = 0
    items_bajo_stock = 0
    
    for r in rows:
        items.append({
            "sku": r["sku"],
            "bodega": r["bodega"],
            "stock": r["stock"],
            "estado": r["estado"]
        })
        total_stock += r["stock"]
        total_items += 1
        if r["estado"] == "BAJO_STOCK":
            items_bajo_stock += 1
    
    return {
        "items": items,
        "total_items": total_items,
        "total_stock": total_stock,
        "items_bajo_stock": items_bajo_stock,
        "bodegas_disponibles": bodegas
    }
