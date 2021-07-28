#!/usr/bin/env python
import math
import numpy as np
from floor import Floor   	    
from bike import Bike
from bike_gr_int import bk_gd_int
from model import force 



#bike1 = Bike() # Initiate Bike object
#bike1.gen_rand_bike() # Random parameters

#open("trajectory",'w')

#--------------------------------------------------------------
"""
 This is the fourth order Runge-Kutta method for solving the Second order equation of motion and
producing trajectory.
"""
def RuKu4(bike1,ground):
    tmax=20.0
    n=2000
    dt=tmax/float(n-1)
    pm = np.matrix([[0,0],[0,0],[0,0],[0,0]])
    vm = np.matrix([[0,0],[0,0],[0,0],[0,0]])
    k1 = np.matrix([[0,0],[0,0],[0,0],[0,0]]);l1 = np.matrix([[0,0],[0,0],[0,0],[0,0]])
    k2 = np.matrix([[0,0],[0,0],[0,0],[0,0]]);l2 = np.matrix([[0,0],[0,0],[0,0],[0,0]])
    k3 = np.matrix([[0,0],[0,0],[0,0],[0,0]]);l3 = np.matrix([[0,0],[0,0],[0,0],[0,0]])
    k4 = np.matrix([[0,0],[0,0],[0,0],[0,0]]);l4 = np.matrix([[0,0],[0,0],[0,0],[0,0]])
    traj=np.zeros([n,9])
    nrow=-1
                 #traj=np.array([np.zeros(9)])
    t=0.0
    move=1
    while (move>0):
        nrow=nrow+1
        #k1=acc(t,x)*dt------------------------------
        pm = bike1.bike_pos
        vm = bike1.bike_vel
    
        for i_el in range(4):
    	    assert( bike1.bike_pos[i_el,0] >0 )  
        force(bike1)
        for i_el in range(4):
            assert( bike1.bike_pos[i_el,0] >0 ) 
    
        bk_gd_int(bike1,ground)
        k1 = bike1.bike_acc*dt
        l1 = vm*dt
    
    
        #k2=acc(t+dt/2.0,x+k1/2.0,v+l1/2)*dt-----------------
        bike1.bike_pos = pm+k1/2.0
        bike1.bike_vel = vm+l1/2.0
    
        for i_el in range(4):
    	    assert( bike1.bike_pos[i_el,0] >0 ) 
        force(bike1)  
        for i_el in range(4):
            assert( bike1.bike_pos[i_el,0] >0 ) 
    
        bk_gd_int(bike1,ground)
    
        for i_el in range(4):
            assert( bike1.bike_pos[i_el,0] >0 ) 
    
        k2 = bike1.bike_acc*dt
    
        for i_el in range(4):
            assert( bike1.bike_pos[i_el,0] >0 ) 
    
        l2 = bike1.bike_vel*dt
    
        for i_el in range(4):
            assert( bike1.bike_pos[i_el,0] >0 ) 
    
           
        #k3=acc(t+dt/2.0,x+k2/2.0,v+l2/2)*dt-----------------
        bike1.bike_pos = pm+k2/2.0
    
        for i_el in range(4):
            assert( bike1.bike_pos[i_el,0] >0 ) 
    
        bike1.bike_vel = vm+l2/2.0
    
        for i_el in range(4):
    	    assert( bike1.bike_pos[i_el,0] >0 ) 
        force(bike1)
        for i_el in range(4):
            assert( bike1.bike_pos[i_el,0] >0 ) 
    
        bk_gd_int(bike1,ground)
    
        for i_el in range(4):
            assert( bike1.bike_pos[i_el,0] >0 ) 
    
        k3=bike1.bike_acc*dt
    
        for i_el in range(4):
            assert( bike1.bike_pos[i_el,0] >0 ) 
    
        l3=bike1.bike_vel*dt
        
        #k4=acc(t+dt,x+k3,v+l3)*dt--------------------------
        bike1.bike_pos = pm+k3
    
        for i_el in range(4):
            assert( bike1.bike_pos[i_el,0] >0 ) 
    
        bike1.bike_vel = vm+l3
    
        for i_el in range(4):
    	    assert( bike1.bike_pos[i_el,0] >0 ) 
        force(bike1)
        for i_el in range(4):
            assert( bike1.bike_pos[i_el,0] >0 ) 
        bk_gd_int(bike1,ground)
        k4 = bike1.bike_acc*dt
        l4 = bike1.bike_vel*dt
    
        #updating the velocities:
        #v=v+(k1 + 2*(k2 + k3) + k4)/6.0-----------------
        bike1.bike_vel = vm + (k1 + 2*(k2 + k3) + k4)/6.0
        
        #updating the positions:
        #x=x+v*dt---------------------------------------
        #x=x+(l1 + 2*(l2 + l3) + l4)/6.0-----------------
        #bike1.bike_pos = pm + bike1.bike_vel*dt
        bike1.bike_pos = pm + (l1 + 2*(l2 + l3) + l4)/6.0
        for i_el in range(4):
    	    assert( bike1.bike_pos[i_el,0] >0 ) 
        err = bk_gd_int(bike1,ground)
        t=t+dt
        	#traj=([traj,np.traj([t, bike1.bike_pos[0][0], bike1.bike_pos[0][1],  \
        	#                        bike1.bike_pos[1][0], bike1.bike_pos[1][1],  \
        	#                        bike1.bike_pos[2][0], bike1.bike_pos[2][1],  \
        	#                        bike1.bike_pos[3][0], bike1.bike_pos[3][1]])])
        traj[nrow][0]=t
        traj[nrow][1]=bike1.bike_pos[0][0]
        traj[nrow][2]=bike1.bike_pos[0][1]
        traj[nrow][3]=bike1.bike_pos[1][0]
        traj[nrow][4]=bike1.bike_pos[1][1]
        traj[nrow][5]=bike1.bike_pos[2][0]
        traj[nrow][6]=bike1.bike_pos[2][1]
        traj[nrow][7]=bike1.bike_pos[3][0]
        traj[nrow][8]=bike1.bike_pos[3][1]
        #print "{0:2e} {1:3e} {2:4e} {3:5e} {4:6e} {5:7e} {6:8e} {7:9e} {8:10e}".format(traj[nrow][0],traj[nrow][1],traj[nrow][2],traj[nrow][3] \
        #                              ,traj[nrow][4],traj[nrow][5],traj[nrow][6],traj[nrow][7],traj[nrow][8])   
        if err==1:
            move = 0
        else:
            if t>tmax:
                move = 0
            else:
                 move = 1
        ##if t>tmax:
        ##    break
    bike1.traj = traj
    return






