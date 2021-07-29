import numpy as np

def score(bike):
    #Give the object bike a score bike.score, analizing bike.traj
    puntaje = np.zeros(4)
    for i in range(4):
        puntaje[i] = np.amax(bike.traj[:,2*i+1], axis=0) # Get maximum  x coordinate of each wheel/head 
    puntaje_f = np.amax(puntaje, axis=0)
    bike.score = puntaje_f #Set bike score

