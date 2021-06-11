import utils.api.db as db

def insert_user(user_id):
    sql = "INSERT INTO users (id, yep, cock) VALUES (%s, 0, 0)"
    val = (user_id)
    db.execute_val(sql, (val,))
    db.commit()

def update_user(column, user_id):
    sql = "UPDATE users SET {0} = {0} + 1 WHERE id = %s".format(column)
    val = (user_id)
    db.execute_val(sql, (val,))
    db.commit()

def get_user(user_id):
    sql = "SELECT * FROM users WHERE id = %s"
    val = (user_id)
    db.execute_val(sql, (val,))
    db.commit()
    return db.fetchall()