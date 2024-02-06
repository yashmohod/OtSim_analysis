'''
Simulate a sphere, simply.

'''

 
sys.path.append('/Users/ymohod/Developer/ot_sim/dataAnalysis/brownian_ot')

count=0
import numpy as np
from numpy import pi
from brownian_ot import Beam
from brownian_ot.particles import Dimer
from brownian_ot.simulation import OTSimulation
import random

if __name__ == "__main__":
    random.seed(10)

    pol = float(sys.argv[1:][0])
    por = float(sys.argv[1:][1])
    polarization = np.array([1,1])*np.sqrt(0.5)
    if(pol==1):
        #LCP
        polarization = np.array([1,1j])*np.sqrt(0.5)
    else:
        #RCP
        polarization = np.array([1,-1j])*np.sqrt(0.5)

    beam = Beam(wavelen = 1064e-9, pol = polarization,
                NA = 1.2, n_med = 1.33,
                power = por*10e-3) # linear polarization

    sph = Dimer(0.4e-6, n_p = 1.45)
    curseed = int(random.random()*1e10)
    sim = OTSimulation(sph, beam, timestep = 1e-5, viscosity = 1e-3,
                    kT = 295*1.38e-23,
                    pos0 = np.array([0, 0, 0]),
                    seed = curseed)
    # pol_power_curseed
    ploN = "L"
    if pol ==1:
        ploN = "LCP"
    else:
        ploN = "RCP"
    traj = sim.run(100, outfname = ploN+"_"+str(por)+"_"+str(curseed)+".npy")