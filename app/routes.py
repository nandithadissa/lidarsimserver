#defines the REST api

from app import app
from flask import render_template,flash, redirect
from app.forms import SimulationParamsForm, SimulationResultsForm
from app.simulations.basic import run_simulation
import os

app.config['UPLOAD_FOLDER'] = os.path.join('static','SimResults')

@app.route('/')
@app.route('/index')
def index():
	return render_template('base.html')

@app.route('/simulate',methods=['GET','POST'])
def simulate():
	'''submit parameters for a basic simulation of #-events per pulse vs. distance'''
	form = SimulationParamsForm()
	if form.validate_on_submit():
		avgPower = float(form.avgPower.data)
		bg = float(form.background.data)
		#print('average power:{}'.format(avgPower))
		
		results=run_simulation(avgPower,bg)	#result is an object of SimulationResultsForm
		
		resultForm = SimulationResultsForm()
		#photopath = os.path.join(app.config["UPLOAD_FOLDER"],"result.jpg")
		photopath = os.path.join(app.config["UPLOAD_FOLDER"],results)
		print(photopath)
		resultForm.url = photopath
		resultForm.avgPower = str(avgPower)
		resultForm.background = str(bg)
		return render_template('simulationresults.html',title='simulation results',form=resultForm)
		#return render_template('s.html',title='simulation results',form=resultForm)
	return render_template('simulate.html',title='enter simulation parameters',form=form)
