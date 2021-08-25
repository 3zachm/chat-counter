import utils.api.db as db

def insert_log(user_id, message):
    sql = "INSERT INTO logs (id, message) VALUES (%s, %s)"
    val = (user_id, message)
    db.execute_val(sql, val)
    db.commit()