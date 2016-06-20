from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField

class AddArtForm(Form):
    title = StringField('Title: ')
    text = TextAreaField("Text: ")
    submit = SubmitField("Push")