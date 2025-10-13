from app.db.conn import get_db
from app.models.schemas import IncidentCreate

def create_incident(body: IncidentCreate) -> int:
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
      INSERT INTO incidentes (cargo_id, vehicle_id, employee_id, type, description, lat, lon)
      VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (body.cargo_id, body.vehicle_id, body.employee_id, body.type,
          body.description or "", body.location.lat, body.location.lon))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    # Notificación fake (para demo)
    print(f"[ALERTA] Incidente #{new_id} tipo={body.type} cargo={body.cargo_id}")
    return new_id
