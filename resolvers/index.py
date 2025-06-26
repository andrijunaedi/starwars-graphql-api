from ariadne import QueryType, MutationType

# Import semua resolvers
from .character.queries import register_character_queries
from .character.mutations import register_character_mutations
from .character.type_defs import character_type

from .planet.queries import register_planet_queries
from .planet.mutations import register_planet_mutations
from .planet.type_defs import planet_type

from .starship.queries import register_starship_queries
from .starship.mutations import register_starship_mutations
from .starship.type_defs import starship_type

from .film.queries import register_film_queries
from .film.mutations import register_film_mutations
from .film.type_defs import film_type

# Inisialisasi
query = QueryType()
mutation = MutationType()

# Register resolvers
register_character_queries(query)
register_character_mutations(mutation)

register_planet_queries(query)
register_planet_mutations(mutation)

register_starship_queries(query)
register_starship_mutations(mutation)

register_film_queries(query)
register_film_mutations(mutation)

# Compile semua resolvers
resolvers = [query, mutation, character_type, planet_type, starship_type, film_type]