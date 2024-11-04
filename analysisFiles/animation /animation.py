from vpython import *
from time import *
import numpy as np 

from brownian_ot.brownian_ot import analysis


c2 = canvas(width=2000, height=900,background=color.white)


scale = 1
traj1= analysis.expand_trajectory(np.load(r"C:\Users\mohod\Development\ot_sim\data\L1\data\LCP_0.02_5714025.npy"))*scale
traj2= analysis.expand_trajectory(np.load(r"C:\Users\mohod\Development\ot_sim\data\L1\data\LCP_0.03_5714025.npy"))*scale
traj3= analysis.expand_trajectory(np.load(r"C:\Users\mohod\Development\ot_sim\data\L1\data\LCP_0.04_5714025.npy"))*scale

axis_len = 10

scene.background_color = (0.8, 0.8, 0.8)

x = arrow(pos=vector(0,0,0),axis=vector(axis_len,0,0),shaftwidth=0.1, color=color.red)
y = arrow(pos=vector(0,0,0),axis=vector(0,axis_len,0),shaftwidth=0.1, color=color.blue)
z = arrow(pos=vector(0,0,0),axis=vector(0,0,axis_len),shaftwidth=0.1, color=color.green)

mySphere1 = sphere(color = color.red, pos=vector(0,0,0), radius=0.4,make_trail=True,retain=30)
mySphere2 = sphere(color = color.blue, pos=vector(0,0,0), radius=0.4,make_trail=True,retain=30)
mySphere3 = sphere(color = color.green, pos=vector(0,0,0), radius=0.4,make_trail=True,retain=30)


count =0

# while True:
#     mySphere.pos = vector(2*np.sin(count),0,2*np.cos(count))
#     sleep(0.01)

c2.camera.pos = vector(5,5,5)
# c2.camera.rotate = rotate()
while (count < len(traj1[:,0])):
    mySphere1.pos = vector(traj1[count,0] *1e7,traj1[count,1]*1e7,traj1[count,2]*1e7)
    mySphere2.pos = vector(traj2[count,0] *1e7,traj2[count,1]*1e7,traj2[count,2]*1e7)
    mySphere3.pos = vector(traj3[count,0] *1e7,traj3[count,1]*1e7,traj3[count,2]*1e7)

    sleep(0.001)
    count+=1