import sqlite3

conn = sqlite3.connect('/app/data/inventario.db')
cur = conn.cursor()

# Consultar asignaciones completadas
cur.execute("""
    SELECT 
        COUNT(*) as total,
        SUM(CASE WHEN fecha_hora IS NULL THEN 1 ELSE 0 END) as on_time
    FROM asignaciones
    WHERE estado = 'COMPLETADA' AND fecha_completada IS NOT NULL
""")

row = cur.fetchone()
total = row[0]
on_time = row[1]

if total > 0:
    sla = (on_time / total * 100)
    print(f"Total completadas: {total}")
    print(f"Completadas a tiempo: {on_time}")
    print(f"SLA: {sla:.1f}%")
else:
    print("No hay asignaciones completadas")

conn.close()
