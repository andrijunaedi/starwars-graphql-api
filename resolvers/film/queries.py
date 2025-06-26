from database import get_db_connection

def register_film_queries(query):
    @query.field("allFilms")
    def resolve_all_films(_, info):
        conn = get_db_connection()
        try:
            films = conn.execute(
                "SELECT id, title, episode_id, director, release_date, opening_crawl FROM films"
            ).fetchall()
            return [dict(film) for film in films]
        finally:
            conn.close()

    @query.field("film")
    def resolve_film(_, info, id):
        conn = get_db_connection()
        try:
            film = conn.execute(
                "SELECT id, title, episode_id, director, release_date, opening_crawl FROM films WHERE id = ?", 
                (id,)
            ).fetchone()
            return dict(film) if film else None
        finally:
            conn.close()