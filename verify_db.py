import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('/app/data/inventario.db')
cursor = conn.cursor()

# Listar todas las tablas
print('\n' + '='*60)
print('  TABLAS EN LA BASE DE DATOS')
print('='*60)
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
for table in tables:
    print(f'  - {table[0]}')

# Verificar usuarios
print('\n' + '='*60)
print('  DATOS DE LA TABLA: users')
print('='*60)
try:
    cursor.execute('SELECT id, username, role, rut, full_name FROM users')
    users = cursor.fetchall()
    
    if users:
        for u in users:
            print(f'\nID: {u[0]}')
            print(f'Usuario: {u[1]}')
            print(f'Rol: {u[2]}')
            print(f'RUT: {u[3] if u[3] else "N/A"}')
            print(f'Nombre: {u[4] if u[4] else "N/A"}')
    else:
        print('\nNo hay usuarios registrados.')
except Exception as e:
    print(f'\nError al consultar usuarios: {e}')

# Verificar asignaciones
print('\n' + '='*60)
print('  DATOS DE LA TABLA: asignaciones')
print('='*60)
try:
    cursor.execute('SELECT id, cargo_id, vehicle_id, origen, destino, responsable_id FROM asignaciones LIMIT 5')
    asignaciones = cursor.fetchall()
    
    if asignaciones:
        for a in asignaciones:
            print(f'\nID: {a[0]}')
            print(f'Carga: {a[1]}')
            print(f'Vehículo: {a[2]}')
            print(f'Origen: {a[3]}')
            print(f'Destino: {a[4]}')
            print(f'Responsable ID: {a[5]}')
    else:
        print('\nNo hay asignaciones registradas.')
except Exception as e:
    print(f'\nError al consultar asignaciones: {e}')

# Verificar responsables
print('\n' + '='*60)
print('  DATOS DE LA TABLA: responsables')
print('='*60)
try:
    cursor.execute('SELECT id, nombre, rut, telefono FROM responsables')
    responsables = cursor.fetchall()
    
    if responsables:
        for r in responsables:
            print(f'\nID: {r[0]}')
            print(f'Nombre: {r[1] if r[1] else "N/A"}')
            print(f'RUT: {r[2]}')
            print(f'Teléfono: {r[3] if r[3] else "N/A"}')
    else:
        print('\nNo hay responsables registrados.')
except Exception as e:
    print(f'\nError al consultar responsables: {e}')

print('\n' + '='*60)
conn.close()
