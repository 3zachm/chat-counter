import utils.api.db as db

def insert_log(user_id, username, message):
    sql = "INSERT INTO logs (id, user, message) VALUES (%s, %s, %s)"
    val = (user_id, username, message)
    db.execute_val(sql, val)
    db.commit()