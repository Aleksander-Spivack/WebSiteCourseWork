from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from flask_login import login_required, logout_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    from __init__ import User
    from __init__ import db

    login = request.form.get('email')
    password = request.form.get('pass')

    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))

    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            return redirect(url_for('main.profile'))
        else:
            flash(u"Логин или пароль не некорректны", 'error')

    return render_template('login.html')


@auth.route('/register', methods=['POST', 'GET'])
def register():
    from __init__ import User
    from __init__ import db

    name = request.form.get('name')
    login = request.form.get('email')
    psw = request.form.get('pass')
    psw2 = request.form.get('pass2')

    if request.method == 'POST':
        if not (login or psw or psw2 or name):
            flash(u'Заполните все поля', 'error')
        elif psw != psw2:
            flash(u'Пароли не совпадают', 'error')
        elif User.query.filter_by(login=login).first():
            flash(u"Логин уже существует", 'error')
        elif User.query.filter_by(name=name).first():
            flash(u"Такое имя уже существует", 'error')
        else:
            hash_psw = generate_password_hash(psw)
            new_user = User(login=login, password=hash_psw, name=name)
            db.session.add(new_user)
            db.session.commit()

            return redirect('login')

    return render_template('register.html')


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.base'))


@auth.after_request
def redirect_login(responce):
    if responce.status_code == 401:
        return redirect(url_for('login') + '?next' + request.url)

    return responce


