# -*- coding: UTF-8 -*-
import os
import uuid
import settings
from flask_login import LoginManager, login_required, current_user
from flask import Flask, g, render_template
from flask import Flask, request, Response





import settings

app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = settings.SECRET_KEY
manager = LoginManager(app)


SHOW_MOVIES = True;

# Отображение фильмов на главной странице
@app.route('/')
def TopMovie():
    from models import db_session, Cinema, WorkingFilms, ParticationCinema
    cinemas = db_session.query(Cinema).filter(Cinema.cinema_option == 'False').order_by(Cinema.note.desc()).limit(5).all()
    return render_template('MovieSelections/TopMovie.html', cinemas=cinemas, show_movies=SHOW_MOVIES)

@app.route('/NewMovie')
def NewMovie():
    return render_template('MovieSelections/NewMovie.html', show_movies=SHOW_MOVIES)

@app.route('/PopularMovies')
def PopularMovies():
    return render_template('MovieSelections/PopularMovies.html', show_movies=SHOW_MOVIES)

@app.route('/TopSerial')
def TopSerial():
    from models import db_session, Cinema, WorkingFilms, ParticationCinema
    cinemas = db_session.query(Cinema).filter(Cinema.cinema_option == 'True').all()
    return render_template('MovieSelections/TopMovie.html', cinemas=cinemas, show_movies=SHOW_MOVIES)

@app.route('/NSerial')
def NSerial():
    return render_template('SeriesSelections/NSerial.html', show_movies=not SHOW_MOVIES)

@app.route('/PopularSerial')
def PopularSerial():
    return render_template('SeriesSelections/PopularSerial.html', show_movies=not SHOW_MOVIES)

@app.route('/Film/<int:id>/')
def Film_by_id(id):
    from models import db_session, Cinema, WorkingFilms, Reviews
    cinema = db_session.query(Cinema).filter(Cinema.id == id).first()
    reviews = db_session.query(Reviews).filter(Reviews.mail_obrash == id).all()
    app.logger.info(cinema.director)
    return render_template('SaytMovie/Film.html', cinema=cinema, reviews=reviews)


@app.route("/Film/<int:id>/", methods=["POST"])
@login_required
def add_review(id):
    from models import db_session, Reviews
    if request.method == 'POST':
        # Получаем имя текущего авторизованного пользователя
        user_name = current_user.login

        # Получаем остальные данные из формы
        mail_comer = request.form.get('userReview')
        mail_obrash = request.form.get('id')
        href1 = request.form.get('#')
        href2 = request.form.get('#')
        href3 = request.form.get('#')
        number = request.form.get('userRating', 10, type=int)

        # Создаем новый объект Review и добавляем его в базу данных
        new_review = Reviews(name=user_name, mail_comer=mail_comer, mail_obrash=mail_obrash,
                             href1=href1, href2=href2, href3=href3, number=number)
        db_session.add(new_review)
        db_session.commit()

        return """
            <script>
                window.location.href = window.location.href;
            </script>
            """
    else:
        return 'Метод GET не поддерживается для этого маршрута', 405



@app.route("/Film/<int:id>", methods=["GET", "POST"])
def find_news_by_get(id):
    if request.method == 'GET':
        title = request.args.get('userName')
        limit = request.args.get('userRating', 10, type=int)
        text = request.args.get('userReview')
        id = request.args.get('id', type=int)
        if title is None or text is None:
            return 'Не найдено', 404
        return {'userRating': limit, 'userName': title, 'userReview': text, 'id': id}
    else:
        return 'Метод POST не поддерживается для этого маршрута', 405



##@app.route('/Login')
##def Login():
##    return render_template('Login/Login.html')

#@app.route('/Vhod')
#def Vhod():
#    return render_template('Login/login.html')

#@app.route("/<page_name>/")
#def main(page_name):
   # return render_template(page_name+'.html')


##@app.route('/Login', methods = ['GET', 'POST'])
##def register():
##    if request.method == 'GET':
##        return render_template('Login/Login.html')
##    login = request.form.get('username')
##    password = request.form.get('password')
##    user = User(login = login, password = password)
##    db_session.add(user)
##    db_session.commit()
##    login_user(user)
##    return render_template('Login/Login.html')
##
##@app.route('/logout')
##@login_required
##def logout():
##    logout_user()
##    return redirect(url_for('TopMovie'))
##
##
##@app.after_request
##def redirect_to_sign(response):
##    if response.status_code == 401:
##        return redirect(url_for('Login'))
##    return response

@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    from werkzeug.middleware.shared_data import SharedDataMiddleware
    from controller import *
    app.run(host='0.0.0.0', port=5057, debug=True)
