import sqlite3

conn = sqlite3.connect('/app/data/inventario.db')
cur = conn.cursor()

rows = cur.execute('''
    SELECT id, cargo_id, fecha_hora, fecha_completada 
    FROM asignaciones 
    WHERE estado = "COMPLETADA"
''').fetchall()

print("Asignaciones completadas:")
for r in rows:
    print(f"ID: {r[0]}, Cargo: {r[1]}")
    print(f"  Programada: {r[2]}")
    print(f"  Completada: {r[3]}")
    print()

conn.close()
