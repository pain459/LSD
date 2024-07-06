from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

class EmployeeForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    middle_name = StringField('Middle Name', validators=[Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    sex = StringField('Sex', validators=[DataRequired(), Length(max=10)])
    age = IntegerField('Age', validators=[DataRequired()])
    designation = StringField('Designation', validators=[DataRequired(), Length(max=100)])
    employee_id = StringField('Employee ID', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')
