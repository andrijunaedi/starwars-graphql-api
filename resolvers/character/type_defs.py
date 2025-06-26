from ariadne import ObjectType
from database import get_db_connection

character_type = ObjectType("Character")

@character_type.field("homePlanet")
def resolve_character_home_planet(character_obj, info):
    home_planet_id = character_obj.get("home_planet_id")
    if not home_planet_id:
        return None
    conn = get_db_connection()
    try:
        planet = conn.execute("SELECT id, name, climate, terrain FROM planets WHERE id = ?", (home_planet_id,)).fetchone()
        return dict(planet) if planet else None
    finally:
        conn.close()

@character_type.field("pilotedStarships")
def resolve_character_piloted_starships(character_obj, info):
    character_id = character_obj.get("id")
    conn = get_db_connection()
    try:
        starships = conn.execute(
            """
            SELECT s.id, s.name, s.model, s.manufacturer
            FROM starships s
            JOIN character_starships cs ON s.id = cs.starship_id
            WHERE cs.character_id = ?
            """,
            (character_id,),
        ).fetchall()
        return [dict(s) for s in starships]
    finally:
        conn.close()

@character_type.field("appearsIn")
def resolve_character_appears_in(character_obj, info):
    character_id = character_obj.get("id")
    conn = get_db_connection()
    try:
        films = conn.execute(
            """
            SELECT f.id, f.title, f.episode_id, f.director, f.release_date, f.opening_crawl
            FROM films f
            JOIN film_characters fc ON f.id = fc.film_id
            WHERE fc.character_id = ?
            """,
            (character_id,),
        ).fetchall()
        return [dict(film) for film in films]
    finally:
        conn.close()