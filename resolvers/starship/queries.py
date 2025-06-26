from database import get_db_connection

def register_starship_queries(query):
    @query.field("allStarships")
    def resolve_all_starships(_, info):
        conn = get_db_connection()
        try:
            starships = conn.execute("SELECT id, name, model, manufacturer FROM starships").fetchall()
            return [dict(s) for s in starships]
        finally:
            conn.close()

    @query.field("starship")
    def resolve_starship(_, info, id):
        conn = get_db_connection()
        try:
            starship = conn.execute("SELECT id, name, model, manufacturer FROM starships WHERE id = ?", (id,)).fetchone()
            return dict(starship) if starship else None
        finally:
            conn.close()
