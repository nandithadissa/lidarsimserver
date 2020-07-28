#model blackbody radiation

import numpy as np
import matplotlib.pyplot as plt
from scipy import constants


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

if __name__ == "__main__":
	print(bb_fraction(780,20))
	
