# coding=utf-8
from flask.ext.login import login_user, logout_user, login_required, current_user
from flask import flash, render_template, redirect, url_for, abort
from . import admin
from .forms import *
from ..models import *

@admin.route('/', methods=["POST", "GET"])
@login_required
def add_articles():
    role = Role.query.filter_by(id=current_user.role_id).first()
    if not role.is_admin:
        abort(404)
    form = AddArtForm()
    if form.validate_on_submit():
        article = Article()
        article.title = form.title.data
        article.text = form.text.data
        db.session.add(article)
        db.session.commit()
        flash("Add success")
        form.title.data = ""
        form.text.data = ""
    return render_template("admin/add_articles.html", form=form)



