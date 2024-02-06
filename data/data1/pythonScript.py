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
from brownian_ot import Beam
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

beam = Beam(wavelen = 1064e-9, pol = [1,0],
            NA = 1.2, n_med = 1.33,
            power = 10e-3) # linear polarization

sph = Sphere(0.4e-6, n_p = 1.45)

sim = OTSimulation(sph, beam, timestep = 1e-5, viscosity = 1e-3,
                   kT = 295*1.38e-23,
                   pos0 = np.array([0, 0, 0]),
                   seed = 1324895)

'''

1) Simulate a sphere held in a point trap (Gaussian beam). Calculate mean-squared displacements in x, y, and z. Then, extract lateral (x-y) and axial (z) trap stiffnesses.

'''

start = time.time()
traj = sim.run(100000, outfname = 'traj.npy')
stop = time.time()

print(stop - start)
