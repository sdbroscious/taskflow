from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired, Optional

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[Optional()])
    priority = SelectField('Priority', 
                         choices=[
                             (1, 'High'), 
                             (2, 'Medium'), 
                             (3, 'Low'), 
                             (4, 'No Priority')
                         ], 
                         coerce=int,
                         default=4)
    submit = SubmitField('Save Task')
