import os
import secrets
from flask import render_template, url_for, flash, redirect, request, Blueprint, abort, current_app
from recipeapp import db
from recipeapp.models import Recipe
from flask_login import current_user, login_required
from recipeapp.recipes.forms import RecipeForm

recipes = Blueprint('recipes', __name__)


@recipes.route('/add_recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        if form.picture.data:
            print("Getting Picture")
            photo_file = upload_photo(form.picture.data)
            recipe = Recipe(title=form.title.data, ingredients=form.ingredients.data, directions=form.directions.data, author=current_user, course=form.course.data, notes=form.notes.data, recipe_image=photo_file)
        else:
            recipe = Recipe(title=form.title.data, ingredients=form.ingredients.data, directions=form.directions.data, author=current_user, course=form.course.data, notes=form.notes.data)
        db.session.add(recipe)
        db.session.commit()
        flash(f'{ recipe.title } Added', 'success')
        return redirect(url_for('main.home'))
    return render_template('new_recipe.html', title='A Recipe', form=form, legend="New Recipe")


@recipes.route('/recipe/<int:recipe_id>/')
def recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.recipe_image:
        image_file = url_for('static', filename='recipe_pics/' + recipe.recipe_image)
        return render_template('recipe.html', recipe=recipe, title=recipe.title, image_file=image_file)
    else:
        return render_template('recipe.html', recipe=recipe, title=recipe.title)


@recipes.route('/recipes/<string:course>/', methods=['GET'])
def recipes_course(course):
    recipes = Recipe.query.filter_by(course=course)
    return render_template('recipes.html', recipes=recipes)


@recipes.route('/recipes/search/<string:title>/', methods=['GET', 'POST'])
def recipes_search(title):
    recipes = Recipe.query.filter(Recipe.title.ilike(f"%{title}%"))
    return render_template('recipes.html', recipes=recipes)


@recipes.route('/recipes/search/', methods=['GET', 'POST'])
def recipes_searchb():
    search_text = request.form['search']
    recipes = Recipe.query.filter(Recipe.title.ilike(f"%{search_text}%"))
    return render_template('recipes.html', recipes=recipes)


@recipes.route('/recipe/<int:recipe_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.author != current_user:
        abort(403)
    form = RecipeForm()
    if form.validate_on_submit():
        print("form here")
        if form.picture.data:
            print("Getting Picture")
            photo_file = upload_photo(form.picture.data)
            recipe.recipe_image = photo_file
        recipe.title = form.title.data
        recipe.ingredients = form.ingredients.data
        recipe.directions = form.directions.data
        recipe.course = form.course.data
        recipe.notes = form.notes.data
        db.session.commit()
        flash('Recipe Updated!', 'success')
        return redirect(url_for('recipes.recipe', recipe_id=recipe.id))
    elif request.method == 'GET':
        form.title.data = recipe.title
        form.ingredients.data = recipe.ingredients
        form.directions.data = recipe.directions
        form.course.data = recipe.course
        form.notes.data = recipe.notes
    return render_template('new_recipe.html', title='Edit Recipe', form=form, legend="Edit Recipe")


@recipes.route('/recipe/<int:recipe_id>/delete', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.author != current_user:
        abort(403)
    db.session.delete(recipe)
    db.session.commit()
    flash(f"{ recipe.title } Deleted", 'success')
    return redirect(url_for('main.home'))


def upload_photo(picture_in):
    random_filename = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture_in.filename)
    final_pic = random_filename + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/recipe_pics', final_pic)
    picture_in.save(picture_path)

    return final_pic
