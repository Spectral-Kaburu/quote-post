import sqlite3
from contextlib import closing

DATABASE = "website7.db"

def get_db():
    return sqlite3.connect(DATABASE)

def create_tables():
    with closing(get_db()) as cx:
        cursor = cx.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL, username TEXT NOT NULL, email TEXT NOT NULL)")
        cursor.execute("CREATE TABLE IF NOT EXISTS blogs(blog_id INTEGER PRIMARY KEY, blog TEXT NOT NULL UNIQUE)")
        cursor.execute("CREATE TABLE IF NOT EXISTS connect(blog_id INTEGER, user_id INTEGER, PRIMARY KEY(blog_id, user_id))")
        cursor.execute("CREATE TABLE IF NOT EXISTS commect(blog_id INTEGER, comment_id INTEGER, PRIMARY KEY(blog_id, comment_id))")
        cursor.execute("CREATE TABLE IF NOT EXISTS comment(comment_id INTEGER PRIMARY KEY, comment TEXT NOT NULL, username TEXT NOT NULL)")
        cursor.execute("CREATE TABLE IF NOT EXISTS hashed_passwords(username TEXT NOT NULL, password TEXT NOT NULL)")
        cx.commit()
