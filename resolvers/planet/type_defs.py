from ariadne import ObjectType
from database import get_db_connection

planet_type = ObjectType("Planet")

@planet_type.field("residents")
def resolve_planet_residents(planet_obj, info):
    planet_id = planet_obj.get("id")
    conn = get_db_connection()
    try:
        characters = conn.execute(
            "SELECT id, name, species, home_planet_id FROM characters WHERE home_planet_id = ?",
            (planet_id,),
        ).fetchall()
        return [dict(char) for char in characters]
    finally:
        conn.close()

@planet_type.field("appearsIn")
def resolve_planet_appears_in(planet_obj, info):
    planet_id = planet_obj.get("id")
    conn = get_db_connection()
    try:
        films = conn.execute(
            """
            SELECT f.id, f.title, f.episode_id, f.director, f.release_date, f.opening_crawl
            FROM films f
            JOIN film_planets fp ON f.id = fp.film_id
            WHERE fp.planet_id = ?
            """,
            (planet_id,),
        ).fetchall()
        return [dict(film) for film in films]
    finally:
        conn.close()