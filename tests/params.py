characters_get_params = [
    ("1. Successful get on /characters/", "/characters/", 200),
    ("2. Successful get on /characters/search/", "/characters/search/1", 200),
]
characters_get_ids = [x[0] for x in characters_get_params]

delete_post_params = [
    ("1. Delete character record", "people", 200),
    ("2. Delete reference info record", "referenceinfo", 200),
]
delete_ids = [x[0] for x in delete_post_params]
