import sqlite3


DATABASE = 'shackspacekey.sqlite'


def get_db():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    return cur, conn

