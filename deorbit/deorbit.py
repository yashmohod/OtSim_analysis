'''
deorbit.py

Jerome Fung

Examine trajectories of orbiting dimers where we need to separate effects
of orbiting from those of spinning.

There are two potential ways to do the de-orbiting: base on the \phi
of the z axis (because the z axis is, fluctuations aside) locked to the orbit,
OR base it on the \phi of the CM.

'''

import numpy as np

def deorbit_particle_axes(traj, via_CM = False):
    '''
    Remove effects of particle CM orbit from the components of the
    particle body axes, collapsing to phi = 0.

    Parameters
    ----------
    traj : ndarray (n x 12)
        Expanded particle trajectory (n rows, columns are 3 CM coordinates,
        u1x, u1y, u1z, u2x, u2y, ..., u3z)
    via_CM : boolean, optional
        If True, use x and y coordinates of CM to determine rotation angle.
        If False, use x and y components of u3.

    Returns
    -------
    traj_deorbit : ndarray (n x 12)
        Particle trajectory with de-orbited particle body axes.

    '''

    if via_CM:
        phis = np.arctan2(traj[:, 1], traj[:, 0])
    else:
        phis = np.arctan2(traj[:, 10], traj[:, 9])

    traj_deorbit = np.zeros(traj.shape)
    traj_deorbit[:, :3] = np.copy(traj[:, :3])
        
    for in_entry, out_entry, phi in zip(traj, traj_deorbit, phis):
        # rotate by -phi
        rot_matrix = np.array([[np.cos(phi), np.sin(phi), 0],
                               [-np.sin(phi), np.cos(phi), 0],
                               [0, 0, 1]])
        out_entry[3:6] = np.matmul(rot_matrix, in_entry[3:6])
        out_entry[6:9] = np.matmul(rot_matrix, in_entry[6:9])
        out_entry[9:12] = np.matmul(rot_matrix, in_entry[9:12])

    return traj_deorbit


        
    
