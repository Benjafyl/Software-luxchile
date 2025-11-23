#!/usr/bin/env python3
"""
Script de inicialización de datos de prueba para el inventario.
Se ejecuta automáticamente al iniciar el backend si la BD está vacía.
"""
import sqlite3
import os

DB_PATH = os.getenv("DB_PATH", "/app/data/inventario.db")

def init_inventario():
    conn = sqlite3.connect(DB_PATH)
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
    
    # Verificar si ya hay datos
    cur.execute('SELECT COUNT(*) FROM inventario')
    if cur.fetchone()[0] > 0:
        print('ℹ️  Inventario ya tiene datos, omitiendo inicialización')
        conn.close()
        return
    
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
    print(f'✅ Inventario inicializado: {total} registros')
    
    conn.close()

if __name__ == '__main__':
    try:
        init_inventario()
    except Exception as e:
        print(f'❌ Error inicializando inventario: {e}')
