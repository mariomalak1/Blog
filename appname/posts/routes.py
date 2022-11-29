from flask import render_template, redirect, url_for, flash, request, Blueprint
from appname import db
from appname.posts.forms import PostForm, PostEditForm
from appname.posts.models import Post
from flask_login import current_user, login_required

# your routes here

posts = Blueprint("posts", __name__)

@posts.route("/post", methods = ["POST", "GET"])
@login_required
def Post_page():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content = form.content.data, user_id = current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("your post added successfully", "success")
        return redirect(url_for("main.homepage"))
    else:
        return render_template("post.html", title = "Create Post", form = form)


# to check that user change any of his information or not
def validate_post_edit(title, content):
    post = Post.query.filter_by(title = title.data, content = content.data).first()
    if post:
        return True

@posts.route("/post/<int:post_id>/update", methods = ["POST", "GET"])
@login_required
def post_edit(post_id):
    form = PostEditForm()
    post = Post.query.get_or_404(post_id)
    if post.author == current_user:
        if form.validate_on_submit():
            if validate_post_edit(form.title, form.content):
                flash("you don't make any changes to save it", "warning")
                return redirect(url_for("posts.post_edit", post_id=post_id))
            else:
                post.title = form.title.data
                post.content = form.content.data
                db.session.commit()
                flash("Post Edit Successfully", "success")
                return redirect(url_for("posts.post_edit",post_id = post_id))
        elif request.method == 'GET':
            form.title.data = post.title
            form.content.data = post.content
        return render_template("post_edit.html", post= post, form = form)
    else:
        return render_template("errors/403.html")



@posts.route("/post_view/<int:post_id>")
@login_required
def post_full(post_id):
    post = Post.query.filter_by(id = post_id).first()
    return render_template("post_full_view.html", post = post)

# to delete post
def delete(post):
    db.session.delete(post)
    db.session.commit()
    flash("your post has been deleted", "success")

@posts.route("/deletePost/<int:post_id>/<string:place>", methods = ["POST", "GET"])
def delete_post(post_id,place: str):
    post = Post.query.get_or_404(int(post_id))
    if place == "account_page":
        delete(post)
        return redirect(url_for("users.account", user_id= current_user.id))
    else:
        delete(post)
        return redirect(url_for("main.homepage"))
