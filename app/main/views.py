# coding=utf-8
from . import main
from .forms import *
from .. import db, mail
from ..models import *
from flask.ext.login import current_user
from flask import render_template, url_for, redirect, flash, abort

# index:show article-list
@main.route('/')
def index():
    articles = Article.query.order_by(Article.id.desc()).all()
    return render_template('index.html', articles=articles)

# show article
@main.route('/article/<article_id>', methods=['GET', 'POST'])
def article(article_id):
    article = Article.query.filter_by(id=article_id).first()
    if article is None:
        abort(404)
    comments = Comment.query.filter_by(article_id=article_id).all()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment()
        comment.article_id = article_id
        comment.comment = form.comment.data
        if hasattr(current_user, 'id'):
            comment.user_id = current_user.id
        comment.time_stamp = datetime.now()
        db.session.add(comment)
        db.session.commit()
        form.comment.data = ''
        return redirect(url_for('main.article', article_id=article.id))
    return render_template('article_template.html', article=article, comments=comments, form=form)

#  for show user
@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user_tempalte.html', user=user)

# for show messages leave by user
@main.route('/msgboard', methods=['GET', "POST"])
def msgboard():
    msgs = Message.query.order_by(Message.id.desc()).all()
    form = PushMsgForm()
    if form.validate_on_submit():
        message = Message()
        message.message = form.message.data
        if hasattr(current_user, 'id'):
                message.user_id = current_user.id
        db.session.add(message)
        db.session.commit()
        form.message.data = ''
        return redirect(url_for('main.msgboard'))
    return render_template('msgboard.html', msgs=msgs, form=form)

# about site
@main.route('/about')
def about():
    return render_template('about.html')