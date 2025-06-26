from ariadne import ObjectType
from database import get_db_connection

film_type = ObjectType("Film")

@film_type.field("characters")
def resolve_film_characters(film_obj, info):
    film_id = film_obj.get("id")
    conn = get_db_connection()
    try:
        characters = conn.execute(
            """
            SELECT c.id, c.name, c.species, c.home_planet_id
            FROM characters c
            JOIN film_characters fc ON c.id = fc.character_id
            WHERE fc.film_id = ?
            """,
            (film_id,),
        ).fetchall()
        return [dict(char) for char in characters]
    finally:
        conn.close()

@film_type.field("planets")
def resolve_film_planets(film_obj, info):
    film_id = film_obj.get("id")
    conn = get_db_connection()
    try:
        planets = conn.execute(
            """
            SELECT p.id, p.name, p.climate, p.terrain
            FROM planets p
            JOIN film_planets fp ON p.id = fp.planet_id
            WHERE fp.film_id = ?
            """,
            (film_id,),
        ).fetchall()
        return [dict(planet) for planet in planets]
    finally:
        conn.close()

@film_type.field("starships")
def resolve_film_starships(film_obj, info):
    film_id = film_obj.get("id")
    conn = get_db_connection()
    try:
        starships = conn.execute(
            """
            SELECT s.id, s.name, s.model, s.manufacturer
            FROM starships s
            JOIN film_starships fs ON s.id = fs.starship_id
            WHERE fs.film_id = ?
            """,
            (film_id,),
        ).fetchall()
        return [dict(starship) for starship in starships]
    finally:
        conn.close()