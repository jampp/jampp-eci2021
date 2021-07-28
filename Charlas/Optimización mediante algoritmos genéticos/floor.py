import numpy as np

#Floor Class
class Floor(object):
    """
    Defines the ground from a random walk
    """

    def __init__(self):
        self.path_length = 400 # Total ground length
        self.path_detail = 5.0 #delta X between ground points
        self.flat_grd = 15.0 #distance of the initial flat part of the ground, so bikes can land
        self.rugosity = 5. #Works with 0.5 
        self.path_dim = int(self.path_length/self.path_detail) #Number of points in the ground array
        self.coor = np.zeros((self.path_dim,2)) #Initiate ground array with zeros
        self.slopes = np.zeros((self.path_dim,1))
        self.nor_ver = np.zeros((self.path_dim,2)) 
        self.par_ver = np.zeros((self.path_dim,2))
        self._gen_coor()
        self._gen_versors()

    def _gen_coor(self): #This generates the coordinates of the ground
        #Flat part of the ground, wher bikes will land
        for j in range(int(self.flat_grd/self.path_detail)):
            self.coor[j,1] = 0. #Y coordinate of ground
            self.coor[j,0] = j * self.path_detail #X coordinate of ground

        #Rrandom part of the ground
        for j in range(int(self.flat_grd/self.path_detail),self.path_dim):
            self.coor[j,1] = self.coor[j-1,1] + self.rugosity * ( np.random.random() - .5 ) #Y coordinate of ground
            self.coor[j,0] = j*self.path_detail #X coordinate of ground


    def _gen_versors(self): #This generates the local system of coordinates in the ground
        #First calculate the slopes for all thge segments
        for j in range(self.path_dim - 1):
            self.slopes[j] = (self.coor[j+1,1] - self.coor[j,1]) / (self.coor[j+1,0] - self.coor[j,0])
            self.par_ver[j,0] = 1. #X coordinate of the parallel versor 
            self.par_ver[j,1] = self.slopes[j] #Y ccoordinate of the parallel versor
            inv_norm = 1 / np.sqrt( self.par_ver[j,0]**2 + self.par_ver[j,1]**2) #Normalization factor
            self.par_ver[j,0] = self.par_ver[j,0] * inv_norm #Normalize parallel versor
            self.par_ver[j,1] = self.par_ver[j,1] * inv_norm #Normalize parallel versor
       	    
            #Now Define normal versor in each seagment of the floor
            self.nor_ver[j,1] = 1.0 #X coordinate of the parallel versor 
            self.nor_ver[j,0] = - self.slopes[j] #Y ccoordinate of the parallel versor
            inv_norm = 1 / np.sqrt( self.nor_ver[j,0]**2 + self.nor_ver[j,1]**2) #Normalization factor
            self.nor_ver[j,0] = self.nor_ver[j,0] * inv_norm #Normalize parallel versor
            self.nor_ver[j,1] = self.nor_ver[j,1] * inv_norm #Normalize parallel versor




