
DELIMITER = ";"

def deserialize_genres(genres):
    return genres.split(DELIMITER)

def serialize_genres(genres):
    return DELIMITER.join(genres)

