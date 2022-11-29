from appname.posts.models import Post
from flask import render_template, request
from flask import Blueprint

main = Blueprint("main", __name__)


@main.route('/')
@main.route('/home', methods = ["POST", "GET"])
def homepage():
    page = request.args.get("page", 1, type= int)
    posts = Post.query\
        .order_by(Post.date_create.desc())\
        .paginate(page = page, per_page = 5)
    return render_template("homepage.html", title = "Home", posts = posts)


@main.route("/about")
def about():
    return render_template("about.html")