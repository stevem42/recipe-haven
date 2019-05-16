from flask import render_template, Blueprint
from recipeapp.models import Recipe

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    recipes = Recipe.query.order_by(Recipe.date_posted.desc())
    return render_template('home.html', recipes=recipes)
