#forms required to enter data

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, SelectField, HiddenField, DecimalField, TextAreaField, TextField
from wtforms.validators import DataRequired, Email, Length


#get simulation parameters
class SimulationParamsForm(FlaskForm):
	'''enter all the parameters form the simulation'''
	avgPower = StringField('Average Laser Power (mW)', validators= [DataRequired(), Length(max=32)], default=20)
	BG = StringField('Background (W/m2)', validators= [DataRequired(), Length(max=32)], default=500)
	wavelength = StringField('Wavelength (nm)', validators= [DataRequired(), Length(max=32)], default=780)
	jitter = StringField('system jitter (ps)', validators= [DataRequired(), Length(max=32)], default=200)
	R = StringField('target reflectivity (ps)', validators= [DataRequired(), Length(max=32)], default=0.1)
	PDP = StringField('PDP', validators= [DataRequired(), Length(max=32)], default=0.1)
	FF = StringField('FF', validators= [DataRequired(), Length(max=32)], default=0.5)
	F_no = StringField('F/#', validators= [DataRequired(), Length(max=32)], default=1.4)
	Tlens = StringField('Lens efficiency', validators= [DataRequired(), Length(max=32)], default=0.8)
	Tfilter = StringField('Filter efficiency', validators= [DataRequired(), Length(max=32)], default=0.7)
	BW = StringField('Filter bandwidth (nm)', validators= [DataRequired(), Length(max=32)], default=20)
	theta_H = StringField('HFOV (degrees)', validators= [DataRequired(), Length(max=32)], default=20)
	theta_V = StringField('VFOV (degrees)', validators= [DataRequired(), Length(max=32)], default=20)
	pixelSize = StringField('Pixel size (um)', validators= [DataRequired(), Length(max=32)], default=20)
	DCR = StringField('DCR (cp/um2)', validators= [DataRequired(), Length(max=32)], default=1000)
	gateTime = StringField('Gate time (us)', validators= [DataRequired(), Length(max=32)], default=1)
	registerWidth = StringField('# bits in counter ', validators= [DataRequired(), Length(max=32)], default=12)
	submit = SubmitField('Run')

#view simulation results
class SimulationResultsForm(FlaskForm):
	'''show the results of the simulation'''
	url_sn_events = ""
	url_snr = ""
	url_stats = ""
	url_tcspc = ""
	avgPower= ""
	background = ""
