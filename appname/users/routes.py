from flask import render_template, redirect, url_for, flash, request, Blueprint
from appname import app, db, by
from appname.users.forms import LoginForm, RegistrationFrom, ChangeInformationForm, ForgetPasswordForm, ResetPasswordForm, ChangePasswordForm
from appname.users.models import User
from flask_login import login_user, current_user, logout_user, login_required
from .utils import send_reset_email, save_image
import os
from appname.posts.models import Post


users = Blueprint("users", __name__)

@users.route("/login", methods = ["post", "get"])
def login():
    loginform = LoginForm()
    if loginform.validate_on_submit():
        user = User.query.filter_by(email = loginform.email.data).first()
        if user and by.check_password_hash(user.password, loginform.password.data):
            login_user(user, remember= loginform.remember_me.data)
            next_page = request.args.get('next')
            flash(f"login done successful {current_user.username}", "info")
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for("main.homepage"))
        else:
            flash("your data is not valid", "danger")
    return render_template("login_page.html", form_login= loginform, title="Login")

@users.route("/signup", methods = ["post", "get"])
def signup():
    register_form = RegistrationFrom()
    if register_form.validate_on_submit():
        global user_registration
        hashed_password = by.generate_password_hash(register_form.password.data).decode('utf-8')
        user_registration = User(username= register_form.username.data, password= hashed_password, email= register_form.email.data)
        send_reset_email(user_registration, register_form,"registration")
        flash("check your email to confirm it, you can found it in spam field", "success")
        return redirect(url_for("users.login"))
    else:
        return render_template("register.html", form = register_form, title = "Registration")

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("users.login"))


@users.route("/account/<int:user_id>", methods = ['post', 'get'])
@login_required
def account(user_id):
    global form_Change
    form_Change = ChangeInformationForm()
    image = url_for('static', filename= 'imgs/profile_images/' + current_user.image_file)
    user = User.query.filter_by(id = user_id).first()
    if user:
        if user != current_user:
            return redirect(url_for("users.account_view", user_id = user.id))
    else:
        return render_template("errors/404.html")
    page = request.args.get("page", 1, type= int)
    posts = Post.query.\
        order_by(Post.date_create.desc())\
        .filter_by(author = user).\
        paginate(page= page, per_page= 5)
    if request.method == "POST":
        if request.form.get('action1') == "remove image":
            if user.image_file == "default.jpg":
                flash("you don't put any new photos to remove", "warning")
                return redirect(url_for("users.account", user_id = user.id))
            else:
                old_pic_path = os.path.join(app.root_path, 'static/imgs/profile_images', user.image_file)
                os.remove(old_pic_path)
                user.image_file = "default.jpg"
                db.session.commit()
                flash("photo removed", "success")
                return redirect(url_for("users.account", user_id = user.id))
    if form_Change.validate_on_submit():
        if validate_user_input(form_Change.username, form_Change.email, form_Change.image_name):
            flash("you don't enter new data to change it", "warning")
            return redirect(url_for("users.account", user_id = user.id))
        user.username = form_Change.username.data
        if form_Change.image_name.data:
            image_save = save_image(form_Change.image_name.data)
            user.image_file = image_save
        db.session.commit()
        if validate_email(form_Change, user.id):
            flash("Please Check Your Mail to confirm your Email, If you doesn't found it, check spam", "success")
            return redirect(url_for("main.homepage"))
        flash("Account Information has been changed", "success")
        return redirect(url_for("users.account", user_id = user.id))
    elif request.method == 'GET':
        form_Change.username.data = user.username
        form_Change.email.data = user.email
    return render_template('account.html', title = 'account', img = image, form = form_Change, posts = posts)

@users.route("/account_<int:user_id>")
def account_view(user_id):
    user = User.query.filter_by(id = user_id).first()
    if user:
        if user == current_user:
            return redirect(url_for("users.account", user_id = user_id))
    else:
        return render_template("errors/404.html")
    page = request.args.get("page", 1, type= int)
    posts = Post.query\
        .filter_by(author = user)\
        .order_by(Post.date_create.desc()).\
        paginate(page = page, per_page= 5)
    if user:
        return render_template("account_another.html", user = user, posts = posts)
    else:
        return render_template("errors/404.html")

@users.route("/forget password", methods = ["POST", "GET"])
def forget_password():
    if current_user.is_authenticated:
        return redirect(url_for("main.homepage"))
    form = ForgetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user, form,"resetpassword")
        flash("Check Your Email Inbox To Reset Password", "info")
        return redirect(url_for("users.login"))
    else:
        return render_template("forget_password.html", form = form, title = "Forget Password")

@users.route("/reset password/<token>/<string:action>", methods = ["POST", "GET"])
def reset_token(token, action):
    if action == "forget_password":
        user = User.verify_reset_token(token)
        if user is None:
            flash("that is invalid or expired token", "warning")
            return redirect(url_for("users.forget_password"))
        form = ResetPasswordForm()
        if form.validate_on_submit():
            if by.check_password_hash(user.password, form.password.data):
                flash("you don't change any thing please enter new password", "warning")
                return redirect(url_for("users.reset_token", token=token, _external=True, action= "forget_password"))
            else:
                hashed_password = by.generate_password_hash(form.password.data).decode('utf-8')
                user.password = hashed_password
                db.session.commit()
                flash(f"Your password has been updated!, Now you can Login", "success")
                return redirect(url_for("users.login"))
        return render_template("reset_password.html", form=form, title="Reset Password")
    elif action == "register":
        db.session.add(user_registration)
        db.session.commit()
        flash(f"account created successfully to {user_registration.username}!, Now you can Login", "success")
        return redirect(url_for("users.login"))

    elif action == "email_confirmation":
        current_user.email = form_Change.email.data
        db.session.commit()
        flash(f"account change email successfully", "success")
        return redirect(url_for("users.account", user_id= current_user.id))
    else:
        form = RegistrationFrom()
        return render_template("register.html", form=form, title="Registration")

# to check that user change any of his information or not
def validate_user_input(username, email, image_name):
    user = User.query.filter_by(username = username.data, email = email.data).first()
    if user and image_name.data == None:
        return True

def validate_email(form, user_id):
    user = User.query.filter_by(id = user_id).first()
    if user and user.email != form.email.data:
        send_reset_email(user, form,"email_confirmation")
        return True

@users.route("/change password /<int:user_id>", methods = ["POST", "GET"])
def change_password(user_id):
    form = ChangePasswordForm()
    user = User.query.filter_by(id = user_id).first()
    if form.validate_on_submit():
        if user:
            if by.check_password_hash(user.password,form.old_password.data):
                if by.check_password_hash(user.password,form.new_password.data):
                    flash("your new password is similar to old password, please change it", "warning")
                    return render_template("change_password.html", form = form)
                else:
                    hashed_password = by.generate_password_hash(form.new_password.data).decode('utf-8')
                    user.password = hashed_password
                    db.session.commit()
                    flash("your password is changed", "success")
                return redirect(url_for("users.account", user_id= user_id))
            else:
                flash("Your old Password is not correct please enter it again", "warning")
                return render_template("change_password.html", form= form)
        else:
            return redirect(url_for("errors"))
    else:
        return render_template("change_password.html", form = form)