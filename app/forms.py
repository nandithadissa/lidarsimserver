#forms required to enter data

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, SelectField, HiddenField, DecimalField, TextAreaField, TextField
from wtforms.validators import DataRequired, Email, Length


#get simulation parameters
class SimulationParamsForm(FlaskForm):
	'''enter all the parameters form the simulation'''
	avgPower = StringField('Average Laser Power (mW)', validators= [DataRequired(), Length(max=32)])
	background = StringField('Background (W/m2)', validators= [DataRequired(), Length(max=32)])
	submit = SubmitField('Run')

#view simulation results
class SimulationResultsForm(FlaskForm):
	'''show the results of the simulation'''
	url = ""
	avgPower= ""
	background = ""
