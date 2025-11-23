import sqlite3

print("\n" + "="*80)
print("  VERIFICACIÓN DE USUARIOS Y RESPONSABLES")
print("="*80)

# Base de datos principal
conn = sqlite3.connect("/app/inventario.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Ver estructura de la tabla users
print("\n📋 ESTRUCTURA DE LA TABLA USERS:")
cur.execute("PRAGMA table_info(users)")
columns = cur.fetchall()
for col in columns:
    print(f"  - {col['name']}: {col['type']}")

# Ver usuarios registrados
print("\n👤 USUARIOS REGISTRADOS:")
cur.execute("SELECT * FROM users")
users = cur.fetchall()
for user in users:
    print(f"\n  ID: {user['id']}")
    print(f"  Username: {user['username']}")
    print(f"  Nombre: {user['full_name']}")
    print(f"  Email: {user['email'] if 'email' in user.keys() else 'N/A'}")
    print(f"  Rol: {user['role']}")
    print(f"  RUT: {user['rut'] if user['rut'] else 'N/A'}")
    print(f"  Activo: {user['is_active']}")

# Ver estructura de la tabla responsables
print("\n" + "-"*80)
print("📋 ESTRUCTURA DE LA TABLA RESPONSABLES:")
cur.execute("PRAGMA table_info(responsables)")
columns = cur.fetchall()
for col in columns:
    print(f"  - {col['name']}: {col['type']}")

# Ver responsables registrados
print("\n👷 RESPONSABLES REGISTRADOS:")
cur.execute("SELECT * FROM responsables")
responsables = cur.fetchall()
for resp in responsables:
    print(f"\n  ID: {resp['id']}")
    print(f"  Nombre: {resp['nombre']}")
    print(f"  RUT: {resp['rut']}")
    print(f"  Teléfono: {resp['telefono'] if resp['telefono'] else 'N/A'}")
    print(f"  Email: {resp['email'] if resp['email'] else 'N/A'}")

# Ver asignaciones
print("\n" + "-"*80)
print("🚚 ASIGNACIONES ACTUALES:")
cur.execute("""
    SELECT a.*, r.nombre as responsable_nombre, r.rut as responsable_rut 
    FROM asignaciones a 
    LEFT JOIN responsables r ON a.responsable_id = r.id
""")
asignaciones = cur.fetchall()
for asig in asignaciones:
    print(f"\n  Cargo: {asig['cargo_id']}")
    print(f"  Responsable ID: {asig['responsable_id']}")
    print(f"  Responsable RUT: {asig['responsable_rut']}")
    print(f"  Responsable Nombre: {asig['responsable_nombre']}")

conn.close()
print("\n" + "="*80 + "\n")
