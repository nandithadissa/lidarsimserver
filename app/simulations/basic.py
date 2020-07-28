#recreating the results of the paper 2918_modeling_analysis_dtof_charbon_preethi
#this is part of the Lidar simulation

import numpy as np
import matplotlib.pyplot as plt
font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 14 }
import matplotlib
matplotlib.rc('font', **font)

from scipy import constants
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

#if __name__ == "__main__":
#	print(bb_fraction(780,20))

def run_simulation(_Pavg=20,_BG=500):

	Pavg = _Pavg 			#mW - average laser power
	wavelength = 780	#nm - wavelength
	rep_rate = 1E6		#MHz - RepRate
	FWHM = 540 			#ps	- Jitter
	R = 0.1				#% - reflectivity
	BG = _BG		#W/m2 - expressed in klux
	RES = 1024.00			#sensor resolution
	PDP = 0.1		#% - PDP
	FF = 0.5			#% - FF
	Dlens = 11			#mm - Diameter of the lens
	F_no = 1.4			#F/#
	Focallength = 15	#mm 
	Tl = 0.8			#lens efficiency
	Delta_BW = 20		#nm optical passband
	Tf = 0.7 			#filter efficiency
	theta_h = np.radians(20)		#horizontal AFOV
	theta_v = np.radians(20)	#vertical AFOV
	
	energy = (1240/wavelength)*1.602E-19 #J

	tmeasure = 20E-9 #measurement time
	
	D = np.arange(0,100,0.2) #m distance
	
	BW_power = bb_fraction(wavelength,Delta_BW)
	
	def _pnoise():
		a = BG*np.tan(theta_h/2.0)*np.tan(theta_v/2.0)*R*BW_power*((Dlens*1E-3)**2)*Tl*Tf*(2/np.pi)*(1/RES)
		return a
	
	Pnoise = [_pnoise()*PDP*FF*(1/energy) for i in D]
	
	def _psignal(d):
		return Pavg*1E-3*R*((Dlens*1e-3/(2*d))**2)*Tl*Tf*(2/np.pi)*(1/RES)
		
	Psignal = [_psignal(d)*PDP*FF*(1/energy) for d in D]

	SignalEvents_per_pulse = [s/rep_rate for s in Psignal]
	#NoiseEvents_per_pulse  = [n/rep_rate for n in Pnoise]
	NoiseEvents_per_pulse  = [n*tmeasure for n in Pnoise]
	
	#print(D)
	#print(Pnoise)
	#print(Psignal)

	plt.figure(figsize=(16,8))
	plt.loglog(D,SignalEvents_per_pulse,label='signal events')
	plt.loglog(D,NoiseEvents_per_pulse,label='noise events')
	plt.grid(b=True, which='major', color='k', linestyle='-')
	plt.minorticks_on()
	plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.2),
	plt.xlabel('Distance (m)')
	plt.ylabel('# events per pulse')
	plt.legend()
	#plt.show()
	filename = 'result_%s.jpg'%(str(uuid4().hex))
	plt.savefig('./app/static/SimResults/%s'%filename)
	url = filename#'./app/static/SimResults/%s'%filename 
	return url

	
if __name__ == "__main__":
	run_simulation()
	
