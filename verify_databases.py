import sqlite3
import os

print("\n" + "="*70)
print("  VERIFICACIÓN DE BASES DE DATOS SQLite")
print("="*70)

# Verificar ambas bases de datos
databases = [
    "/app/inventario.db",
    "/app/data/inventario.db"
]

for db_path in databases:
    if os.path.exists(db_path):
        print(f"\n📁 Base de datos: {db_path}")
        print(f"   Tamaño: {os.path.getsize(db_path) / 1024:.2f} KB")
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Obtener lista de tablas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            if tables:
                print(f"   Tablas encontradas ({len(tables)}):")
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    print(f"      - {table_name}: {count} registros")
            else:
                print("   ⚠️  No hay tablas en esta base de datos")
            
            conn.close()
        except Exception as e:
            print(f"   ❌ Error al leer: {e}")
    else:
        print(f"\n📁 Base de datos: {db_path}")
        print(f"   ❌ No existe")

print("\n" + "="*70)
print("  FIN DE LA VERIFICACIÓN")
print("="*70 + "\n")
