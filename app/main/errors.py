from . import main
from flask import render_template

@main.app_errorhandler(404)
def page_404(e):
    return render_template('errors/404.html'), 404

@main.app_errorhandler(500)
def page_500(e):
    return  render_template('errors/500.html'), 500