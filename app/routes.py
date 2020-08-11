#defines the REST api

from app import app
from flask import render_template,flash, redirect
from app.forms import SimulationParamsForm, SimulationResultsForm
#from app.simulations.basic import run_simulation
from app.simulations.snr_lidar import run_simulation
import os
from app.simulations.parameters import Params

app.config['UPLOAD_FOLDER'] = os.path.join('static','SimResults')

@app.route('/')
@app.route('/index')
def index():
	return render_template('base.html')

@app.route('/wiki')
def wiki():
	return render_template('wiki.html')

@app.route('/simulate',methods=['GET','POST'])
def simulate():
	'''submit parameters for a basic simulation of #-events per pulse vs. distance'''
	form = SimulationParamsForm()
	if form.validate_on_submit():
		params = Params
		params.avgPower = float(form.avgPower.data)
		params.repRate = float(form.repRate.data)
		params.BG = float(form.BG.data)
		params.jitter = float(form.jitter.data)
		params.R = float(form.R.data)
		params.BW = float(form.BW.data)
		params.pixelSize = float(form.pixelSize.data)
		params.PDP = float(form.PDP.data)
		params.FF = float(form.FF.data)
		params.Tlens = float(form.Tlens.data)
		params.Tfilter = float(form.Tfilter.data)
		params.F_no = float(form.F_no.data)
		params.theta_H = float(form.theta_H.data)
		params.theta_V = float(form.theta_V.data)
		params.DCR = float(form.DCR.data)
		params.gateTime = float(form.gateTime.data)
		params.registerWidth = float(form.registerWidth.data)
		params.laserShots = float(form.laserShots.data)
		
		#print('average power:{}'.format(avgPower))
		url_sn_events,url_snr,url_stats,url_tcspc=run_simulation(params)	#result is an object of SimulationResultsForm
		
		resultForm = SimulationResultsForm()
		#photopath = os.path.join(app.config["UPLOAD_FOLDER"],"result.jpg")
		resultForm.url_sn_events = os.path.join(app.config["UPLOAD_FOLDER"],url_sn_events)
		resultForm.url_snr = os.path.join(app.config["UPLOAD_FOLDER"],url_snr)
		resultForm.url_stats = os.path.join(app.config["UPLOAD_FOLDER"],url_stats)
		resultForm.url_tcspc = os.path.join(app.config["UPLOAD_FOLDER"],url_tcspc)
		
		params_dic = {	"Average Power (mW)":params.avgPower,
						"Rep rate (Hz)": params.repRate,
						"Background intensity (W/sq-m)":params.BG,
						"Jitter (ps)":params.jitter,
						"Reflectivity":params.R,
						"Filter bandgap (nm)":params.BW,
						"Pixel size (um)":params.pixelSize,
						"PDP": params.PDP,
						"Fill Factor":params.FF,
						"Lens optical transmission":params.Tlens,
						"Filter optical transmission":params.Tfilter,
						"F/#": params.F_no,
						"Horizontal Field of View (degrees)":params.theta_H,
						"Vertical Field of View (degrees)":params.theta_V,
						"DCR (Hz/um2)": params.DCR,
						"Ragegate time (us)": params.gateTime,
						"# Bits in counter" : params.registerWidth,
						"Laser shots for TCSPC mode" : params.laserShots
					}
		resultForm.params = params_dic
		#print(photopath)
		#resultForm.url = photopath
		resultForm.avgPower = str(params.avgPower)
		resultForm.background = str(params.BG)
		return render_template('simulationresults.html',title='simulation results',form=resultForm)
		#return render_template('s.html',title='simulation results',form=resultForm)
	return render_template('simulate.html',title='enter simulation parameters',form=form)
