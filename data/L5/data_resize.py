import numpy as np
import sys

def main(resizeFactor=0.5):
    print(resizeFactor)
    bigTraj = np.load("traj.npy")
    smallTraj = bigTraj[::int(1/resizeFactor),:]
    np.save("smallTraj.npy",smallTraj)

if __name__ == "__main__":
    
    main(float(sys.argv[1:][0]))
