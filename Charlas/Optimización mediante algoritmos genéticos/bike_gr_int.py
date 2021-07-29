import numpy as np
from floor import Floor
from bike  import Bike


d_prox = 0.1 # Defines the distance at which the torque is ON
f_torq = 10.0 # Defines the force to be aplied to the wheel if its proximate to the ground
damp = 0.1  # Defines how much energy will be conserved in the collison ground-wheel: 
		 #0 is total loss of energy, 1 is conservation of energy 
		#MUST BE BETWEEN 0 and 1 ( do you even physics?! )

def dist_point_line(nx,ny,px,py,xg,yg,xw,yw):
    """ 
    This function calculates the minimum distance between a line and a point
    nx,ny are the unit vectors normal to the surface
    px,py are the unit vectors parallel to the surface
    xg,yg 1 coordinate of the line
    xw,yw coordinate of the point   	
    """    
    det = ny * px - nx * py
    dist = py * (xg - xw) + px * (yw - yg)
    dist =  dist / det # min distance between point and line
    x_int = -dist * nx + xw # nearest point in the line to the point x_coor
    y_int = -dist * ny + yw # nearest point in the line to the point y_coor
    return [abs( dist ), x_int, y_int]


 
def bk_gd_int(bike,ground):
    fl_coor = ground.coor
    par_ver = ground.par_ver #par_ver has all the parallel versos of the segments
    nor_ver = ground.nor_ver #par_ver has all the parallel versos of the segments
    path_detail = ground.path_detail
    assert( path_detail > 0. )    
    for elmt in range(4): #Inspect element number (0:mass1, 1:mass2, 2:wheel1, 3:wheel2)
        vel_tmp = bike.bike_vel[elmt,:]
        rad = bike.bike_rad[elmt] # Get bike's element radius
        #        print rad
        
        assert( rad > 0. )
        xw = bike.bike_pos[elmt,0] #Get wheel's position
        assert( xw >= 0. )
        
        yw = bike.bike_pos[elmt,1]
        #        print rad,xw
        # Set the possilbe interaction range
        x_max = xw + rad
        x_min = xw - rad    
        assert( x_max >= 0 )
        assert( x_min >= 0 )

        if x_max >= ground.path_length: # Arrived to finish line
            bike.path_completed = True
            return 1 #End solving algorithm run, return 1
        
        # Select the possible interacting segments
        i_min = int( x_min / float(path_detail))    
        i_max = int( x_max / float(path_detail))   
        
        assert( i_min >= 0 )
        assert( i_max >= 0 )
        
        
        #        print 'element', elmt 
        #        print 'wheel min ',x_min, 'wheel max ', x_max
        #        print 'segment min ',fl_coor[i_min,0], 'segment max ', fl_coor[i_max+1,0]
        #        print 'i_min ',i_min, ' i_max = ', i_max
        
        
        #For those segments, calculate minimal distance
        for i in range(i_min,i_max+1):
            # print i #FOR DEBUGGING PURP
            nx = nor_ver[i,0]
            ny = nor_ver[i,1]
            px = par_ver[i,0]
            py = par_ver[i,1]
            xg = fl_coor[i,0]
            yg = fl_coor[i,1]
            
            #calculate minimal distance between line and point 
            [dist, x_int, y_int ] = dist_point_line(nx,ny,px,py,xg,yg,xw,yw)
            
            # Is the minimum contained in the segment? Let's find out:
            if x_int > fl_coor[i,0] and x_int < fl_coor[i+1,0]:
                #minimum distance contained in this segment
                # print 'minimum distance in segment',fl_coor[i,0],fl_coor[i+1,0]
                pass #Do nothing to the distance   
            elif x_int < fl_coor[i,0]:
                # Minimum distance at left edge
                # print 'Evaluate left Edge in segment ',fl_coor[i,0],fl_coor[i+1,0]
                dist_edge = np.sqrt( ( xw - fl_coor[i,0] )**2 +( yw - fl_coor[i,1] )**2 )
                x_int = fl_coor[i,0]
                y_int = fl_coor[i,1]
                nx = (xw - fl_coor[i,0]) / dist_edge
                ny = (yw - fl_coor[i,1]) / dist_edge
                px = ny #Set new versor for the edges. Not ideal choise, see if it works
                py = -nx # OTHER idea would be to make an average of segments
                dist = dist_edge
            # print 'edge distance = ', dist_edge 
            elif x_int > fl_coor[i+1,0] if i+1<ground.path_dim else ground.path_length:
                continue # edge already taken into account in previous elif
            #    # Minimum distance at right edge of the segment
            #    # print 'Evaluate right Edge in segment ',fl_coor[i,0],fl_coor[i+1,0]
            #    dist_edge = np.sqrt( ( xw - fl_coor[i+1,0] )**2 +( yw - fl_coor[i+1,1] )**2 ) 
            #    x_int = fl_coor[i+1,0]
            #    y_int = fl_coor[i+1,1]
            #    px = 1.    #Set new versor for the edges. Not ideal choise, see if it works
            #    py = 0.    # OTHER idea would be to make an average of segments
            #    nx = 0.
            #    ny = 1.  
            # print 'edge distance = ', dist_edge
            
            dist = dist - rad #clalculates distance between contour of object and fround	
            
            # UNCOMMENT THESE 2 LINES TO make masses act as masses 
            if (dist<0) and (elmt < 2): #Object touching the ground and object is a mass
                return 1 #End solving algorithm run, return 1
            
            if (dist<d_prox) and (elmt==3): #Object is proximate to ground and okbject is a wheel 
                bike.bike_acc[elmt,:] += f_torq * np.array([px,py])
            
            #Uncomment final part to make masses behave as masses
            if (dist<0) and (elmt > 1): #Object touching the ground and object is a wheel
                #Change normal direction of velocity
                norm_vel = sum( vel_tmp * np.array([nx,ny] )) # dot product
                par_vel = sum( vel_tmp * np.array([px,py] ))  #dot product
                vel_tmp = par_vel * np.array([px,py]) - damp* abs(norm_vel) * np.array([nx,ny])                #damp is to take energy away in a collison
                bike.bike_vel[elmt,:] = vel_tmp # Give it to bike
                # Move wheel out of ground  
                bike.bike_pos[elmt,:] += np.array([nx,ny]) * (-dist)
                 
        
    



