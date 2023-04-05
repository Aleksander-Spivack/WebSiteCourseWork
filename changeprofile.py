from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import os
from werkzeug.utils import secure_filename


changeprof = Blueprint('changeprof', __name__)

@changeprof.route('/profile/setting')
@login_required
def settingmain():
    return render_template('SettingProfile.html')


@changeprof.route('/profile/setting/password', methods=['POST', 'GET'])
def changepassword():
    from __init__ import User
    from __init__ import db
    from forms import ResetPasswordForm

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(login=form.email.data).first()

        if user:
            if user and check_password_hash(user.password, form.password.data):
                if form.password.data == form.confirm_password.data:
                    flash('Пароли не должны совпадать!')
                else:
                    hash_password = generate_password_hash(form.confirm_password.data)
                    user.password = hash_password

                    db.session.commit()
                    return redirect(url_for('changeprof.settingmain'))
            else:
                flash('Старый пароль не совпадает с текущим!')

        else:
            flash('Такой почты не существует!')
    return render_template('ChangePassword.html', form=form)


@changeprof.route('/profile/setting/name', methods=['POST', 'GET'])
@login_required
def changename():
    from __init__ import db
    from __init__ import User
    from forms import ResetNameForm

    form=ResetNameForm()

    if form.validate_on_submit():
        user = User.query.filter_by(login=form.email.data).first()

        if user:
            if user.name == form.name.data:
                flash('Текущее имя не должно совпадать с новым!')

            else:
                user.name = form.name.data

                db.session.commit()

                return redirect(url_for('changeprof.settingmain'))
        else:
            flash('Такой почты не существует!')

    return render_template('ChangeName.html', form=form)

