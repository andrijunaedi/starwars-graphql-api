import sqlite3
from database import get_db_connection

def register_film_mutations(mutation):
    @mutation.field("createFilm")
    def resolve_create_film(_, info, input):
        conn = get_db_connection()
        try:
            conn.execute(
                """
                INSERT INTO films (title, episode_id, director, release_date, opening_crawl)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    input["title"],
                    input.get("episodeId"),
                    input.get("director"),
                    input.get("releaseDate"),
                    input.get("openingCrawl"),
                )
            )
            conn.commit()
            film_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            film = conn.execute(
                """
                SELECT id, title, episode_id, director, release_date, opening_crawl 
                FROM films WHERE id = ?
                """, 
                (film_id,)
            ).fetchone()
            return dict(film)
        except sqlite3.IntegrityError:
            conn.rollback()
            raise Exception(f"Film dengan judul '{input['title']}' atau episode ID {input.get('episodeId')} sudah ada.")
        finally:
            conn.close()
    
    @mutation.field("updateFilm")
    def resolve_update_film(_, info, input):
        conn = get_db_connection()
        try:
            film = conn.execute(
                "SELECT id, title, episode_id, director, release_date, opening_crawl FROM films WHERE id = ?", 
                (input["id"],)
            ).fetchone()
            if not film:
                raise Exception(f"Film dengan ID {input['id']} tidak ditemukan.")
                
            conn.execute(
                """
                UPDATE films 
                SET title = ?, episode_id = ?, director = ?, release_date = ?, opening_crawl = ?
                WHERE id = ?
                """,
                (
                    input.get("title", film["title"]),
                    input.get("episodeId", film["episode_id"]),
                    input.get("director", film["director"]),
                    input.get("releaseDate", film["release_date"]),
                    input.get("openingCrawl", film["opening_crawl"]),
                    input["id"],
                )
            )
            conn.commit()
            updated_film = conn.execute(
                """
                SELECT id, title, episode_id, director, release_date, opening_crawl 
                FROM films WHERE id = ?
                """, 
                (input["id"],)
            ).fetchone()
            return dict(updated_film)
        except sqlite3.IntegrityError:
            conn.rollback()
            raise Exception(f"Film dengan judul '{input.get('title')}' atau episode ID {input.get('episodeId')} sudah ada.")
        finally:
            conn.close()
    
    @mutation.field("deleteFilm")
    def resolve_delete_film(_, info, id):
        conn = get_db_connection()
        try:
            film = conn.execute("SELECT id FROM films WHERE id = ?", (id,)).fetchone()
            if not film:
                raise Exception(f"Film dengan ID {id} tidak ditemukan.")
            
            # Delete related records in junction tables
            conn.execute("DELETE FROM film_characters WHERE film_id = ?", (id,))
            conn.execute("DELETE FROM film_planets WHERE film_id = ?", (id,))
            conn.execute("DELETE FROM film_starships WHERE film_id = ?", (id,))
            
            # Delete the film
            conn.execute("DELETE FROM films WHERE id = ?", (id,))
            conn.commit()
            return True
        finally:
            conn.close()
            
    # Film relationship mutations
    @mutation.field("addCharacterToFilm")
    def resolve_add_character_to_film(_, info, input):
        conn = get_db_connection()
        try:
            film_id, character_id = input["filmId"], input["characterId"]
            
            # Check if film exists
            film = conn.execute("SELECT id FROM films WHERE id = ?", (film_id,)).fetchone()
            if not film:
                raise Exception(f"Film dengan ID {film_id} tidak ditemukan.")
            
            # Check if character exists
            character = conn.execute("SELECT id FROM characters WHERE id = ?", (character_id,)).fetchone()
            if not character:
                raise Exception(f"Karakter dengan ID {character_id} tidak ditemukan.")
                
            # Add relationship
            conn.execute(
                "INSERT OR IGNORE INTO film_characters (film_id, character_id) VALUES (?, ?)",
                (film_id, character_id)
            )
            conn.commit()
            
            # Return updated film
            film = conn.execute(
                "SELECT id, title, episode_id, director, release_date, opening_crawl FROM films WHERE id = ?", 
                (film_id,)
            ).fetchone()
            return dict(film)
        finally:
            conn.close()
    
    @mutation.field("removeCharacterFromFilm")
    def resolve_remove_character_from_film(_, info, input):
        conn = get_db_connection()
        try:
            film_id, character_id = input["filmId"], input["characterId"]
            
            # Check if film exists
            film = conn.execute("SELECT id FROM films WHERE id = ?", (film_id,)).fetchone()
            if not film:
                raise Exception(f"Film dengan ID {film_id} tidak ditemukan.")
            
            # Remove relationship
            conn.execute(
                "DELETE FROM film_characters WHERE film_id = ? AND character_id = ?",
                (film_id, character_id)
            )
            conn.commit()
            
            # Return updated film
            film = conn.execute(
                "SELECT id, title, episode_id, director, release_date, opening_crawl FROM films WHERE id = ?", 
                (film_id,)
            ).fetchone()
            return dict(film)
        finally:
            conn.close()
    
    @mutation.field("addPlanetToFilm")
    def resolve_add_planet_to_film(_, info, input):
        conn = get_db_connection()
        try:
            film_id, planet_id = input["filmId"], input["planetId"]
            
            # Check if film exists
            film = conn.execute("SELECT id FROM films WHERE id = ?", (film_id,)).fetchone()
            if not film:
                raise Exception(f"Film dengan ID {film_id} tidak ditemukan.")
            
            # Check if planet exists
            planet = conn.execute("SELECT id FROM planets WHERE id = ?", (planet_id,)).fetchone()
            if not planet:
                raise Exception(f"Planet dengan ID {planet_id} tidak ditemukan.")
                
            # Add relationship
            conn.execute(
                "INSERT OR IGNORE INTO film_planets (film_id, planet_id) VALUES (?, ?)",
                (film_id, planet_id)
            )
            conn.commit()
            
            # Return updated film
            film = conn.execute(
                "SELECT id, title, episode_id, director, release_date, opening_crawl FROM films WHERE id = ?", 
                (film_id,)
            ).fetchone()
            return dict(film)
        finally:
            conn.close()
    
    @mutation.field("removePlanetFromFilm")
    def resolve_remove_planet_from_film(_, info, input):
        conn = get_db_connection()
        try:
            film_id, planet_id = input["filmId"], input["planetId"]
            
            # Check if film exists
            film = conn.execute("SELECT id FROM films WHERE id = ?", (film_id,)).fetchone()
            if not film:
                raise Exception(f"Film dengan ID {film_id} tidak ditemukan.")
            
            # Remove relationship
            conn.execute(
                "DELETE FROM film_planets WHERE film_id = ? AND planet_id = ?",
                (film_id, planet_id)
            )
            conn.commit()
            
            # Return updated film
            film = conn.execute(
                "SELECT id, title, episode_id, director, release_date, opening_crawl FROM films WHERE id = ?", 
                (film_id,)
            ).fetchone()
            return dict(film)
        finally:
            conn.close()
    
    @mutation.field("addStarshipToFilm")
    def resolve_add_starship_to_film(_, info, input):
        conn = get_db_connection()
        try:
            film_id, starship_id = input["filmId"], input["starshipId"]
            
            # Check if film exists
            film = conn.execute("SELECT id FROM films WHERE id = ?", (film_id,)).fetchone()
            if not film:
                raise Exception(f"Film dengan ID {film_id} tidak ditemukan.")
            
            # Check if starship exists
            starship = conn.execute("SELECT id FROM starships WHERE id = ?", (starship_id,)).fetchone()
            if not starship:
                raise Exception(f"Kapal dengan ID {starship_id} tidak ditemukan.")
                
            # Add relationship
            conn.execute(
                "INSERT OR IGNORE INTO film_starships (film_id, starship_id) VALUES (?, ?)",
                (film_id, starship_id)
            )
            conn.commit()
            
            # Return updated film
            film = conn.execute(
                "SELECT id, title, episode_id, director, release_date, opening_crawl FROM films WHERE id = ?", 
                (film_id,)
            ).fetchone()
            return dict(film)
        finally:
            conn.close()
    
    @mutation.field("removeStarshipFromFilm")
    def resolve_remove_starship_from_film(_, info, input):
        conn = get_db_connection()
        try:
            film_id, starship_id = input["filmId"], input["starshipId"]
            
            # Check if film exists
            film = conn.execute("SELECT id FROM films WHERE id = ?", (film_id,)).fetchone()
            if not film:
                raise Exception(f"Film dengan ID {film_id} tidak ditemukan.")
            
            # Remove relationship
            conn.execute(
                "DELETE FROM film_starships WHERE film_id = ? AND starship_id = ?",
                (film_id, starship_id)
            )
            conn.commit()
            
            # Return updated film
            film = conn.execute(
                "SELECT id, title, episode_id, director, release_date, opening_crawl FROM films WHERE id = ?", 
                (film_id,)
            ).fetchone()
            return dict(film)
        finally:
            conn.close()