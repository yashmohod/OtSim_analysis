'''
Simulate a sphere, simply.

'''

import sys
sys.path.append('/home/ymohod/OT_simScripts/depen/brownian_ot')

count=0
import numpy as np
print("import",count,"complete")
count+=1
from numpy import pi
print("import",count,"complete")
count+=1
from brownian_ot import LGBeam
print("import",count,"complete")
count+=1
from brownian_ot.particles import Sphere
print("import",count,"complete")
count+=1
from brownian_ot.simulation import OTSimulation
print("import",count,"complete")
count+=1
import time
print("import",count,"complete")
count+=1
print("All imports Complete!")

'''
        Parameters
        ----------
        wavelen : float
            Incident wavelength in vacuum.
        pol : list, tuple, or ndarray (2)
            Jones vector describing incident polarization state.
            Can be complex if polarization is elliptical.
        NA : float
            Objective lens numerical aperture.
        n_med : float
            Refractive index of medium surrounding particle.
        power : float
            Incident beam power.
'''
polarization = np.array([1,1])*np.sqrt(0.5)

beam = LGBeam(wavelen = 1064e-9,mode= [0,2], pol =[1,0],
            NA = 1.2, n_med = 1.33,
            power = 10e-3) # linear polarization

sph = Sphere(0.4e-6, n_p = 1.45)

sim = OTSimulation(sph, beam, timestep = 1e-5, viscosity = 1e-3,
                   kT = 295*1.38e-23,
                   pos0 = np.array([0, 0, 0]),
                   seed = 1324895)

'''

3) Simulate a sphere in an LG donut beam (e.g., LG02). Extract the radius of the orbit and the orbital period.

'''

start = time.time()
traj = sim.run(500000, outfname = 'traj.npy')
stop = time.time()

print(stop - start)
