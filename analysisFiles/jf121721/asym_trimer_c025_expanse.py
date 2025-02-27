'''
Simulate an asymmetric trimer with c = 0.25 on Expanse.

'''

import os
import time

import numpy as np
from numpy import pi

from brownian_ot import LGBeam
from brownian_ot.particles import SphereCluster
from brownian_ot.simulation import OTSimulation
from brownian_ot.analysis import expand_trajectory

# Aspect ratio
c = 0.25

def xcm_nondim(c):
    return c**3 * np.sqrt(c**2 + 2*c) / (c**3 + 2)

xcm = xcm_nondim(c)
trimer_coords = np.array([[-xcm, 0, 1], 
                          [-xcm, 0, -1],
                          [np.sqrt(c**2 + 2*c) - xcm, 0, 0]])

a0 = 0.4e-6

scaled_cd = np.load('../asym_trimer_data/asym_trimer_c025_cd.npy')
scaled_dtt = np.load('../asym_trimer_data/asym_trimer_c025_dtt_diag.npy')
scaled_drr = np.load('../asym_trimer_data/asym_trimer_c025_drr_diag.npy')
scaled_dtr = np.load('../asym_trimer_data/asym_trimer_c025_dtr.npy')

Dtt = np.diag(scaled_dtt) / (8 * pi * a0)
Dtr = scaled_dtr / (8 * pi * a0**2)
Drr = np.diag(scaled_drr) / (8 * pi * a0**3)
Ddim = np.vstack((np.hstack((Dtt, Dtr)),
                  np.hstack((Dtr.transpose(), Drr))))


beam = LGBeam(mode = [0, 2], wavelen = 1064e-9, pol = [1,1j],
              NA = 1.2, n_med = 1.33,
              power = 20e-3) # LCP

trimer = SphereCluster(trimer_coords, Ddim, 
                       scaled_cd * a0, a0, n_p = 1.45,
                       a_ratios = np.array([1, 1, c]))


sim = OTSimulation(trimer, beam, timestep = 5e-5, viscosity = 1e-3,
                   kT = 295*1.38e-23,
                   pos0 = np.array([0.5e-6, 0, 0.4e-6]),
                   seed = 2438791)

start = time.time()
traj = sim.run(200000, outfname = 'asym_trimer_a0_4um_c0_25_lg02_lcp_20mW.npy')
stop = time.time()

# print(stop - start)

# # Downsample to millisecond time resolution
# traj_downsampled = traj[::20, :]
# np.save('asym_trimer_a0_4um_c0_25_lg02_lcp_20mW_1ms_exp.npy',
#         expand_trajectory(traj_downsampled))
