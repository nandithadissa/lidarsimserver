#class holds all the parameters needed for running the simulations

class Params(object):
	avgPower = 		20		# mW, average power mW
	wavelength = 	780 	# nm, wavelength
	repRate = 		1E3		# Hz, laser repition rate
	jitter	= 		230		# ps, laser 
	R		=		0.1		# none, reflection coefficient
	BG		=		500		# W/m2, background illumination ->> convert to LUX using white light luminous intensity (1050 W/m2 == 98 klux)
	pixels_X =		256		# #, pixels x direciton
	pixels_Y = 		256 	# #, pixels y direction
	PDP =			0.1		# none, pdp
	FF =			0.5 	# none, FF
	F_no	=		1.4		# none, F - numbers
	Tlens	=		0.8		# none, lens efficiency
	BW		=		20		# nm, passband of the filter
	Tfilter = 		0.7		# none, filter efficiency
	theta_H	=		20		# degrees, HFOV	
	theta_V = 		20		# degrees, VFOV
	pixelSize =		20.0	# um, pixel width assuming rectangle
	DCR		=		1E3		# cp/um2, average DCR per pixel
	gateTime = 		1		# us, range gate time
	registerWidth = 12		# #-bits, counter size
	
class Results(object):
	'''holds the urls'''
	url_sn_events = ""
	url_snr = ""
	url_stats = ""
	url_tcspc = ""	
	
