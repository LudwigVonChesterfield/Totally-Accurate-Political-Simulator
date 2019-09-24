import sqlite3
import hashlib
import json

import global_vars

from defines import *
from config_loader import get_secret_key, get_salt

DATABASE_PATH = "../database/users.db"


def init_database():
    db_global_cursor.execute("""
        CREATE TABLE users
        (user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        super_secret TEXT,
        email TEXT UNIQUE,
        discord_id TEXT UNIQUE,
        hear_from TEXT,
        permissions INTEGER)
    """)


def setup():
    init_database()


if __name__ == "__main__":
    with open(DATABASE_PATH, "w+") as f:
        pass
    db = sqlite3.connect(DATABASE_PATH)
    db_global_cursor = db.cursor()
    setup()

db = sqlite3.connect(DATABASE_PATH)
db_global_cursor = db.cursor()


def arr_2_text(array):
    return json.dumps(array)


def text_2_arr(text):
    return json.loads(text)


def gen_user_super_secret():
    key = get_secret_key()
    salt = get_salt()  # This is somewhat redundant, but does lessen collisions for keys, and does somewhat increase difficulty, as it's 30 more symbols...

    combo_super_secret = key + salt
    hashed_super_secret = hashlib.sha512(combo_super_secret.encode('utf-8')).digest()

    """
    iterations = random.randint(1000, 3000)
    for i in range(iterations):
        hashed_super_secret = hashlib.sha512(hashed_super_secret.encode('utf-8')).digest()
    """

    return {"super_secret": hashed_super_secret, "key": key, "salt": salt}


def insert_user(email="", discord_id=""):
    db_user_cursor = db.cursor()

    super_secret_obj = gen_user_super_secret()

    hear_from = []
    for citizen in global_vars.citizens:
        hear_from.append(citizen.name)

    hear_from_text = arr_2_text(hear_from)

    db_user_cursor.execute("""
        INSERT INTO users(super_secret, email, discord_id, hear_from, permissions)
        VALUES (?,?,?,?,?)
        """,
        (super_secret_obj["super_secret"], email, discord_id, hear_from_text, SERVER_PERMISSION_BASIC))

    db.commit()

    return {"user_id": db_user_cursor.lastrowid, "key": super_secret_obj["key"], "salt": super_secret_obj["salt"]}  #, "iterations": iterations}


def new_user_super_secret(id):
    super_secret_obj = gen_user_super_secret()

    db_user_cursor = db.cursor()

    db_user_cursor.execute("""
        UPDATE users
        SET super_secret=?
        WHERE user_id=?
        """,
        (super_secret_obj["super_secret"], id,)
        )
    db.commit()

    return {"key": super_secret_obj["key"], "salt": super_secret_obj["salt"]}


def update_user(id, email="", discord_id="", hear_from=None, permissions=SERVER_PERMISSION_NONE):
    db_user_cursor = db.cursor()

    sql = """UPDATE users"""

    needs_update = False

    if(email != ""):
        sql += " SET email=" + email
        needs_update = True
    if(discord_id != ""):
        sql += " SET discord_id=" + str(discord_id)
        needs_update = True
    if(isinstance(hear_from, list) and len(hear_from) != 0):
        sql += "SET hear_from=" + arr_2_text(hear_from)
        needs_update = True
    if(permissions != SERVER_PERMISSION_NONE):
        sql += " SET permissions=" + str(permissions)
        needs_update = True

    if(needs_update):
        sql += " WHERE user_id=" + str(id)

        db_user_cursor.execute(sql)
        db.commit()
