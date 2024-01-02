# store home page, user profile page, post page
#blueprint used to organize a group of views, templates and static files. 

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User
from . import db
#create a blueprint object
views = Blueprint("views", __name__)

#define routes with decorator
@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)
#link to app
#register the blueprint

@views.route("/create_post", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get("text")

        if not text:
            flash("Post cannot be empty", category="error")
        else: 
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post successfully created", category="success")
    return render_template("create_post.html", user=current_user)

@views.route("delete_post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash("No post", category="error")
    elif current_user.id != post.id:
        flash("You do not have permission to delete this post", category="error")

    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted.", category="success")
    return redirect(url_for("views.home"))

@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("No user with username exists", category="error")
        return redirect(url_for("views.home"))
    posts = Post.query.filter_by(username = username).all()
    return render_template('posts.html', username=current_user, posts=posts)