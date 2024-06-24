from flask import Blueprint, render_template


views = Blueprint('views', __name__)


@views.route('/')
def home():
    """where the root is visited what happens"""
    return render_template("home.html")


@views.route('/search_results')
def search_results():
    return render_template("search_results.html")
