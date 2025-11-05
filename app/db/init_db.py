import sqlite3
from app.core.config import DB_PATH

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# --- Inventario (MVP Sprint 1)
cur.execute("""
CREATE TABLE IF NOT EXISTS inventario (
  sku TEXT,
  bodega TEXT,
  stock INTEGER,
  stock_minimo INTEGER
)
""")

# Datos de ejemplo (puedes quitarlos si no quieres resetear)
cur.execute("DELETE FROM inventario")
cur.executemany(
    """
    INSERT INTO inventario (sku, bodega, stock, stock_minimo)
    VALUES (?, ?, ?, ?)
    """,
    [
        # SKU001 - ejemplo mixto (OK y BAJO_STOCK)
        ("SKU001", "Bodega Santiago", 50, 20),
        ("SKU001", "Bodega Viña del Mar", 10, 20),  # BAJO_STOCK

        # SKU002 - disponibilidad amplia en dos bodegas
        ("SKU002", "Bodega Santiago", 100, 30),
        ("SKU002", "Bodega Concepción", 65, 25),

        # SKU003 - uno bajo, otro sobre mínimo
        ("SKU003", "Bodega Santiago", 5, 20),        # BAJO_STOCK
        ("SKU003", "Bodega Concepción", 24, 15),

        # SKU004 - presencia en norte y centro
        ("SKU004", "Bodega Antofagasta", 7, 10),     # BAJO_STOCK
        ("SKU004", "Bodega Viña del Mar", 50, 25),

        # SKU005 - stock alto y cero en sur
        ("SKU005", "Bodega Santiago", 120, 30),
        ("SKU005", "Bodega Puerto Montt", 0, 5),     # BAJO_STOCK
    ],
)

# --- Incidentes (Sprint 2)
cur.execute("""
CREATE TABLE IF NOT EXISTS incidentes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cargo_id TEXT,
  vehicle_id TEXT,
  employee_id TEXT,
  type TEXT,
  description TEXT,
  lat REAL,
  lon REAL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()
print("BD inicializada (inventario + incidentes) 🚀")
