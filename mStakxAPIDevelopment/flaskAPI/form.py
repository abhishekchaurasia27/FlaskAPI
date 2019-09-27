from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class create_form(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    isbn = StringField('isbn', validators=[DataRequired()])
    authors = StringField('authors', validators=[DataRequired()])
    country = StringField('country', validators=[DataRequired()])
    numberOfPages = StringField('numberOfPages', validators=[DataRequired()])
    publisher = StringField('publisher', validators=[DataRequired()])
    release = StringField('release', validators=[DataRequired()])
    submit = SubmitField('Create Book!')
