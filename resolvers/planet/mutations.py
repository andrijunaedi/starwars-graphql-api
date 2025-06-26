import sqlite3
from database import get_db_connection

def register_planet_mutations(mutation):
    @mutation.field("updatePlanet")
    def resolve_update_planet(_, info, input):
        conn = get_db_connection()
        try:
            planet = conn.execute("SELECT id, name, climate, terrain FROM planets WHERE id = ?", (input["id"],)).fetchone()
            if not planet:
                raise Exception(f"Planet dengan ID {input['id']} tidak ditemukan.")
            conn.execute(
                "UPDATE planets SET name = ?, climate = ?, terrain = ? WHERE id = ?",
                (
                    input.get("name", planet["name"]),
                    input.get("climate", planet["climate"]),
                    input.get("terrain", planet["terrain"]),
                    input["id"],
                ),
            )
            conn.commit()
            updated_planet = conn.execute("SELECT id, name, climate, terrain FROM planets WHERE id = ?", (input["id"],)).fetchone()
            return dict(updated_planet)
        except sqlite3.IntegrityError:
            conn.rollback()
            raise Exception("Nama planet sudah digunakan.")
        finally:
            conn.close()

    @mutation.field("deletePlanet")
    def resolve_delete_planet(_, info, id):
        conn = get_db_connection()
        try:
            planet = conn.execute("SELECT id FROM planets WHERE id = ?", (id,)).fetchone()
            if not planet:
                raise Exception(f"Planet dengan ID {id} tidak ditemukan.")
            residents = conn.execute("SELECT COUNT(*) FROM characters WHERE home_planet_id = ?", (id,)).fetchone()[0]
            if residents > 0:
                raise Exception(f"Tidak dapat menghapus planet dengan {residents} penduduk.")
            conn.execute("DELETE FROM planets WHERE id = ?", (id,))
            conn.commit()
            return True
        finally:
            conn.close()

    @mutation.field("createPlanet")
    def resolve_create_planet(_, info, input):
        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO planets (name, climate, terrain) VALUES (?, ?, ?)",
                (input["name"], input["climate"], input["terrain"]),
            )
            conn.commit()
            new_planet = conn.execute("SELECT id, name, climate, terrain FROM planets WHERE name = ?", (input["name"],)).fetchone()
            return dict(new_planet)
        except sqlite3.IntegrityError:
            conn.rollback()
            raise Exception("Nama planet sudah digunakan.")
        finally:
            conn.close()