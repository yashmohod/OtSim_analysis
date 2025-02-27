import numpy as np
import quaternion

def getRadius(traj):
    # radius = np.average(np.sqrt(np.square(traj[:,0])+np.square(traj[:,1])))
    trajx = traj[:,0]
    trajy = traj[:,1]
    
    #trim top
    trajx = trajx[10000:]
    trajy = trajy[10000:]
    #trim bottom
    trajx = trajx[:-10000]
    trajy = trajy[:-10000]
    
    radius  = np.average(np.hypot(trajx,trajy))
    # sd = np.std(np.hypot(trajx,trajy))/np.sqrt(len(trajy))
    sd = np.std(np.hypot(trajx,trajy))
    return radius, sd


def getfreq (traj):
    N = len(traj)
    fs = 1e5
    fstep = fs/N
    f = np.linspace(0,int(N-1)*fstep,N)
    F = np.fft.fftfreq(N,1/fs)
    testFFT = np.fft.fft(traj)
    testFFT_mag = np.abs(testFFT)/N

    max_ind = np.argmax(testFFT_mag)
    
    return F[max_ind]



def expand_trajectory(traj):
    '''
    Code saves trajectories as x, y, z, a, b, c, d where the
    a, b, c, d are quaternion elements. 
    Expand to provide full rotation matrix.

    Rows of output are now
    x, y, z, u1x, u1y, u1z, u2x, u2y, u2z, u3x, u3y, u3z
    '''

    # convert relevant elements of ndarrays to an array of quaternions
    quat_array = quaternion.from_float_array(traj[:, 3:])
    # now convert to array of rotation matrices
    rot_matrices = quaternion.as_rotation_matrix(quat_array)
    # transpose for convenience (so we can access unit vectors)
    # and reshape
    n_pts = traj.shape[0]
    rot_matrices = np.transpose(rot_matrices,
                                axes = (0,2,1)).reshape((n_pts, 9))
    output = np.hstack((traj[:,0:3], rot_matrices))
    return output



'''
deorbit.py

Jerome Fung

Examine trajectories of orbiting dimers where we need to separate effects
of orbiting from those of spinning.

There are two potential ways to do the de-orbiting: base on the \phi
of the z axis (because the z axis is, fluctuations aside) locked to the orbit,
OR base it on the \phi of the CM.
'''

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


