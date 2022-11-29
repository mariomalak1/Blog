import secrets
import os
from PIL import Image
from flask import url_for
from appname import app, mail
from flask_login import current_user
from flask_mail import Message



# function  to save image
def save_image(form_img):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_img.filename)
    pic_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/imgs/profile_images', pic_fn)

    ## to make image 250 * 250
    output_size = (250,250)
    i = Image.open(form_img)
    i.thumbnail(output_size)
    i.save(picture_path)

    if current_user.image_file == "default.jpg":
        return pic_fn
    else:
        old_pic_path = os.path.join(app.root_path, 'static/imgs/profile_images', current_user.image_file)
        os.remove(old_pic_path)
        return pic_fn

def send_reset_email(user, form,action = "resetpassword"):
    token = user.get_reset_token()
    msg = ""
    if action == "resetpassword":
        msg = Message("Password Reset Request", sender ='noreply@demo.com', recipients=[user.email])
        msg.body = f""" To reset your Password, Visit the following link :
        {url_for("users.reset_token", token= token, _external= True, action = "forget_password")}
        If you Don't make the request, then simply ignore this email and no change will be made"""
    if action == "registration":
        msg = Message("Email Confirmation Request", sender ='noreply@demo.com', recipients=[user.email])
        msg.body = f""" TO Confirm Your Email Please Visit the following link :
        {url_for("users.reset_token", token= token, _external= True, action = "register")}
        If you Don't make New Account, then simply ignore this email and no change will be made"""
    if action == "email_confirmation":
        msg = Message("Email Confirmation Request", sender ='noreply@demo.com', recipients=[form.email.data])
        msg.body = f""" TO Confirm Your Email Please Visit the following link :
        {url_for("users.reset_token", token= token, _external= True, action = "email_confirmation")}
        If you Don't make the change, then simply ignore this email and no change will be made"""
    print(msg)
    mail.send(msg)
