from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()])
    directions = TextAreaField('Directions', validators=[DataRequired()])
    course = SelectField('Course', choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('dinner', 'Dinner'), ('drink', 'Drink'), ('snack', 'Snack')], validators=[DataRequired()])
    notes = TextAreaField('Notes:')
    picture = FileField('Add A Recipe Picture?', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')
