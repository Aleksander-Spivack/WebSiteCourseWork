from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

main = Blueprint('main', __name__)


@main.route('/')
def base():
    return render_template('MarketPlace.html')


@main.route('/profile')
@login_required
def profile():

    return render_template('ProfileMarket.html', name=current_user.name)


@main.route('/profile/articles', methods=['POST', 'GET'])
def articles_create():
    from __init__ import Article
    from __init__ import db

    if current_user.is_authenticated:
        title = request.form.get('title')
        intro = request.form.get('intro')
        textFor = request.form.get('textFor')

        if request.method == 'POST':
            if not (title or intro or textFor):
                flash('Заполните все поля!')
            else:
                new_post = Article(title=title, intro=intro, textFor=textFor)
                db.session.add(new_post)
                db.session.commit()
                return redirect(url_for('main.posts'))

        return render_template('ArticlePost.html')
    else:
        return redirect(url_for('auth.login'))
        flash('Войдите в аккаунт для публикации статей')


@main.route('/posts')
def posts():
    from __init__ import Article
    posts = Article.query.order_by(Article.id.desc()).all()
    return render_template('articles.html', posts=posts)


@main.route('/posts/<int:id>')
def post_detail(id):
    from __init__ import Article
    article = Article.query.get(id)

    return render_template('Posts.html', article=article)


@main.route('/contact/form', methods=['POST', 'GET'])
def contactForm():
    return render_template('contactForm.html')


@main.route('/marketplace/content', methods=['POST', 'GET'])
def category_servise():
    return render_template('MarketContent.html')

@main.route('/marketplace/posts_content', methods=['POST', 'GET'])
def postcontent():
    from forms import PostMarketPlaceForm
    from __init__ import User, Product, db

    form = PostMarketPlaceForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():

            new_product = Product(title=form.title.data, intro=form.litle_inform, maintext=form.inform_main)

            db.session.add(new_product)
            db.session.commit()
            return redirect(url_for('main.category_servise'))
    else:
        return redirect(url_for('auth.login'))

    return render_template('MarketplacePost.html', form=form)