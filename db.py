import sqlite3
from flask import g


def get_connection():
    if "db" not in g:
        con = sqlite3.connect("database.db")
        con.execute("PRAGMA foreign_keys = ON")
        con.row_factory = sqlite3.Row
        g.db = con
    return g.db


def close_connection(e=None):
    con = g.pop("db", None)
    if con is not None:
        con.close()


def execute(sql, params=None):
    if params is None:
        params = []
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid


def last_insert_id():
    return g.last_insert_id


def query(sql, params=None):
    if params is None:
        params = []
    con = get_connection()
    return con.execute(sql, params).fetchall()
