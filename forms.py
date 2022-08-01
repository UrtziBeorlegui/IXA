from wtforms import StringField, SubmitField, TextField
from wtforms import validators
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

class bilatuForm(FlaskForm):
    
    hitza = TextField("testua", validators = [DataRequired()])
    submit = SubmitField("bilatu")

class aukerakForm(FlaskForm):
    pass