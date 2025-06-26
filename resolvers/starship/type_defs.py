from ariadne import ObjectType
from database import get_db_connection

starship_type = ObjectType("Starship")

@starship_type.field("pilots")
def resolve_starship_pilots(starship_obj, info):
    starship_id = starship_obj.get("id")
    conn = get_db_connection()
    try:
        characters = conn.execute(
            """
            SELECT c.id, c.name, c.species, c.home_planet_id
            FROM characters c
            JOIN character_starships cs ON c.id = cs.character_id
            WHERE cs.starship_id = ?
            """,
            (starship_id,),
        ).fetchall()
        return [dict(char) for char in characters]
    finally:
        conn.close()

@starship_type.field("appearsIn")
def resolve_starship_appears_in(starship_obj, info):
    starship_id = starship_obj.get("id")
    conn = get_db_connection()
    try:
        films = conn.execute(
            """
            SELECT f.id, f.title, f.episode_id, f.director, f.release_date, f.opening_crawl
            FROM films f
            JOIN film_starships fs ON f.id = fs.film_id
            WHERE fs.starship_id = ?
            """,
            (starship_id,),
        ).fetchall()
        return [dict(film) for film in films]
    finally:
        conn.close()