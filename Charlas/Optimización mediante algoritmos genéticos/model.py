import numpy as np
from numpy import linalg as LA

Gravity_Const=5.0
def force(bike):
    """
    This Routine calculates the force of the internal springs of the bike, gravity and, friction
    """
    gamma = 1. # Set Discipative force constant
    
    bike.bike_acc[:,:] = 0	#Set forces to 0
    for i in range(4): # Loop bikes
        bike.bike_acc[i,1] += -Gravity_Const
        bike.bike_acc[i,:] += -gamma * bike.bike_vel[i,:] / bike.bike_mass[i]
        for j in range(i+1,4): # Loop neighbogrs
            f_spr =  bike.k_sp*(LA.norm(bike.bike_pos[j]-bike.bike_pos[i])-bike.bike_l0[i,j])*(bike.bike_pos[j,:]-bike.bike_pos[i,:])/(LA.norm(bike.bike_pos[i]-bike.bike_pos[j]))
            bike.bike_acc[i,:] += f_spr / bike.bike_mass[i]
            bike.bike_acc[j,:] += -f_spr / bike.bike_mass[j]

	       
