
status_code_400 = { "status_code": 400 }
status_code_500 = { "status_code": 500 }

def parseRequestJson(type, body):
  print("aa")
  if (body is None):
    return status_code_400
  print("bb ")
  if (type == "actor"):
    if ("name" not in body):
      return status_code_400
    data = {
      "status_code": 200,
      "name": body.get("name"),
      "age": body.get("age", 0),
      "gender": body.get("gender", ""),
    }
  elif (type == "movie"):
    if ("title" not in body):
      return status_code_400
    data = {
      "status_code": 200,
      "title": body.get("title"),
      "release_date": body.get("release_date", "")
    }
  elif (type == "audition"):
    if ("actor_id" not in body and "movie_id" not in body):
      return status_code_400
    data = {
      "status_code": 200,
      "actor_id": body.get("actor_id"),
      "movie_id": body.get("movie_id", "")
    }

  return data
