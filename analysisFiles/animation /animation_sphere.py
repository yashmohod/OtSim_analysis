from vpython import *
from time import *
import numpy as np 
import quaternion as qt
from brownian_ot.brownian_ot import analysis


c2 = canvas(width=2000, height=900,background=color.white)


scale = 1
traj= analysis.expand_trajectory(np.load(r"/Users/mohodyash/Developer/otsim_data/L1/data/LCP_0.03_2754058.npy"))*scale

axis_len = 10

scene.background_color = (0.8, 0.8, 0.8)

x = arrow(pos=vector(0,0,0),axis=vector(axis_len,0,0),shaftwidth=0.1, color=color.red)
y = arrow(pos=vector(0,0,0),axis=vector(0,axis_len,0),shaftwidth=0.1, color=color.blue)
z = arrow(pos=vector(0,0,0),axis=vector(0,0,axis_len),shaftwidth=0.1, color=color.green)

mySphere1 = sphere( pos=vector(0,0,0), radius=1,make_trail=True,retain=30,texture=textures.earth)

count =0

c2.camera.pos = vector(1,1,1)
c2.camera.rotate(axis=vec(0,1,1), angle=np.pi, origin=vector(0,0,0))
c2.camera.rotate(axis=vec(0,0,1), angle=-np.pi/2, origin=vector(0,0,0))

aor_pre = []
while (count < len(traj[:,0])):
    
    qu = np.quaternion(traj[count,3],traj[count,4],traj[count,5],traj[count,6])
    rotMat = qt.as_rotation_matrix(qu)
    aor = qt.as_rotation_vector(qu)
    
    
    mySphere1.pos = vector(traj[count,0] *1e7,traj[count,1]*1e7,traj[count,2]*1e7)
    
    if(count>0):
        theta = np.linalg.norm(aor_pre) *-1
        mySphere1.rotate(axis=vec(aor_pre[0],aor_pre[1],aor_pre[2]), angle=theta, origin=mySphere1.pos)



    theta = np.linalg.norm(aor) 
    mySphere1.rotate(axis=vec(aor[0],aor[1],aor[2]), angle=theta, origin=mySphere1.pos)
    aor_pre = aor


    sleep(0.001)
    count+=1