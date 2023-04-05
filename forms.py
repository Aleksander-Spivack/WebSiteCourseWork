from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email, length


class ForgoutPasswordForm(FlaskForm):
    email = EmailField(render_kw={"placeholder": "Введите электронную почту"}, validators=[DataRequired()])
    name = StringField(render_kw={"placeholder": "Введите имя"}, validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired(), length(min=8, max=30)], render_kw={"placeholder": "Введите новый пароль"})
    submit = SubmitField(label='Сменить пароль', validators=[DataRequired()])


class ResetPasswordForm(FlaskForm):
    email = EmailField(render_kw={"placeholder": "Введите электронную почту"}, validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()], render_kw={"placeholder": "Введите старый пароль"})
    confirm_password = PasswordField(validators=[DataRequired(), length(min=8, max=30)], render_kw={"placeholder": "Введите новый пароль"})
    submit = SubmitField(label='Сменить пароль', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    email = EmailField(render_kw={"placeholder": "Введите электронную почту"}, validators=[DataRequired()])
    name = StringField(render_kw={"placeholder": "Введите имя"}, validators=[DataRequired(), length(min=3, max=20)])
    password = PasswordField(render_kw={"placeholder": "Введите пароль"}, validators=[DataRequired(), length(min=8, max=30)])
    confirm_password = PasswordField(render_kw={"placeholder": "Введите повторно пароль"}, validators=[DataRequired(), length(min=8, max=30)])
    submit = SubmitField(label='Зарегистрироваться', validators=[DataRequired()])


class ResetNameForm(FlaskForm):
    email = EmailField(render_kw={"placeholder": "Введите электронную почту"}, validators=[DataRequired()])
    name = StringField(render_kw={"placeholder":"Введите новое имя"}, validators=[DataRequired(), length(min=3, max=20)])
    submit = SubmitField(label="Сменить имя", validators=[DataRequired()])


class PostMarketPlaceForm(FlaskForm):
    title = StringField(render_kw={"placeholder": "Введите название продаваемого продукта"}, validators=[DataRequired(), length(min=10, max=40)])
    litle_inform = StringField(render_kw={"placeholder":"Введите небольшое описание продукта"}, validators=[DataRequired(), length(min=10, max=60)])
    inform_main = StringField(render_kw={"placeholder":"Введите описание продукта"}, validators=[DataRequired(), length(min=20, max=1000)])
    submit = SubmitField(label="Опубликовать")