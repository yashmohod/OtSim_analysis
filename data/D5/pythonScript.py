import sys
sys.path.append('/home/ymohod/OT_simScripts/depen/brownian_ot')

count=0
import numpy as np
from numpy import pi
from brownian_ot import LGBeam
from brownian_ot.particles import Sphere
from brownian_ot.simulation import OTSimulation
import random

if __name__ == "__main__":
    random.seed(10)

    pol = float(sys.argv[1:][0])
    por = float(sys.argv[1:][1])*10e-3
    polarization = np.array([1,1])*np.sqrt(0.5)
    if(pol==1):
        #LCP
        polarization = [1*float(np.sqrt(0.5)),1j*float(np.sqrt(0.5))]
    else:
        #RCP
        polarization = [1*float(np.sqrt(0.5)),-1j*float(np.sqrt(0.5))]

    beam = LGBeam(wavelen = 1064e-9,mode=[0,5] ,pol = polarization,
                NA = 1.2, n_med = 1.33,
                power = por) # linear polarization

    sph = Sphere(0.4e-6, n_p = 1.45)
    curseed = int(random.random()*1e7)
    print("All fine till here")
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
    traj = sim.run(500000, outfname = "data/"+ploN+"_"+str(por)+"_"+str(curseed)+".npy")

