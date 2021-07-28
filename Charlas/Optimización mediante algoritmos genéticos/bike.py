import numpy as np
from copy import deepcopy

class Bike(object):
    """
    Bike has the properties of all its components: Wheels, Masses, positions, vel, Rad, k_spring
    bike.bike_mass np array from 0 to 3, index is for object  
    bike.bike_rad  np array from 0 to 3, index is for object
    bike.bike_pos np array with 2 indices, first index is object, second index is direction
    bike.bike_vel np array with 2 indices, first index is object, second index is direction
    bike.bike_acc np array with 2 indices, first index is object, second index is direction
    bike.bike_l0 is a np matrix indices are for objects (wheel or mass)
    bike.k_sp spring constant
    NEW : Bike now has a matrix for positions, velocities and acceleration and l0
          For masses and radius there are arrays.
    IMPORTANT : FOLLOW THE INDEX CONVENTION.    0 is mass1
						1 is mass2
						2 is wheel1
						3 is wheel2
    """

    def __init__(self, **kwargs):
        # Define Cinematic magnitudes
        self.bike_vel = np.array([np.zeros(2) for _ in range(4)])
        self.bike_acc = np.array([np.zeros(2) for _ in range(4)])

        # Define mass and wheel densities
        w_den = 0.5
        m_den = 1.0    		
        self.dens = [w_den]*2+[m_den]*2
        
        if kwargs:
            args = [kwargs[arg] for arg in ['pos','mass','k_sp']]
            self._gen_sp_bike(*args)
        else:
            self._gen_rand_bike()	

    def _set_springs_l0(self):
        #Set spring's natural length from the initial positions
        l0_mm = np.linalg.norm(self.init_pos[0]-self.init_pos[1])
        l0_ww = np.linalg.norm(self.init_pos[2]-self.init_pos[3])
        l0_w1m1 = np.linalg.norm(self.init_pos[2]-self.init_pos[0])
        l0_w1m2 = np.linalg.norm(self.init_pos[2]-self.init_pos[1])
        l0_w2m1 = np.linalg.norm(self.init_pos[3]-self.init_pos[0])
        l0_w2m2 = np.linalg.norm(self.init_pos[3]-self.init_pos[1])
        
        self.bike_l0 = np.matrix([ 
            [0., l0_mm, l0_w1m1,     l0_w2m1], 
            [l0_mm, 0., l0_w1m2,     l0_w2m2], 
            [l0_w1m1,   l0_w1m2, 0., l0_ww], 
            [l0_w2m1,   l0_w2m2,     l0_ww, 0.] ])
        
    def _gen_rand_bike(self):
        #This method should generate a random bike
        box_size = 10. 
        y_skin = 5.
        x_skin = 5.
        mass_handicap = 0.1
        sprng_hdcp = 250. #ORI 50.
        mass_mag = 5.
        sprng_mag = 50.
        
        self.bike_pos = np.array([
            np.array(
                [x_skin + box_size*np.random.random(),
                y_skin + box_size*np.random.random()]
                ) for _ in range(4)])

        #SAVE INITIAL POSITIONS
        self.init_pos = deepcopy(self.bike_pos)
        
        self.bike_mass = np.array([mass_handicap + mass_mag*np.random.random() for _ in range(4)])
        
        rads = [np.sqrt(m/(np.pi*rho)) for m, rho in zip(self.bike_mass,self.dens)]
        self.bike_rad = np.array(rads)
        
        #Set spring constant and l0
        self.k_sp = sprng_hdcp + sprng_mag * np.random.random()        
        self._set_springs_l0()

    def _gen_sp_bike(self,new_bike_pos,new_bike_mass,new_k_sp):
        #This method should generate a specific bike, given by the genetic algorithm 
        self.bike_vel = np.array([np.zeros(2),np.zeros(2),np.zeros(2),np.zeros(2)])
        self.bike_acc = np.array([np.zeros(2),np.zeros(2),np.zeros(2),np.zeros(2)])
        new_bike_pos.clip(2,15)
        self.bike_pos = new_bike_pos
         
        self.init_pos = deepcopy(self.bike_pos)
        	
        self.bike_mass = new_bike_mass
        
        # Set all radius in one matrix
        rads = [np.sqrt(m/(np.pi*rho)) for m, rho in zip(self.bike_mass,self.dens)]
        self.bike_rad = np.array(rads)

        # Set spings constant and l0
        self.k_sp = new_k_sp     	
        self._set_springs_l0() 
