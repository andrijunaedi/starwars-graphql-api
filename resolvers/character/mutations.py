import sqlite3
from database import get_db_connection

def register_character_mutations(mutation):
    @mutation.field("createCharacter")
    def resolve_create_character(_, info, input):
        conn = get_db_connection()
        try:
            if input.get("homePlanetId"):
                planet = conn.execute("SELECT id FROM planets WHERE id = ?", (input["homePlanetId"],)).fetchone()
                if not planet:
                    raise Exception(f"Planet dengan ID {input['homePlanetId']} tidak ditemukan.")
            conn.execute(
                "INSERT INTO characters (name, species, home_planet_id) VALUES (?, ?, ?)",
                (input["name"], input.get("species"), input.get("homePlanetId")),
            )
            conn.commit()
            char_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            character = conn.execute(
                "SELECT id, name, species, home_planet_id FROM characters WHERE id = ?", (char_id,)
            ).fetchone()
            return dict(character)
        except sqlite3.IntegrityError:
            conn.rollback()
            raise Exception(f"Karakter '{input['name']}' sudah ada.")
        finally:
            conn.close()

    @mutation.field("updateCharacter")
    def resolve_update_character(_, info, input):
        conn = get_db_connection()
        try:
            character = conn.execute("SELECT id, name, species, home_planet_id FROM characters WHERE id = ?", (input["id"],)).fetchone()
            if not character:
                raise Exception(f"Karakter dengan ID {input['id']} tidak ditemukan.")
            if input.get("homePlanetId"):
                planet = conn.execute("SELECT id FROM planets WHERE id = ?", (input["homePlanetId"],)).fetchone()
                if not planet:
                    raise Exception(f"Planet dengan ID {input['homePlanetId']} tidak ditemukan.")
            conn.execute(
                "UPDATE characters SET name = ?, species = ?, home_planet_id = ? WHERE id = ?",
                (
                    input.get("name", character["name"]),
                    input.get("species", character["species"]),
                    input.get("homePlanetId", character["home_planet_id"]),
                    input["id"],
                ),
            )
            conn.commit()
            updated_character = conn.execute(
                "SELECT id, name, species, home_planet_id FROM characters WHERE id = ?", (input["id"],)
            ).fetchone()
            return dict(updated_character)
        except sqlite3.IntegrityError:
            conn.rollback()
            raise Exception(f"Karakter '{input['name']}' sudah ada.")
        finally:
            conn.close()
    
    @mutation.field("deleteCharacter")
    def resolve_delete_character(_, info, id):
        conn = get_db_connection()
        try:
            character = conn.execute("SELECT id FROM characters WHERE id = ?", (id,)).fetchone()
            if not character:
                raise Exception(f"Karakter dengan ID {id} tidak ditemukan.")
            starship_count = conn.execute(
                "SELECT COUNT(*) FROM character_starships WHERE character_id = ?", (id,)
            ).fetchone()[0]
            if starship_count > 0:
                raise Exception(f"Tidak dapat menghapus karakter yang memiliki {starship_count} kapal.")
            conn.execute("DELETE FROM characters WHERE id = ?", (id,))
            conn.commit()
            return True
        finally:
            conn.close()
    
    @mutation.field("assignStarship")
    def resolve_assign_starship(_, info, input):
        conn = get_db_connection()
        try:
            character = conn.execute("SELECT id FROM characters WHERE id = ?", (input["characterId"],)).fetchone()
            starship = conn.execute("SELECT id FROM starships WHERE id = ?", (input["starshipId"],)).fetchone()
            if not character:
                raise Exception(f"Karakter dengan ID {input['characterId']} tidak ditemukan.")
            if not starship:
                raise Exception(f"Kapal dengan ID {input['starshipId']} tidak ditemukan.")
            conn.execute(
                "INSERT OR IGNORE INTO character_starships (character_id, starship_id) VALUES (?, ?)",
                (input["characterId"], input["starshipId"]),
            )
            conn.commit()
            character = conn.execute(
                "SELECT id, name, species, home_planet_id FROM characters WHERE id = ?",
                (input["characterId"],),
            ).fetchone()
            return dict(character)
        finally:
            conn.close()