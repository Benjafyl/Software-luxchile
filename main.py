from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel

app = FastAPI(title="API de Inventario LuxChile")

# Modelo para la consulta
class ConsultaSKU(BaseModel):
    sku: str

# Conexión a la base de datos
def get_db():
    conn = sqlite3.connect("inventario.db")
    conn.row_factory = sqlite3.Row
    return conn

# Endpoint para consultar stock en tiempo real
@app.post("/consultar_stock")
def consultar_stock(data: ConsultaSKU):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT bodega, stock, stock_minimo FROM inventario WHERE sku = ?", (data.sku,))
    resultados = cursor.fetchall()
    conn.close()

    if not resultados:
        return {"mensaje": f"No se encontró el SKU {data.sku}"}

    respuesta = []
    for fila in resultados:
        estado = "⚠️ Bajo stock" if fila["stock"] < fila["stock_minimo"] else "✅ Stock suficiente"
        respuesta.append({
            "bodega": fila["bodega"],
            "stock": fila["stock"],
            "estado": estado
        })

    return {"sku": data.sku, "inventario": respuesta}
