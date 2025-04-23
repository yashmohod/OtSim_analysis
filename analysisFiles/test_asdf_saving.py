'''
play around with including metadata
'''

import sys
sys.path.append('/Users/jfung/code/brownian_ot')

import numpy as np
from numpy import pi, exp

from brownian_ot import LGBeam
from brownian_ot.particles import Sphere
from brownian_ot.simulation import OTSimulation

import asdf
from asdf import AsdfFile


seed = 12345

pos_0 = np.array([0.6e-6, 0, 0.8e-6])

beam = LGBeam(mode = [0,3], wavelen = 1064e-9, pol = np.array([1, 1j]),
              NA = 1.2, n_med = 1.33, power = 20e-3)
sphere = Sphere(a = 0.4e-6, n_p = 1.45+0.001j)
sim = OTSimulation(sphere, beam, timestep = 1e-5, viscosity = 1e-3,
                   kT = 295 * 1.38e-23, seed = seed, pos0 = pos_0,
                   orient0 = np.identity(3))

traj = sim.run(10000, outfname = 'raw_trajectory.npy') # save on our own

# If we're happy with this, code should be refactored so that objects
# know how to serialize themselves

particle_dict = {
    'type' : sphere.__class__.__name__,
    'radius' : sphere.a,
    'refractive_index' : sphere.n_p,
    'diffusion_tensor' : sphere.Ddim,
    'center_of_diffusion' : sphere.cod
}

beam_dict = {
    'type' : beam.type,
    'mode' : beam.mode,
    'wavelength' : beam.wavelen,
    'polarization' : beam.pol,
    'NA' : beam.NA,
    'medium_index' : beam.n_med,
    'power' : beam.power
}


simulation_dict = {
    'timestep' : sim.timestep,
    'type' : sim.__class__.__name__,
    'seed' : sim.rng_seed,
    'viscosity' : sim.viscosity,
    'kT' : sim.kT,
    'n_steps' : len(traj) - 1
}

tree = {
    'trajectory' : traj,
    'particle' : particle_dict,
    'beam' : beam_dict,
    'simulation' : simulation_dict
}

ff = AsdfFile(tree)
ff.write_to('sphere_asdf_test.asdf')

simulation_dict['downsampled_timestep'] = 1e-3

tree2 = {
    'trajectory' : traj.copy(),
    'particle' : particle_dict,
    'beam' : beam_dict,
    'simulation' : simulation_dict
}

ff2 = AsdfFile(tree2)
ff2.write_to('sphere_asdf_test_downsampled1ms.asdf')
