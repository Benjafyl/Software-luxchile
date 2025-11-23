import sqlite3
from datetime import datetime

print("\n" + "="*80)
print("  VERIFICACIÓN DE DATOS REGISTRADOS")
print("="*80)

# Base de datos principal (usuarios, asignaciones, responsables)
print("\n📦 BASE DE DATOS PRINCIPAL: /app/inventario.db")
print("-" * 80)

conn1 = sqlite3.connect("/app/inventario.db")
conn1.row_factory = sqlite3.Row
cur1 = conn1.cursor()

# Verificar ASIGNACIONES
print("\n🚚 ASIGNACIONES REGISTRADAS:")
cur1.execute("SELECT * FROM asignaciones")
asignaciones = cur1.fetchall()

if asignaciones:
    for idx, asig in enumerate(asignaciones, 1):
        print(f"\n  [{idx}] Asignación ID: {asig['id']}")
        print(f"      Cargo ID: {asig['cargo_id']}")
        print(f"      Vehículo: {asig['vehicle_id']}")
        print(f"      Prioridad: {asig['prioridad']}")
        print(f"      Origen: {asig['origen']}")
        print(f"      Destino: {asig['destino']}")
        print(f"      Responsable ID: {asig['responsable_id']}")
        if asig['fecha_hora']:
            print(f"      Fecha/Hora: {asig['fecha_hora']}")
        if asig['notas']:
            print(f"      Notas: {asig['notas']}")
else:
    print("  ⚠️  No hay asignaciones registradas")

# Verificar RESPONSABLES
print("\n👤 RESPONSABLES REGISTRADOS:")
cur1.execute("SELECT * FROM responsables")
responsables = cur1.fetchall()

if responsables:
    for idx, resp in enumerate(responsables, 1):
        print(f"\n  [{idx}] Responsable ID: {resp['id']}")
        print(f"      Nombre: {resp['nombre']}")
        print(f"      RUT: {resp['rut']}")
        if resp['telefono']:
            print(f"      Teléfono: {resp['telefono']}")
        if resp['email']:
            print(f"      Email: {resp['email']}")
else:
    print("  ⚠️  No hay responsables registrados")

conn1.close()

# Base de datos operacional (incidentes, rutas)
print("\n" + "-" * 80)
print("📦 BASE DE DATOS OPERACIONAL: /app/data/inventario.db")
print("-" * 80)

conn2 = sqlite3.connect("/app/data/inventario.db")
conn2.row_factory = sqlite3.Row
cur2 = conn2.cursor()

# Verificar INCIDENTES
print("\n🚨 INCIDENTES REGISTRADOS:")
cur2.execute("SELECT * FROM incidentes")
incidentes = cur2.fetchall()

if incidentes:
    for idx, inc in enumerate(incidentes, 1):
        print(f"\n  [{idx}] Incidente ID: {inc['id']}")
        print(f"      Cargo ID: {inc['cargo_id']}")
        print(f"      Vehículo: {inc['vehicle_id']}")
        print(f"      RUT Empleado: {inc['employee_id']}")
        print(f"      Tipo: {inc['type']}")
        print(f"      Descripción: {inc['description']}")
        print(f"      Ubicación: Lat {inc['lat']}, Lon {inc['lon']}")
        if inc['created_at']:
            print(f"      Fecha/Hora: {inc['created_at']}")
else:
    print("  ⚠️  No hay incidentes registrados")

# Verificar HISTORIAL DE RUTAS
print("\n🗺️  HISTORIAL DE RUTAS:")
cur2.execute("SELECT * FROM route_history")
rutas = cur2.fetchall()

if rutas:
    for idx, ruta in enumerate(rutas, 1):
        print(f"\n  [{idx}] Ruta ID: {ruta['id']}")
        print(f"      Distancia: {ruta['distance_km']} km")
        print(f"      Duración: {ruta['duration_min']}")
        print(f"      Peajes: ${ruta['toll_cost']}")
        print(f"      Riesgo: {ruta['risk_score']}")
else:
    print("  ⚠️  No hay rutas en el historial")

conn2.close()

print("\n" + "="*80)
print("  RESUMEN")
print("="*80)
print(f"  • Asignaciones: {len(asignaciones)}")
print(f"  • Responsables: {len(responsables)}")
print(f"  • Incidentes: {len(incidentes)}")
print(f"  • Rutas: {len(rutas)}")
print("="*80 + "\n")
