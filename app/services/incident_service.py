# app/services/incident_service.py
from app.db.conn import get_db
from app.models.schemas import IncidentCreate

def _ensure_table(cur):
    # Crea la tabla si no existe (demo simple)
    # Incluye created_at para compatibilidad con init_db
    cur.execute(
        """
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
        """
    )

def registrar_incidente(data: IncidentCreate) -> dict:
    """
    Inserta un incidente y retorna el registro creado.
    """
    conn = get_db()
    cur = conn.cursor()
    _ensure_table(cur)

    cur.execute("""
        INSERT INTO incidentes (cargo_id, vehicle_id, employee_id, type, description, lat, lon)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data.cargo_id,
        data.vehicle_id,
        data.employee_id,
        data.type,
        data.description,
        data.location.lat,
        data.location.lon
    ))
    conn.commit()
    new_id = cur.lastrowid

    # Devuelve el registro recién creado
    cur.execute("SELECT id, cargo_id, vehicle_id, employee_id, type, description, lat, lon FROM incidentes WHERE id = ?", (new_id,))
    row = cur.fetchone()
    conn.close()

    return {
        "id": row["id"],
        "cargo_id": row["cargo_id"],
        "vehicle_id": row["vehicle_id"],
        "employee_id": row["employee_id"],
        "type": row["type"],
        "description": row["description"],
        "location": {"lat": row["lat"], "lon": row["lon"]},
        "status": "ok"
    }
