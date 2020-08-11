#recreating the results of the paper 2918_modeling_analysis_dtof_charbon_preethi
#this is part of the Lidar simulation

#date: 08/03/2020 
#This is to calculate the signal to noise ratio in a given lidar system and
#examine the different methods of increasin SNR

import numpy as np
import matplotlib.pyplot as plt
#from blackbody import bb_fraction
font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 14 }
import matplotlib
matplotlib.rc('font', **font)
from scipy import constants
import math
import time

from uuid import uuid4

#blackbody radiation
def bb(start=200,end=4000,step=10): #nm
	
	wavelength = np.arange(start,end,step) #nm
	c = constants.speed_of_light
	h = constants.Planck
	k = constants.Boltzmann
	T = 6000 

	
	freq = np.array([c/(w*1e-9) for w in wavelength])
	B = np.array([(2*h*f**3/c**2)*(1/(np.exp(h*f/(k*T))-1)) for f in freq])

	#plt.plot(freq,B)
	#plt.show()
	
	#power
	P = np.trapz(B,dx=10*1e-9)
	print(P)

	return P


#fraction of power within the spectrum
def bb_fraction(center,bandwidth):
	All = bb(100,10000,10)
	BW = bb(center-bandwidth*0.5,center+bandwidth*0.5,10)
	fraction = BW/All
	return fraction	


#
def run_simulation(params):	#class object of the Params
	
	Pavg = params.avgPower #20 							#mW - average laser power
	wavelength = params.wavelength #780					#nm - wavelength
	rep_rate = params.repRate#1E3						#MHz - RepRate
	FWHM = params.jitter#540 							#ps	- Jitter
	R = params.R#0.1								#% - reflectivity
	BG = params.BG #500							#W/m2 - expressed in klux
	pixels_x = params.pixels_X# 32.0
	pixels_y = params.pixels_Y#32.0
	RES = pixels_x * pixels_y			#sensor format
	PDP = params.PDP#0.1							#% - PDP
	FF = params.FF#0.5							#% - FF
	#Dlens = 11							#mm - Diameter of the lens
	F_no = params.F_no#1.4							#F/#
	#Focallength = F_no*Dlens 			#16mm 
	Tl = params.Tlens#0.8							#lens efficiency
	Delta_BW = params.BW#20						#nm optical passband
	Tf = params.Tfilter#0.7 							#filter efficiency
	theta_h = np.radians(params.theta_H)			#horizontal AFOV
	theta_v = np.radians(params.theta_V)			#vertical AFOV
	C = constants.c						#speed of light
	pixel_size = params.pixelSize#20.0					#um
	pixel_area = pixel_size * pixel_size #um2
	DCR = params.DCR#1E3 							#cp/um2 ==> 1E5 counts per pixel 

	energy = (1240/wavelength)*1.602E-19 #J

	tmeasure = 1E-6						#s, gate-time
	range_measure = (tmeasure/2)*C		#range measred	
	print("range:%f m"%range_measure)

	
	D = np.arange(0,1000,0.2) 			#m distance
	
	BW_power = bb_fraction(wavelength,Delta_BW)
	
	def _pnoise():
		#a = BG*np.tan(theta_h/2.0)*np.tan(theta_v/2.0)*R*BW_power*((Dlens*1E-3)**2)*Tl*Tf*(2/np.pi)*(1/RES)
		a = BG*BW_power*R*((1/(2*F_no))**2)*Tl*Tf*(2/np.pi)*pixel_area*1E-12
		return a
	
	Pnoise = [_pnoise()*PDP*FF*(1/energy) + (DCR*pixel_area)  for i in D]
	
	def _psignal(d):
		#a = Pavg*1E-3*R*((Dlens*1e-3/(2*d))**2)*Tl*Tf*(2/np.pi)*(1/RES)
		a = Pavg*1E-3*R*((1/(2*F_no))**2)*Tl*Tf*(2/np.pi)*pixel_area*1e-12*(1/(2*d*np.tan(theta_v/2)))**2
		return a
		
	Psignal = [_psignal(d)*PDP*FF*(1/energy) for d in D]

	SignalEvents_per_pulse = [s/rep_rate for s in Psignal]
	#NoiseEvents_per_pulse  = [n/rep_rate for n in Pnoise]
	NoiseEvents_per_pulse  = [n*tmeasure for n in Pnoise]

	SNR = [10*np.log10(s/n) for s,n in zip(SignalEvents_per_pulse,NoiseEvents_per_pulse)]

	plt.close()	
	plt.loglog(D,SignalEvents_per_pulse,label='signal events')
	plt.loglog(D,NoiseEvents_per_pulse,label='noise events')
	plt.grid(b=True, which='major', color='k', linestyle='-')
	plt.minorticks_on()
	plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.2),
	plt.xlabel('Distance (m)')
	plt.ylabel('# events per pulse')
	plt.title("Number of signal and noise event per pixel",fontsize=12)
	plt.legend()
	#plt.show()
	url_sn_events = 'result_%s.jpg'%(str(uuid4().hex))
	plt.savefig('./app/static/SimResults/%s'%url_sn_events)
	
	time.sleep(1)

	plt.close()
	#s/n
	plt.semilogx(D,SNR,label='S/N')
	plt.grid(b=True, which='major', color='k', linestyle='-')
	plt.minorticks_on()
	plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.2),
	plt.xlabel('Distance (m)')
	plt.ylabel('SNR (dB)')
	plt.title(" S/N per pulse",fontsize=12)
	plt.legend()
	#plt.show()
	url_snr = 'result_%s.jpg'%(str(uuid4().hex))
	plt.savefig('./app/static/SimResults/%s'%url_snr)

	time.sleep(1)
	#run stats
	url_stats=stats(D,SignalEvents_per_pulse,NoiseEvents_per_pulse,params)

	time.sleep(1)
	#run tcspc
	url_tcspc=tcspc(D,SignalEvents_per_pulse,NoiseEvents_per_pulse,params)

	time.sleep(1)
	#return D,SignalEvents_per_pulse,NoiseEvents_per_pulse
	return url_sn_events, url_snr, url_stats, url_tcspc


