import mysql.connector
import utils.file_manager as files

host = None
user = None
password = None
database = None
db = None
cursor = None

def initiate():
    global cursor, db
    db=mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor=db.cursor(buffered=True, dictionary=True)

def commit():
    db.commit()

def close():
    commit()
    cursor.close()
    db.close()

def execute_val(sql, val):
    try:
        cursor.execute(sql, val)
    except mysql.connector.errors.DatabaseError:
        initiate()
        cursor.execute(sql, val)

def execute(sql):
    try:
        cursor.execute(sql)
    except mysql.connector.errors.DatabaseError:
        initiate()
        cursor.execute(sql)

def fetchall():
    return cursor.fetchall()