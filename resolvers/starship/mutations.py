import sqlite3
from database import get_db_connection

def register_starship_mutations(mutation):
    @mutation.field("createStarship")
    def resolve_create_starship(_, info, input):
        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO starships (name, model, manufacturer) VALUES (?, ?, ?)",
                (input["name"], input.get("model"), input.get("manufacturer")),
            )
            conn.commit()
            starship_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            starship = conn.execute(
                "SELECT id, name, model, manufacturer FROM starships WHERE id = ?", (starship_id,)
            ).fetchone()
            return dict(starship)
        except sqlite3.IntegrityError:
            conn.rollback()
            raise Exception(f"Kapal '{input['name']}' sudah ada.")
        finally:
            conn.close()

    @mutation.field("updateStarship")
    def resolve_update_starship(_, info, input):
        conn = get_db_connection()
        try:
            starship = conn.execute("SELECT id, name, model, manufacturer FROM starships WHERE id = ?", (input["id"],)).fetchone()
            if not starship:
                raise Exception(f"Kapal dengan ID {input['id']} tidak ditemukan.")
            conn.execute(
                "UPDATE starships SET name = ?, model = ?, manufacturer = ? WHERE id = ?",
                (
                    input.get("name", starship["name"]),
                    input.get("model", starship["model"]),
                    input.get("manufacturer", starship["manufacturer"]),
                    input["id"],
                ),
            )
            conn.commit()
            updated_starship = conn.execute(
                "SELECT id, name, model, manufacturer FROM starships WHERE id = ?", (input["id"],)
            ).fetchone()
            return dict(updated_starship)
        except sqlite3.IntegrityError:
            conn.rollback()
            raise Exception(f"Kapal '{input['name']}' sudah ada.")
        finally:
            conn.close()
