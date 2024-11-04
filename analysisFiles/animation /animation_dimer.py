from vpython import *
import vpython as vp
from time import *
import numpy as np 
import quaternion as qt
from brownian_ot.brownian_ot import analysis
from PIL import Image
c2 = canvas(width=2000, height=900,background=color.white)


scale = 1
traj = np.load("/Users/mohodyash/Developer/otsim_data/D3/data/LCP_0.02_6983609.npy")

axis_len = 10

scene.background_color = (0.8, 0.8, 0.8)

x = arrow(pos=vector(0,0,0),axis=vector(axis_len,0,0),shaftwidth=0.1, color=color.red)
y = arrow(pos=vector(0,0,0),axis=vector(0,axis_len,0),shaftwidth=0.1, color=color.blue)
z = arrow(pos=vector(0,0,0),axis=vector(0,0,axis_len),shaftwidth=0.1, color=color.green)


upper = sphere(pos=vector(0,0,0), radius=1,texture=textures.rug)
center = sphere(color = color.blue, pos=vector(0,0,0), radius=0.1,make_trail=True,retain=50)
lower = sphere(pos=vector(0,0,0), radius=1,texture=textures.rug)

count =0

c2.camera.pos = vector(1,1,1)
c2.camera.rotate(axis=vec(0,1,1), angle=np.pi, origin=vector(0,0,0))
c2.camera.rotate(axis=vec(0,0,1), angle=-np.pi/2, origin=vector(0,0,0))

aor_pre = []
while (count < len(traj[:,0])):
    qu = np.quaternion(traj[count,3],traj[count,4],traj[count,5],traj[count,6])
    rotMat = qt.as_rotation_matrix(qu)
    aor = qt.as_rotation_vector(qu)

    
    # local position vector of upper and lower sphere of dimer
    upperMat = [0,0,1/1e7]
    lowerMat = [0,0,-1/1e7]

    # traj of each component of the dimer
    mainTraj = [traj[count,0],traj[count,1],traj[count,2]]
    upperTraj = mainTraj + np.matmul(rotMat,upperMat)
    lowerTraj = mainTraj + np.matmul(rotMat,lowerMat)
    
    # movement update
    upper.pos = vector(upperTraj[0] *1e7,upperTraj[1]*1e7,upperTraj[2]*1e7)
    center.pos = vector(mainTraj[0] *1e7,mainTraj[1]*1e7,mainTraj[2]*1e7)
    lower.pos = vector(lowerTraj[0] *1e7,lowerTraj[1]*1e7,lowerTraj[2]*1e7)

    if(count>0):
        theta = np.linalg.norm(aor_pre) *-1
        upper.rotate(axis=vec(aor_pre[0],aor_pre[1],aor_pre[2]), angle=theta, origin=upper.pos)
        lower.rotate(axis=vec(aor_pre[0],aor_pre[1],aor_pre[2]), angle=theta, origin=lower.pos)


    theta = np.linalg.norm(aor) 
    upper.rotate(axis=vec(aor[0],aor[1],aor[2]), angle=theta, origin=upper.pos)
    lower.rotate(axis=vec(aor[0],aor[1],aor[2]), angle=theta, origin=lower.pos)
    aor_pre = aor

    sleep(0.001)
    count+=1