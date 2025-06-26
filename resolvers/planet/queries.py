from database import get_db_connection

def register_planet_queries(query):
    @query.field("allPlanets")
    def resolve_all_planets(_, info):
        conn = get_db_connection()
        try:
            planets = conn.execute("SELECT id, name, climate, terrain FROM planets").fetchall()
            return [dict(p) for p in planets]
        finally:
            conn.close()

    @query.field("planet")
    def resolve_planet(_, info, id):
        conn = get_db_connection()
        try:
            planet = conn.execute("SELECT id, name, climate, terrain FROM planets WHERE id = ?", (id,)).fetchone()
            return dict(planet) if planet else None
        finally:
            conn.close()