#statistics
def stats(D,SignalEvents,NoiseEvents,params): #per pulse
	'''probability of detecting a signal'''
	
	'''Pd = P(N=0)*P(S>0) - Probability of no noise counts * non-zero signal count'''
	
	tmeasure = params.gateTime*1E-6 #1um range-gate
	C = constants.c						#speed of light

	'''
	def P_noise(k):
		return (NoiseEvents**k * np.exp(-1*NoiseEvents))/math.factorial(k))
	
	def P_signal(k):
		return (SignalEvents**k * np.exp(-1*SignalEvents))/math.factorial(k))
	'''
	
	Pzero_noise = [np.exp(-1*n) for n in NoiseEvents] #zero noise events
	Pzero_signal = [np.exp(-1*n) for n in SignalEvents] #zero signal events


	Psignal = [pzn*(1-pzs) for pzn,pzs in zip(Pzero_noise,Pzero_signal)] 
	Pnoise = [(pzs)*(1-pzn) for pzn,pzs in zip(Pzero_noise,Pzero_signal)] 

	#print("detection probabilities for t=%fs, Psig=%.2f, Pnoise=%.2f"%(tmeasure,Psig,Pnoise))
	
	max_distance = 0.5*tmeasure*C

	plt.close()
	plt.plot(D,Psignal,label='signal')
	plt.plot(D,Pnoise,label='noise')
	plt.grid(b=True, which='major', color='k', linestyle='-')
	plt.minorticks_on()
	plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.2),
	plt.xlabel('Distance (m)')
	plt.ylabel('Signal and Noise detection probability')
	plt.title(" Probability of signal and noise event within the Gate Time",fontsize=12)
	plt.xlim(0,max_distance)
	plt.legend()
	#plt.show()
	url_stats = 'result_%s.jpg'%(str(uuid4().hex))
	plt.savefig('./app/static/SimResults/%s'%url_stats)
	return url_stats

	
#TCSPC and concidence detection to increase signal to noise
def tcspc(D,SignalEvents,NoiseEvents,params): #per pulse
	'''calculate the minimum number of shots needed to get S/N > 1 with tcspc'''

	''' noise is uniformly distributed, signal is guassian with mean at D 
		higher number of shots will reduce the noise and add to the signal'''

	jitter = params.jitter*1E-12 #500 ps
	#rep_rate = 1E3	 #Hz
	C = constants.c						#speed of light
	#signal_mean = [2*d/C for d in D] 	#time the signal arrives 
	tmeasure = params.gateTime*1E-6 #s
	shots = int(params.laserShots)	
	shot_inc = int(shots/10)
	bits = params.registerWidth

	counter_bits = params.registerWidth
	bins = 2**bits
	bin_time = 	tmeasure/bins #number of bins
	noise_floor = [n for n in NoiseEvents]
	
	#shots = range(1,10,1) #0 - 10 laser shots
	shots = range(1,shots,shot_inc) #0 - 10 laser shots
	signal_bins = np.floor(2*jitter/bin_time) #2*jitter/bin
	if signal_bins == 0:
		signal_bins = 1

	print("signal_bins=%d"%signal_bins)
	signal_floor = [n/signal_bins for n in SignalEvents]

	max_distance = 0.5*tmeasure*C

	plt.close()
	print(shots)
	for shot in shots:
		snr = [10*np.log10(shot*sf/nf) for sf,nf in zip(signal_floor,noise_floor)]
		plt.plot(D,snr,label='shot %d'%shot)
		plt.xlim(0,max_distance)
		plt.grid(b=True, which='major', color='k', linestyle='-')
		plt.minorticks_on()
		plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.2),
		plt.xlabel('Distance (m)')
		plt.ylabel('S/N with for different laser shots (dB)')
		plt.title(" Improvement of the S/N using multi-laser shots in TCSPC mode",fontsize=12)
		plt.legend(fontsize=9)

	#plt.show()
	url_tcspc = 'result_%s.jpg'%(str(uuid4().hex))
	plt.savefig('./app/static/SimResults/%s'%url_tcspc)
	return url_tcspc

	
if __name__ == "__main__":
	pass
	#D,SignalEvents,NoiseEvents=snr() #within tmeasure integration
	#stats(D,SignalEvents,NoiseEvents)
	#tcspc(D,SignalEvents,NoiseEvents)
