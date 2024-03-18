# -*- coding: UTF-8 -*-
import os
import uuid


from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flask_login import LoginManager
from flask import request, redirect, url_for
from flask_login import login_required, login_user, logout_user



from models import db_session, WorkingFilms, Cinema, ApplicationUser, Reviews, ParticationCinema


import settings

app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = settings.SECRET_KEY
manager = LoginManager(app)


SHOW_MOVIES = True;

# Отображение фильмов на главной странице
@app.route('/')
def TopMovie():
    cinemas = db_session.query(Cinema).all()
    return render_template('MovieSelections/TopMovie.html', cinemas=cinemas, show_movies=SHOW_MOVIES)

@app.route('/NewMovie')
def NewMovie():
    return render_template('MovieSelections/NewMovie.html', show_movies=SHOW_MOVIES)

@app.route('/PopularMovies')
def PopularMovies():
    return render_template('MovieSelections/PopularMovies.html', show_movies=SHOW_MOVIES)

@app.route('/TopSerial')
def TopSerial():
    return render_template('SeriesSelections/TopSerial.html', show_movies=not SHOW_MOVIES)

@app.route('/NSerial')
def NSerial():
    return render_template('SeriesSelections/NSerial.html', show_movies=not SHOW_MOVIES)

@app.route('/PopularSerial')
def PopularSerial():
    return render_template('SeriesSelections/PopularSerial.html', show_movies=not SHOW_MOVIES)

@app.route('/Film/<int:id>/')
def Film_by_id(id):
    item = db_session.query(Cinema).filter(Cinema.id == id).first()
    return render_template('SaytMovie/Film.html', item = item)

@app.route('/Login')
def Login():
    return render_template('Login/Login.html')

@app.route('/Vhod')
def Vhod():
    return render_template('Login/Vhod.html')

@app.route("/<page_name>/")
def main(page_name):
    return render_template(page_name+'.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('/'))


@app.after_request
def redirect_to_sign(response):
    if response.status_code == 401:
        return redirect(url_for('/Login'))
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5057, debug=True)
