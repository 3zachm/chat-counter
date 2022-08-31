import utils.api.db as db

def insert_log(user_id, username, message, tags):
    sql = "INSERT INTO logs (id, user, message, badges, isMod, isSub, isTurbo, color) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (user_id, username, message, tags['badges'], tags['mod'], tags['subscriber'], tags['turbo'], tags['color'])
    db.execute_val(sql, val)
    db.commit()