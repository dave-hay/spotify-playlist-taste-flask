from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PlaylistEntry(FlaskForm):
    playlist = StringField('Playlist', validators=[DataRequired()])
    submit = SubmitField('Generate')
