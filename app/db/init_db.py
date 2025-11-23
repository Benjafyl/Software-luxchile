import sqlite3
from app.core.config import DB_PATH

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# --- Inventario (MVP Sprint 1)
cur.execute("""
CREATE TABLE IF NOT EXISTS inventario (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sku TEXT NOT NULL,
  bodega TEXT NOT NULL,
  stock INTEGER NOT NULL,
  estado TEXT NOT NULL
)
""")

# Datos de ejemplo - Solo 6 registros únicos (1 SKU por bodega)
cur.execute("DELETE FROM inventario")
cur.executemany(
    """
    INSERT INTO inventario (sku, bodega, stock, estado)
    VALUES (?, ?, ?, ?)
    """,
    [
        ("SKU001", "Bodega Central Santiago", 150, "DISPONIBLE"),
        ("SKU002", "Bodega Valparaíso", 230, "DISPONIBLE"),
        ("SKU003", "Bodega Concepción", 89, "DISPONIBLE"),
        ("SKU004", "Bodega Norte Antofagasta", 340, "DISPONIBLE"),
        ("SKU005", "Bodega Sur Temuco", 78, "DISPONIBLE"),
        ("SKU006", "Bodega Viña del Mar", 210, "DISPONIBLE"),
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
