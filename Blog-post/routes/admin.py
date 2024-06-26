from flask import Blueprint, jsonify
from db import get_db

admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route("/admin")
def admin():
    with get_db() as cx:
        cursor = cx.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        return jsonify(users)

@admin_blueprint.route("/admin/passwords")
def admin_passwords():
    with get_db() as cx:
        cursor = cx.cursor()
        cursor.execute("SELECT * FROM hashed_passwords")
        passwords = cursor.fetchall()
        return jsonify(passwords)

@admin_blueprint.route("/admin/blogs")
def admin_blogs():
    with get_db() as cx:
        cursor = cx.cursor()
        cursor.execute("SELECT * FROM blogs")
        blogs = cursor.fetchall()
        return jsonify(blogs)

@admin_blueprint.route("/admin/comments")
def admin_comments():
    with get_db() as cx:
        cursor = cx.cursor()
        cursor.execute("SELECT * FROM comment")
        comments = cursor.fetchall()
        return jsonify(comments)

@admin_blueprint.route("/admin/connect")
def admin_connect():
    with get_db() as cx:
        cursor = cx.cursor()
        cursor.execute("SELECT blog_id, user_id FROM connect")
        connects = cursor.fetchall()
        
        bloggers = []
        for blog_id, user_id in connects:
            cursor.execute("SELECT username FROM users WHERE user_id=?", (user_id,))
            user = cursor.fetchone()
            cursor.execute("SELECT blog FROM blogs WHERE blog_id=?", (blog_id,))
            blog = cursor.fetchone()
            bloggers.append((user_id, user, blog_id, blog))

        return jsonify(bloggers)
