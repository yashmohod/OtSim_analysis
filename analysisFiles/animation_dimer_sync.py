
from vpython import *
import vpython as vp
from time import *
import numpy as np 
import quaternion as qt
# from brownian_ot.brownian_ot import analysis
from PIL import Image

from scipy.spatial.transform import Rotation as R

c2 = canvas(width=2000, height=900,background=color.white)



axis_len = 10


time = np.arange(0,100*np.pi,np.pi/(2**6)) 

traj = np.zeros((len(time),3))

traj[:,0]=1
traj[:,1]=1
traj[:,2]=1

scene.background_color = (0.8, 0.8, 0.8)

x = arrow(pos=vector(0,0,0),axis=vector(axis_len,0,0),shaftwidth=0.1, color=color.red)
y = arrow(pos=vector(0,0,0),axis=vector(0,axis_len,0),shaftwidth=0.1, color=color.blue)
z = arrow(pos=vector(0,0,0),axis=vector(0,0,axis_len),shaftwidth=0.1, color=color.green)


upper = sphere(pos=vector(0,0,0), radius=1,texture=textures.rug)
center = sphere(color = color.blue, pos=vector(0,0,0), radius=0.1,make_trail=True,retain=50)
lower = sphere(pos=vector(0,0,0), radius=1,texture=textures.rug)

count =1

c2.camera.pos = vector(1,1,1)
c2.camera.rotate(axis=vec(0,1,1), angle=np.pi, origin=vector(0,0,0))
c2.camera.rotate(axis=vec(0,0,1), angle=-np.pi/2, origin=vector(0,0,0))


while (count < len(traj[:,0])):

    # z axis rotation
    matnorz = np.array(
        [
            [np.cos(time[count]),-np.sin(time[count])   ,0],
            [np.sin(time[count]),np.cos(time[count])    ,0],
            [0                  ,0                  ,1]
        ]
    )
    
    # x axis rotation
    matnorx = np.array(
        [
            [1,0,0],
            [0,np.cos(time[count]),-np.sin(time[count]) ],
            [0,np.sin(time[count]),np.cos(time[count])]
        ]
    )

    # y axis rotation
    matnory = np.array(
        [
            [np.cos(time[count]),0,np.sin(time[count])],
            [0,1,0 ],
            [-np.sin(time[count]),0,np.cos(time[count])]
        ]
    )
    
    qu = qt.from_rotation_matrix(matnorx)
    rotMat = qt.as_rotation_matrix(qu)
    aor = qt.as_rotation_vector(qu)
    
    
    # local position vector of upper and lower sphere of dimer
    upperMat = np.array([0,0,1])
    lowerMat = np.array([0,0,-1])

    # traj of each component of the dimer
    mainTraj = [traj[count,0],traj[count,1],traj[count,2]]
    upperTraj =  mainTraj+ np.matmul(rotMat,upperMat)
    lowerTraj = mainTraj +np.matmul(rotMat,lowerMat)


    # movement update
    upper.pos = vector(upperTraj[0],upperTraj[1],upperTraj[2])
    center.pos = vector(mainTraj[0],mainTraj[1],mainTraj[2])
    lower.pos = vector(lowerTraj[0],lowerTraj[1],lowerTraj[2])

    theta= np.linalg.norm(aor)    
   

    
    upper.rotate(axis=vec(aor[0],aor[1],aor[2]), angle=theta, origin=upper.pos)
    lower.rotate(axis=vec(aor[0],aor[1],aor[2]), angle=theta, origin=lower.pos)
    
    
    sleep(0.3)
    count+=1

