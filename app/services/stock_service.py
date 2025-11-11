# app/services/stock_service.py
from app.db.conn import get_db

def consultar_stock_sku(sku: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT bodega, stock, stock_minimo FROM inventario WHERE sku = ?", (sku,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return {"mensaje": f"No se encontró el SKU {sku}", "sku": sku, "inventario": []}

    respuesta = []
    for r in rows:
        estado = "BAJO_STOCK" if r["stock"] < r["stock_minimo"] else "OK"
        respuesta.append({"bodega": r["bodega"], "stock": r["stock"], "estado": estado})

    return {"sku": sku, "inventario": respuesta}
