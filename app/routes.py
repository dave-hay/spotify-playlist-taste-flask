from flask import render_template, redirect, url_for
from app import app
from app.forms import PlaylistEntry
from app.generator import playlist


@app.route('/generate', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def generate():
    form = PlaylistEntry()
    if form.validate_on_submit():
        playlist_id = form.playlist.data
        playlist(playlist_id)
        return redirect(url_for('results'))
    return render_template('generate.html', form=form)


@app.route('/result')
def results():
    return render_template('results.html')
