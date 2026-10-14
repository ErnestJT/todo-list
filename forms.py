from wtforms import StringField, SubmitField, ColorField, DateField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

class CategoryAddForm(FlaskForm):
    category_add_field = StringField(default='Add a new category...', )
    submit_field = SubmitField(label='Submit')

class TaskAddForm(FlaskForm):
    task_add_field = StringField(default='Add a new task...')
    submit_field = SubmitField(label='Submit')

class CategoryDeleteForm(FlaskForm):
    delete_field = SubmitField(label='Delete Category')

class TaskEditForm(FlaskForm):
    color_field = ColorField(label='Color:', validators=[DataRequired()], default="#ffffff")
    name_field = StringField(label='Name:', validators=[DataRequired()])
    date_field = DateField(label='Due Date:', validators=[DataRequired()])
    submit_field = SubmitField(label='Submit')
