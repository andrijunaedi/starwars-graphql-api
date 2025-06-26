from database import get_db_connection

def register_character_queries(query):
    @query.field("allCharacters")
    def resolve_all_characters(_, info):
        conn = get_db_connection()
        try:
            characters = conn.execute("SELECT id, name, species, home_planet_id FROM characters").fetchall()
            return [dict(char) for char in characters]
        finally:
            conn.close()

    @query.field("character")
    def resolve_character(_, info, id):
        conn = get_db_connection()
        try:
            character = conn.execute("SELECT id, name, species, home_planet_id FROM characters WHERE id = ?", (id,)).fetchone()
            return dict(character) if character else None
        finally:
            conn.close()