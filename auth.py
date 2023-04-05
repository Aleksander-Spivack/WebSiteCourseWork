from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, logout_user
from flask_mail import Message

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
            flash('Логин или пароль не корректны!')

    return render_template('login.html')


@auth.route('/register', methods=['POST', 'GET'])
def register():
    from __init__ import User
    from __init__ import db
    from forms import RegisterForm

    form = RegisterForm()

    if form.validate_on_submit():
        login = User.query.filter_by(login=form.email.data).first()
        name = User.query.filter_by(name=form.name.data).first()

        if login:
            flash('Такая электронная почта уже существует!')
        elif name:
            flash('Такой пользователь уже существует!')
        elif form.password.data != form.confirm_password.data:
            flash('Пароли не совпадают!')
        else:
            hash_password = generate_password_hash(form.password.data)
            new_user = User(name=form.name.data, login=form.email.data, password=hash_password)

            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))



    return render_template('register.html', form=form)


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

@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    from forms import ForgoutPasswordForm
    from __init__ import User
    from __init__ import db

    form = ForgoutPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(login=form.email.data).first()
        name = User.query.filter_by(name=form.name.data).first()

        if name and user:
            hash_password = generate_password_hash(form.password.data)
            user.password = hash_password

            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            flash('Такого имени или почты не существует!')
    return render_template('ResetPassword.html', form=form)


