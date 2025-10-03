import sqlite3

conn = sqlite3.connect("inventario.db")
cursor = conn.cursor()

# Crear tabla
cursor.execute("""
CREATE TABLE IF NOT EXISTS inventario (
    sku TEXT,
    bodega TEXT,
    stock INTEGER,
    stock_minimo INTEGER
)
""")

# Insertar datos de ejemplo
cursor.executemany("""
INSERT INTO inventario (sku, bodega, stock, stock_minimo)
VALUES (?, ?, ?, ?)
""", [
    ("SKU001", "Bodega Santiago", 50, 20),
    ("SKU001", "Bodega Viña del Mar", 10, 20),
    ("SKU002", "Bodega Santiago", 100, 30),
])

conn.commit()
conn.close()
print("Base de datos inicializada 🚀")
