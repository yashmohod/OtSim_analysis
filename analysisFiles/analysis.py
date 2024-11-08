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
    # fp = np.where(F>=0)
    testFFT = np.fft.fft(traj)
    testFFT_mag = np.abs(testFFT)/N
    # f_plot = f[0:int((N/2)+1)]
    # testFFT_mag_plot = 2 * testFFT_mag[0:int((N/2)+1)]
    # testFFT_mag_plot[0] = testFFT_mag_plot[0] /2
    # curmax =0
    # std_passes =0
    max_ind = np.argmax(testFFT_mag)
    
    # for i in range(len(f_plot)):
    #     if testFFT_mag_plot[i] > curmax:
    #         curmax = testFFT_mag_plot[i]
    #         std_passes = f_plot[i]
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
