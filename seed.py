from database import get_db_connection, init_db

def seed_data():
    """Mengisi database dengan data awal Star Wars."""
    conn = get_db_connection()
    c = conn.cursor()

    # Bersihkan data lama
    c.execute("DELETE FROM film_characters")
    c.execute("DELETE FROM film_planets")
    c.execute("DELETE FROM film_starships")
    c.execute("DELETE FROM character_starships")
    c.execute("DELETE FROM characters")
    c.execute("DELETE FROM starships")
    c.execute("DELETE FROM planets")
    c.execute("DELETE FROM films")
    conn.commit()

    # Data planet
    planets = [
        ("Tatooine", "Arid", "Desert"),
        ("Alderaan", "Temperate", "Grasslands, Mountains"),
        ("Yavin IV", "Temperate, Humid", "Jungle, Rainforests"),
        ("Naboo", "Temperate", "Grassy Hills, Swamps"),
        ("Coruscant", "Temperate", "Cityscape"),
    ]
    c.executemany("INSERT INTO planets (name, climate, terrain) VALUES (?, ?, ?)", planets)
    planet_ids = {row["name"]: row["id"] for row in c.execute("SELECT id, name FROM planets").fetchall()}

    # Data karakter
    characters = [
        ("Luke Skywalker", "Human", planet_ids["Tatooine"]),
        ("Leia Organa", "Human", planet_ids["Alderaan"]),
        ("Han Solo", "Human", None),
        ("C-3PO", "Droid", None),
        ("Yoda", "Unknown", None),
    ]
    c.executemany("INSERT INTO characters (name, species, home_planet_id) VALUES (?, ?, ?)", characters)
    character_ids = {row["name"]: row["id"] for row in c.execute("SELECT id, name FROM characters").fetchall()}

    # Data kapal
    starships = [
        ("Millennium Falcon", "YT-1300 light freighter", "Corellian Engineering"),
        ("X-wing", "T-65 X-wing starfighter", "Incom Corporation"),
        ("TIE Fighter", "TIE/LN starfighter", "Sienar Fleet Systems"),
    ]
    c.executemany("INSERT INTO starships (name, model, manufacturer) VALUES (?, ?, ?)", starships)
    starship_ids = {row["name"]: row["id"] for row in c.execute("SELECT id, name FROM starships").fetchall()}

    # Relasi karakter-kapal
    character_starships = [
        (character_ids["Han Solo"], starship_ids["Millennium Falcon"]),
        (character_ids["Luke Skywalker"], starship_ids["X-wing"]),
    ]
    c.executemany("INSERT INTO character_starships (character_id, starship_id) VALUES (?, ?)", character_starships)
    
    # Data film
    films = [
        (
            "A New Hope", 
            4, 
            "George Lucas", 
            "1977-05-25", 
            "It is a period of civil war. Rebel spaceships, striking from a hidden base, have won their first victory against the evil Galactic Empire."
        ),
        (
            "The Empire Strikes Back", 
            5, 
            "Irvin Kershner", 
            "1980-05-21", 
            "It is a dark time for the Rebellion. Although the Death Star has been destroyed, Imperial troops have driven the Rebel forces from their hidden base and pursued them across the galaxy."
        ),
        (
            "Return of the Jedi", 
            6, 
            "Richard Marquand", 
            "1983-05-25", 
            "Luke Skywalker has returned to his home planet of Tatooine in an attempt to rescue his friend Han Solo from the clutches of the vile gangster Jabba the Hutt."
        ),
    ]
    c.executemany(
        "INSERT INTO films (title, episode_id, director, release_date, opening_crawl) VALUES (?, ?, ?, ?, ?)", 
        films
    )
    film_ids = {row["title"]: row["id"] for row in c.execute("SELECT id, title FROM films").fetchall()}
    
    # Relasi film-karakter
    film_characters = [
        (film_ids["A New Hope"], character_ids["Luke Skywalker"]),
        (film_ids["A New Hope"], character_ids["Leia Organa"]),
        (film_ids["A New Hope"], character_ids["Han Solo"]),
        (film_ids["A New Hope"], character_ids["C-3PO"]),
        (film_ids["The Empire Strikes Back"], character_ids["Luke Skywalker"]),
        (film_ids["The Empire Strikes Back"], character_ids["Leia Organa"]),
        (film_ids["The Empire Strikes Back"], character_ids["Han Solo"]),
        (film_ids["The Empire Strikes Back"], character_ids["Yoda"]),
        (film_ids["Return of the Jedi"], character_ids["Luke Skywalker"]),
        (film_ids["Return of the Jedi"], character_ids["Leia Organa"]),
        (film_ids["Return of the Jedi"], character_ids["Han Solo"]),
        (film_ids["Return of the Jedi"], character_ids["Yoda"]),
    ]
    c.executemany("INSERT INTO film_characters (film_id, character_id) VALUES (?, ?)", film_characters)
    
    # Relasi film-planet
    film_planets = [
        (film_ids["A New Hope"], planet_ids["Tatooine"]),
        (film_ids["A New Hope"], planet_ids["Alderaan"]),
        (film_ids["A New Hope"], planet_ids["Yavin IV"]),
        (film_ids["The Empire Strikes Back"], planet_ids["Tatooine"]),
        (film_ids["The Empire Strikes Back"], planet_ids["Naboo"]),
        (film_ids["Return of the Jedi"], planet_ids["Tatooine"]),
        (film_ids["Return of the Jedi"], planet_ids["Coruscant"]),
    ]
    c.executemany("INSERT INTO film_planets (film_id, planet_id) VALUES (?, ?)", film_planets)
    
    # Relasi film-kapal
    film_starships = [
        (film_ids["A New Hope"], starship_ids["Millennium Falcon"]),
        (film_ids["A New Hope"], starship_ids["X-wing"]),
        (film_ids["A New Hope"], starship_ids["TIE Fighter"]),
        (film_ids["The Empire Strikes Back"], starship_ids["Millennium Falcon"]),
        (film_ids["The Empire Strikes Back"], starship_ids["X-wing"]),
        (film_ids["Return of the Jedi"], starship_ids["Millennium Falcon"]),
    ]
    c.executemany("INSERT INTO film_starships (film_id, starship_id) VALUES (?, ?)", film_starships)

    conn.commit()
    conn.close()
    print("Database berhasil diisi dengan data Star Wars!")

if __name__ == "__main__":
    init_db()  # Pastikan tabel ada
    seed_data()