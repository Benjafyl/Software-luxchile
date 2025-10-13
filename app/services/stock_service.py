from app.db.conn import get_db

def consultar_stock_por_sku(sku: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT bodega, stock, stock_minimo FROM inventario WHERE sku = ?",
        (sku,)
    )
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return None

    inventario = []
    for r in rows:
        estado = "BAJO_STOCK" if r["stock"] < r["stock_minimo"] else "OK"
        inventario.append({
            "bodega": r["bodega"],
            "stock": r["stock"],
            "estado": estado
        })
    return {"sku": sku, "inventario": inventario}
