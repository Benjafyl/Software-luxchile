import sqlite3

conn = sqlite3.connect('/app/data/inventario.db')
cur = conn.cursor()

# Crear tabla de inventario si no existe
cur.execute('''
    CREATE TABLE IF NOT EXISTS inventario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sku TEXT NOT NULL,
        bodega TEXT NOT NULL,
        stock INTEGER NOT NULL,
        estado TEXT NOT NULL
    )
''')

# Limpiar datos anteriores (opcional)
cur.execute('DELETE FROM inventario')

# Insertar datos de prueba
datos_prueba = [
    ('SKU001', 'Bodega Central Santiago', 150, 'DISPONIBLE'),
    ('SKU001', 'Bodega Valparaíso', 45, 'DISPONIBLE'),
    ('SKU001', 'Bodega Concepción', 8, 'BAJO_STOCK'),
    ('SKU002', 'Bodega Central Santiago', 230, 'DISPONIBLE'),
    ('SKU002', 'Bodega Valparaíso', 120, 'DISPONIBLE'),
    ('SKU002', 'Bodega Concepción', 67, 'DISPONIBLE'),
    ('SKU003', 'Bodega Central Santiago', 5, 'BAJO_STOCK'),
    ('SKU003', 'Bodega Valparaíso', 89, 'DISPONIBLE'),
    ('SKU003', 'Bodega Concepción', 12, 'BAJO_STOCK'),
    ('SKU004', 'Bodega Central Santiago', 340, 'DISPONIBLE'),
    ('SKU004', 'Bodega Valparaíso', 180, 'DISPONIBLE'),
    ('SKU004', 'Bodega Concepción', 95, 'DISPONIBLE'),
    ('SKU005', 'Bodega Central Santiago', 78, 'DISPONIBLE'),
    ('SKU005', 'Bodega Valparaíso', 3, 'BAJO_STOCK'),
    ('SKU005', 'Bodega Concepción', 45, 'DISPONIBLE'),
    ('SKU006', 'Bodega Central Santiago', 210, 'DISPONIBLE'),
    ('SKU006', 'Bodega Valparaíso', 156, 'DISPONIBLE'),
    ('SKU006', 'Bodega Concepción', 89, 'DISPONIBLE'),
]

cur.executemany(
    'INSERT INTO inventario (sku, bodega, stock, estado) VALUES (?, ?, ?, ?)',
    datos_prueba
)

conn.commit()

# Verificar datos insertados
cur.execute('SELECT COUNT(*) FROM inventario')
total = cur.fetchone()[0]
print(f'✅ Datos de prueba insertados correctamente: {total} registros')

# Mostrar resumen por SKU
cur.execute('''
    SELECT sku, COUNT(*) as bodegas, SUM(stock) as total_stock
    FROM inventario
    GROUP BY sku
    ORDER BY sku
''')

print('\n📦 Resumen de inventario:')
for row in cur.fetchall():
    print(f'  {row[0]}: {row[1]} bodegas, Total stock: {row[2]}')

conn.close()
