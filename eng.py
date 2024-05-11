# -*- coding: UTF-8 -*-
import os
import uuid

import settings
from flask_login import LoginManager, login_required, current_user
from flask import Flask, g, render_template
from flask import Flask, request, Response, jsonify, flash, redirect, url_for





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

@app.route('/search')
def search_movies():
    from flask import Flask, request, jsonify, render_template
    from models import db_session, Cinema  # Подставьте нужные импорты моделей
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify([])

    # Используем запрос к базе данных для поиска фильмов
    cinemas = db_session.query(Cinema).filter(Cinema.label.ilike(f'%{query}%')).all()

    # Собираем данные о фильмах
    movies_data = []
    for cinema in cinemas:
        movie_data = {
            'image': cinema.image,
            'label': cinema.label,
            'year': cinema.year,
            'country': cinema.country,
            'genre': cinema.genre,
            'age_rating': cinema.age_rating,
            'trailer_link': cinema.trailer_link,
            'note': cinema.note,
            'link': url_for('Film_by_id', id=cinema.id)
        }
        movies_data.append(movie_data)

    return jsonify(movies_data)

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
    raiting = None
    if current_user.is_authenticated:
        raiting = db_session.query(Reviews).filter(Reviews.name == current_user.login, Reviews.mail_obrash == id).first()
    app.logger.info(cinema.director)
    return render_template('SaytMovie/Film.html', cinema=cinema, reviews=reviews, raiting=raiting)


@app.route("/Film/<int:id>/", methods=["POST"])
@login_required
def add_review(id):
    from models import db_session, Reviews
    from flask import make_response, redirect
    if request.method == 'POST':
        # Получаем имя текущего авторизованного пользователя
        user_name = current_user.login
        user_img = current_user.profile_picture

        # Получаем остальные данные из формы
        mail_comer = request.form.get('userReview')
        mail_obrash = request.form.get('id')
        href1 = request.form.get('user_img')
        href2 = request.form.get('#')
        href3 = request.form.get('#')
        number = request.form.get('userRating', 10, type=int)

        # Создаем новый объект Review и добавляем его в базу данных
        new_review = Reviews(name=user_name, mail_comer=mail_comer, mail_obrash=mail_obrash,
                             href1=user_img, href2=href2, href3=href3, number=number)
        db_session.add(new_review)

            # Получаем все отзывы пользователя
        user_reviews = Reviews.query.filter_by(name=user_name).all()

        # Обновляем оценку у всех комментариев пользователя
        for review in user_reviews:
            review.number = number
        db_session.commit()

        # Устанавливаем куки, чтобы пометить форму как отправленную
        response = make_response(redirect(request.url))
        response.set_cookie('form_submitted', 'true')
        return response

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

@app.route('/Captcha')
def Captcha():
    return render_template('captcha.html', )

@app.route('/Profily')
@login_required
def Profily():
    from models import db_session, User
    user_name = current_user.login
    user_profile_picture = current_user.profile_picture  # Получаем путь к фото профиля пользователя
    return render_template('SaytMovie/Profily.html', user_name=user_name, user_profile_picture=user_profile_picture)



# Папка для сохранения загруженных изображений
UPLOAD_FOLDER = 'D:\Programming\Kinodom(web)/flask_project/static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from werkzeug.utils import secure_filename

# Здесь можно определить разрешенные типы файлов, если требуется
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Функция для проверки разрешенных типов файлов
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Затем используйте эти переменные в вашем коде


@app.route('/upload_profile_picture', methods=['POST'])
@login_required
def upload_profile_picture():
    from models import db_session, User
    file = request.files['profilePicture']
    if ('profilePicture' not in request.files) and (file.filename == ''):
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        current_user.profile_picture = os.path.join(filename)
        flash('File uploaded successfully')
    new_username = request.form.get('newUsername')  # Получаем новое имя пользователя из формы
    current_user.login = new_username  # Обновляем имя текущего пользователя
    db_session.commit()  # Сохраняем изменения в базе данных
    return redirect(url_for('Profily'))

@app.route("/update_username", methods=["GET"])
def update_username_get():
    return 'Метод GET не поддерживается для этого маршрута', 405  # Возвращаем сообщение об ошибке для GET запросов


from flask import send_file

@app.route('/get_profile_picture/<int:user_id>')
def get_profile_picture(user_id):
    from models import db_session, User
    user = db_session.query(User).get(user_id)
    if user:
        # Предположим, что изображение хранится в поле profile_picture модели User
        return send_file(user.profile_picture, mimetype='image/jpeg')  # Используйте правильный MIME-тип для вашего изображения
    else:
        return 'Изображение не найдено', 404


if __name__ == "__main__":
    from werkzeug.middleware.shared_data import SharedDataMiddleware
    from controller import *
    app.run(host='0.0.0.0', port=5057, debug=True)