##################################################
def Euler(bike1,ground):
    if hasattr(bike1,'traj'):
        return
    tmax=20.0
    n=2500
    dt=tmax/float(n-1)
    traj=np.zeros([n,9])
    nrow=-1
    t=0.0
    move=1
    while (move>0): 
        if any([bike1.bike_pos[i_el,0] < 0 for i_el in range(4)]):
            err = 1 # Stop moving if x<0 for any coordinate
        
        #for i_el in range(4):
        #    assert( bike1.bike_pos[i_el,0] >0 )  
        
        force(bike1)
        
        #for i_el in range(4):
        #    assert( bike1.bike_pos[i_el,0] >0 )  
        
        err = bk_gd_int(bike1,ground)
        if (err == 1):
            move = 0 # Stop moving if head hits ground
        
        #for i_el in range(4):
        #    assert( bike1.bike_pos[i_el,0] >0 )  
        
        bike1.bike_vel[:,:] += bike1.bike_acc[:,:] * dt
        
        #for i_el in range(4):
        #    assert( bike1.bike_pos[i_el,0] >0 )  
        
        bike1.bike_pos[:,:] += bike1.bike_vel[:,:] * dt + .5* bike1.bike_acc[:,:] * dt**2
        if any([bike1.bike_pos[i_el,0] < 0 for i_el in range(4)]):
            err = 1 # Stop moving if x<0 for any coordinate
        nrow=nrow+1
        
        t=t+dt
        	#traj=([traj,np.traj([t, bike1.bike_pos[0][0], bike1.bike_pos[0][1],  \
        	#                        bike1.bike_pos[1][0], bike1.bike_pos[1][1],  \
        	#                        bike1.bike_pos[2][0], bike1.bike_pos[2][1],  \
        	#                        bike1.bike_pos[3][0], bike1.bike_pos[3][1]])])
        traj[nrow][0]=t
        traj[nrow][1]=bike1.bike_pos[0][0]
        traj[nrow][2]=bike1.bike_pos[0][1]
        traj[nrow][3]=bike1.bike_pos[1][0]
        traj[nrow][4]=bike1.bike_pos[1][1]
        traj[nrow][5]=bike1.bike_pos[2][0]
        traj[nrow][6]=bike1.bike_pos[2][1]
        traj[nrow][7]=bike1.bike_pos[3][0]
        traj[nrow][8]=bike1.bike_pos[3][1]
        # print "{0:2e} {1:3e} {2:4e} {3:5e} {4:6e} {5:7e} {6:8e} {7:9e} {8:10e}".format(traj[nrow][0],traj[nrow][1],traj[nrow][2],traj[nrow][3] \
        #   ,traj[nrow][4],traj[nrow][5],traj[nrow][6],traj[nrow][7],traj[nrow][8])   
        if err==1:
            move = 0
        else:
            if t>tmax:
                move = 0
            else:
                 move = 1
        ##if t>tmax:
        ##    break
    bike1.traj = traj # Set trajectory as a property of the bike
    return

