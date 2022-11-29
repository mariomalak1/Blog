from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Length, DataRequired, ValidationError
from appname.posts.models import Post


class PostForm(FlaskForm):
    title = StringField("Title", validators=[Length(min = 2, max = 100), DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min = 2)])
    submit = SubmitField("Post")

    def validate_title(self, title):
        post = Post.query.filter_by(title= title.data).first()
        if post:
            raise ValidationError("this title is already taken you can search with this name to get it (:")

class PostEditForm(FlaskForm):
    title = StringField("Title", validators=[Length(min = 2, max = 100)])
    content = TextAreaField("Content", validators=[Length(min = 2)])
    submit = SubmitField("Save")
    def validate_title(self, title):
        post = Post.query.filter_by(title= title.data).first()
        if post and post.content == self.content:
            raise ValidationError("this title is already taken you can search with this name to get it (:")
