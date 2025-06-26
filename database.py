import sqlite3

DATABASE_NAME = "starwars.db"

def get_db_connection():
    """Membuka koneksi ke database dengan row factory untuk akses kolom berdasarkan nama."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Membuat tabel jika belum ada."""
    conn = get_db_connection()
    c = conn.cursor()

    # Tabel planets
    c.execute("""
        CREATE TABLE IF NOT EXISTS planets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            climate TEXT,
            terrain TEXT
        )
    """)

    # Tabel characters
    c.execute("""
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            species TEXT,
            home_planet_id INTEGER,
            FOREIGN KEY (home_planet_id) REFERENCES planets (id)
        )
    """)

    # Tabel starships
    c.execute("""
        CREATE TABLE IF NOT EXISTS starships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            model TEXT,
            manufacturer TEXT
        )
    """)

    # Tabel penghubung characters-starships (many-to-many)
    c.execute("""
        CREATE TABLE IF NOT EXISTS character_starships (
            character_id INTEGER,
            starship_id INTEGER,
            PRIMARY KEY (character_id, starship_id),
            FOREIGN KEY (character_id) REFERENCES characters (id),
            FOREIGN KEY (starship_id) REFERENCES starships (id)
        )
    """)
    
    # Tabel films
    c.execute("""
        CREATE TABLE IF NOT EXISTS films (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            episode_id INTEGER UNIQUE,
            director TEXT,
            release_date TEXT,
            opening_crawl TEXT
        )
    """)
    
    # Tabel penghubung films-characters (many-to-many)
    c.execute("""
        CREATE TABLE IF NOT EXISTS film_characters (
            film_id INTEGER,
            character_id INTEGER,
            PRIMARY KEY (film_id, character_id),
            FOREIGN KEY (film_id) REFERENCES films (id),
            FOREIGN KEY (character_id) REFERENCES characters (id)
        )
    """)
    
    # Tabel penghubung films-planets (many-to-many)
    c.execute("""
        CREATE TABLE IF NOT EXISTS film_planets (
            film_id INTEGER,
            planet_id INTEGER,
            PRIMARY KEY (film_id, planet_id),
            FOREIGN KEY (film_id) REFERENCES films (id),
            FOREIGN KEY (planet_id) REFERENCES planets (id)
        )
    """)
    
    # Tabel penghubung films-starships (many-to-many)
    c.execute("""
        CREATE TABLE IF NOT EXISTS film_starships (
            film_id INTEGER,
            starship_id INTEGER,
            PRIMARY KEY (film_id, starship_id),
            FOREIGN KEY (film_id) REFERENCES films (id),
            FOREIGN KEY (starship_id) REFERENCES starships (id)
        )
    """)

    conn.commit()
    conn.close()
    print("Tabel berhasil dibuat.")

if __name__ == "__main__":
    init_db()