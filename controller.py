from flask import render_template, request, redirect, url_for, flash

from eng import app
from models import db_session, User, Cinema

from flask_login import login_required, login_user, logout_user, current_user


@app.route('/Register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('Login/Register.html')
    login = request.form.get('username')
    password = request.form.get('password')
    profile_picture = request.form.get('D:\Programming\Kinodom(web)/flask_project/static\image.jpg')
    user = User(login=login, password=password, profile_picture=profile_picture)
    db_session.add(user)
    db_session.commit()
    login_user(user)
    return redirect(url_for('TopMovie'))


@app.route('/log')
@login_required
def logout():
    logout_user()
    return redirect(url_for('TopMovie'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('Login/login.html')

    login = request.form.get('username')
    password = request.form.get('password')
    user = db_session.query(User).filter(User.login == login, User.password == password).first()

    if user is None:
        flash('Неверный логин или пароль', 'error')
        return redirect(url_for('login'))  # возвращаем обратно на страницу входа

    login_user(user)
    return redirect(url_for('TopMovie'))


@app.after_request
def redirect_to_sign(response):
    if response.status_code == 401:
        return redirect(url_for('Register'))
    return response
