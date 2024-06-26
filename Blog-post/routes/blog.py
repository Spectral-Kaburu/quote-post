from flask import Blueprint, request, session, render_template, redirect, flash
from db import get_db
import sqlite3

blog_blueprint = Blueprint('blog', __name__)

@blog_blueprint.route("/blog", methods=["GET", "POST"])
def blogs():
    if "username" not in session:
        flash("You have not been registered or logged in yet!!")
        return redirect("/login")

    username = session["username"]

    with get_db() as cx:
        cursor = cx.cursor()
        cursor.execute("SELECT user_id FROM users WHERE username=?", (username,))
        user_id = cursor.fetchone()[0]

        if request.method == "GET":
            cursor.execute("SELECT blog_id, blog FROM blogs WHERE blog_id IN (SELECT blog_id FROM connect WHERE user_id=?)", (user_id,))
            blogs = cursor.fetchall()
            return render_template("blog.html", blogs=blogs)
        
        blog = request.form.get("blog")
        if not blog:
            msg = "Error: No blog content provided."
            return render_template("error.html", msg=msg)
        
        try:
            cursor.execute("INSERT INTO blogs(blog) VALUES (?)", (blog,))
            cx.commit()
        except sqlite3.IntegrityError:
            cx.rollback()
            return redirect("/view")
        
        cursor.execute("SELECT blog_id FROM blogs WHERE blog=?", (blog,))
        blog_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO connect(blog_id, user_id) VALUES (?, ?)", (blog_id, user_id))
        cx.commit()

    return redirect("/view")

@blog_blueprint.route("/edit/<blog_id>", methods=["GET", "POST"])
def edit(blog_id):
    if "username" not in session:
        return redirect("/signup")
    
    with get_db() as cx:
        cursor = cx.cursor()
        if request.method == "GET":
            cursor.execute("SELECT * FROM blogs WHERE blog_id = ?", (blog_id, ))
            blog = cursor.fetchone()
            return render_template("edit.html", blog=blog)
        
        edited = request.form.get("edited")
        cursor.execute("UPDATE blogs SET blog = ? WHERE blog_id = ?", (edited, blog_id))
        cx.commit()
        flash("edited successfully!!")
        return redirect("/blog")
    
@blog_blueprint.route("/delete/<blog_id>")
def delete(blog_id):
    if "username" not in session:
        return redirect("/signup")
    
    with get_db() as cx:
        cursor = cx.cursor()
        cursor.execute("DELETE FROM blogs WHERE blog_id = ?", (blog_id, ))
        cursor.execute("DELETE FROM connect WHERE blog_id = ?", (blog_id, ))
        cursor.execute("DELETE FROM comment WHERE comment_id IN (SELECT comment_id FROM commect WHERE blog_id = ?)", (blog_id, ))
        cursor.execute("DELETE FROM commect WHERE blog_id = ?", (blog_id,))

        cx.commit()
        return redirect("/blog")

@blog_blueprint.route("/view")
def view():
    if "username" not in session:
        return redirect("/signup")

    with get_db() as cx:
        cursor = cx.cursor()
        cursor.execute("SELECT * FROM connect")
        id_tuples = cursor.fetchall()

        if not id_tuples:
            msg = "Error: No blogs inserted!!"
            return render_template("error.html", msg=msg)

        bloggers = []
        for blog_id, user_id in id_tuples:
            cursor.execute("SELECT blog FROM blogs WHERE blog_id=?", (blog_id,))
            blog = cursor.fetchone()
            cursor.execute("SELECT username FROM users WHERE user_id=?", (user_id,))
            user = cursor.fetchone()

            if blog and user:
                bloggers.append((blog_id, blog[0], user[0]))

        return render_template("index.html", bloggers=bloggers)


@blog_blueprint.route("/comment/<int:idea>", methods=["GET", "POST"])
def comment(idea):
    cx = sqlite3.connect("website7.db")
    cursor = cx.cursor()

    if not idea:
        msg = "Error: Invalid blog ID"
        return render_template("error.html", msg=msg)

    if "username" not in session:
        flash("You've not been logged in yet.")
        return redirect("/login")

    blog_id = idea
    username = session["username"]

    if request.method == "GET":
        cursor.execute("SELECT comment_id FROM commect WHERE blog_id = ?", (blog_id,))
        comment_ids_tuple = cursor.fetchall()

        if comment_ids_tuple:
            comments = []
            for comment_ids in comment_ids_tuple:
                comment_i = comment_ids[0]
                cursor.execute("SELECT comment, username FROM comment WHERE comment_id = ?", (comment_i,))
                coment = cursor.fetchone()
                comments.append(coment)

            return render_template("comment.html", comments=comments, id=idea)

        return render_template("comment.html", id=idea)

    comment = request.form.get("comment")
    cursor.execute("INSERT INTO comment(comment, username) VALUES (?, ?)", (comment, username))
    cx.commit()
    cursor.execute("SELECT comment_id FROM comment WHERE comment=?", (comment,))
    comment_id_tuple = cursor.fetchone()

    if not comment_id_tuple:
        msg = "Error: Insertion of your comment failed."
        return render_template("error.html", msg=msg)

    comment_id = comment_id_tuple[0]
    cursor.execute("INSERT INTO commect(blog_id, comment_id) VALUES (?, ?)", (blog_id, comment_id))
    cx.commit()
    cursor.close()

    return redirect(f"/comment/{idea}")
