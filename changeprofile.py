from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

changeprof = Blueprint('changeprof', __name__)

@changeprof.route('/profile/setting')
@login_required
def settingmain():
    return render_template('SettingProfile.html')


@changeprof.route('/profile/setting/password', methods=['POST', 'GET'])
def changepassword():
    from __init__ import User
    from __init__ import db

    oldpass = request.form.get('oldpass')
    newpass = request.form.get('newpass')
    id = User.query.filter(User.id).first()

    if request.method == 'POST':
        hash_oldpass = generate_password_hash(oldpass)
        if not (oldpass or newpass):
            flash('Заполните все поля!')
        elif oldpass == newpass:
            flash('Пароли не должны совпадать')

        if id and check_password_hash(id.password, hash_oldpass):

            flash('Неправильно введен текущий пароль')
        else:
            hash_newpass = generate_password_hash(newpass)
            newpass = User(password=hash_newpass, name=current_user.name, login=current_user.login, id=current_user.id)

            User.query.filter(User.login).delete()
            User.query.filter(User.id).delete()
            User.query.filter(User.name).delete()
            User.query.filter(User.password).delete()
            db.session.add(newpass)
            db.session.commit()

            redirect(url_for('changeprof.settingmain'))


    return render_template('ChangePassword.html')


@changeprof.route('/profile/setting/name', methods=['POST', 'GET'])
@login_required
def changename():
    from __init__ import db
    from __init__ import User

    newname = request.form.get('name')

    if request.method == 'POST':
        if not (newname):
            flash('Заполните поле!')
        elif newname == User.name:
            flash('Новое имя не должно совпадать с текущим!')

        else:
            newpass = User(password=current_user.password, name=newname, login=current_user.login, id=current_user.id)

            User.query.filter(User.login).delete()
            User.query.filter(User.id).delete()
            User.query.filter(User.name).delete()
            User.query.filter(User.password).delete()

            db.session.add(newpass)
            db.session.commit()

    return render_template('ChangeName.html')


@changeprof.route('/profile/setting/ava')
@login_required
def changeava():
    return render_template('ChangeAva.html')


@changeprof.route('/profile/setting/change/cover')
@login_required
def changecover():
    return render_template('ChangeCover.html')