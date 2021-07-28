import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
import matplotlib.animation as animation

from floor import *
from bike import *

class Render(object):
    """Class for visualization"""
    def __init__(self, ground, bike, ibike):
        self.ground = ground 
        self.bike = bike
        self.ibike = ibike
        self.scale = 5.0
        self.rotation = 30.0  #rotation angle of wheel's spokes 
	
        #draw canvas, set defaults, output text
        self.fig = plt.figure()
        self.fig.suptitle(' Evolutionary Algorithm', fontsize = 14) #, fontweight = 'bold')
        self.ax = self.fig.add_subplot(111, aspect = 'equal', autoscale_on = False, xlim = (0.0, 100.0), ylim = (-30.0, 70.0))
        self.ax.set_title('The Genetic Bike')
        #self.ax.add_patch(patches.Rectangle((60.0, 45.0), 38, 23, fill = False, linewidth = 1.0))
        #self.ax.text(61.0, 65.0, 'Fitness value', fontsize = 11) 
        #self.ax.text(38.0, -27.0, 'best distance:', fontsize = 11)
        #self.ax.text(10.0, 65.0, '-th generation', fontsize = 14)
        img = mpimg.imread('image.jpeg')
        xmin, xmax = self.ax.get_xlim()
        ymin, ymax = self.ax.get_ylim()
        imgplot = plt.imshow(img, extent = [xmin, xmax, ymin, ymax], aspect = 'auto', alpha = 0.6)
        self.ax.grid()

        #create ground level trajectory
        self.x_line = np.zeros((self.ground.path_dim, 1))
        self.y_line = np.zeros((self.ground.path_dim, 1))    
        xy = self.ground.coor   
        for i in range(0, self.ground.path_dim): 
            self.x_line[i] = xy[i, 0] * self.scale
            self.y_line[i] = xy[i, 1] * self.scale       
        self.line = self.ax.plot([0.0], [0.0], lw = 2.0, color = 'black', alpha = 0.5)[0] 
           
        #create circles for masses ORIGINAL 1.8, touched by Kevin 
        xy_out = -10.0
        scl = self.scale
        self.cir_mass1 = self.ax.plot(xy_out, xy_out, 'ro', ms = 6.0 * self.bike.bike_rad[0] * scl, mew = 1.0, alpha = 0.4)[0]
        self.cir_mass2 = self.ax.plot(xy_out, xy_out, 'ro', ms = 6.0 * self.bike.bike_rad[1] * scl, mew = 1.0, alpha = 0.4)[0] 
        #create wheels    
        self.cir_wheel1 = self.ax.plot(xy_out, xy_out, 'bo', ms = 5.65 * self.bike.bike_rad[2] * scl, mew = 3.0, alpha = 0.4)[0]
        self.cir_wheel2 = self.ax.plot(xy_out, xy_out, 'bo', ms = 5.65 * self.bike.bike_rad[3] * scl, mew = 3.0, alpha = 0.4)[0] 
                                                                                        
        #create springs between masses (mN) and wheels (wN)
        self.line_m1w1 = self.ax.plot(0.0, 0.0, lw = 1.0, color = 'black', alpha = 0.7)[0]
        self.line_m1w2 = self.ax.plot(0.0, 0.0, lw = 1.0, color = 'black', alpha = 0.7)[0]
        self.line_m2w1 = self.ax.plot(0.0, 0.0, lw = 1.0, color = 'black', alpha = 0.7)[0]
        self.line_m2w2 = self.ax.plot(0.0, 0.0, lw = 1.0, color = 'black', alpha = 0.7)[0]
        self.line_m1m2 = self.ax.plot(0.0, 0.0, lw = 1.0, color = 'black', alpha = 0.7)[0]
        self.line_w1w2 = self.ax.plot(0.0, 0.0, lw = 1.0, color = 'black', alpha = 0.7)[0]

        #create spokes of wheels
        self.line_spoke1 = self.ax.plot(0.0, 0.0, lw = 1.0, color = 'black', alpha = 0.5)[0]
        self.line_spoke2 = self.ax.plot(0.0, 0.0, lw = 1.0, color = 'black', alpha = 0.5)[0]

        #bike motion data [t, [x, y]]
        self.time = []
        self.x_mass1, self.y_mass1 = [], []
        self.y_mass2, self.x_mass2 = [], []
        self.x_wheel1, self.y_wheel1 = [], []
        self.x_wheel2, self.y_wheel2 = [], []
 
        nrow, ncol = bike.traj.shape
        self.nframes = nrow  #number of frames for moving 1 bike         
        for i in range(0, self.nframes):
            self.time = np.append(self.time, i)
            self.x_mass1 = np.append(self.x_mass1, bike.traj[i, 1] * scl) 
            self.y_mass1 = np.append(self.y_mass1, bike.traj[i, 2] * scl)
            self.x_mass2 = np.append(self.x_mass2, bike.traj[i, 3] * scl) 
            self.y_mass2 = np.append(self.y_mass2, bike.traj[i, 4] * scl) 
            self.x_wheel1 = np.append(self.x_wheel1, bike.traj[i, 5] * scl) 
            self.y_wheel1 = np.append(self.y_wheel1, bike.traj[i, 6] * scl) 
            self.x_wheel2 = np.append(self.x_wheel2, bike.traj[i, 7] * scl) 
            self.y_wheel2 = np.append(self.y_wheel2, bike.traj[i, 8] * scl)   

        #create text objects
        self.time_text = self.ax.text(2.5, -20.0, '', fontsize = 13) 
        self.dist_text = self.ax.text(2.5, -27.0, '', fontsize = 13) 
        self.bike_text = self.ax.text(75.0, -27.0, '', fontsize = 13)

    def init_line(self):
        """Initialize animation"""
        #ground
        self.line.set_data([], [])
        
        #text
        self.time_text.set_text('')
        self.dist_text.set_text('')

        return self.line, self.line_m1w1, self.line_m1w2, self.line_m2w1, self.line_m2w2, self.line_m1m2, self.line_w1w2, self.line_spoke1, self.line_spoke2, self.cir_mass1, self.cir_mass2, self.cir_wheel1, self.cir_wheel2, self.time_text, self.dist_text, self.bike_text,


    def animate(self, itime):  #itime = frame number
        """Perform animation step"""
        
        #scaling canvas  
        xmin, xmax = self.ax.get_xlim()
        if self.x_wheel1[itime] > self.x_wheel2[itime]: x_wheel_max = self.x_wheel1[itime]
        else: x_wheel_max = self.x_wheel2[itime]
        
        if x_wheel_max > (xmax - 10.0): 
            self.ax.set_xlim((30.0 + xmin), (30.0 + xmax))
            xmin, xmax = self.ax.get_xlim()
            self.time_text.set_position((2.5 + xmin, -20.0)) 
            self.dist_text.set_position((2.5 + xmin, -27.0))  
            self.bike_text.set_position((75.0 + xmin, -27.0))
            self.ax.figure.canvas.draw()
 
        
        ymin, ymax = self.ax.get_ylim()
        y_wheel_min,y_wheel_max = sorted([self.y_wheel1[itime],self.y_wheel2[itime]])

        if y_wheel_min < ymin+10: 
            self.ax.set_ylim((-30.0 + ymin), (-30 + ymax))
            ymin, ymax = self.ax.get_ylim()
            self.ax.figure.canvas.draw()
        elif y_wheel_max > ymax-10: 
            self.ax.set_ylim((+30.0 + ymin), (+30 + ymax))
            ymin, ymax = self.ax.get_ylim()
            self.ax.figure.canvas.draw()

        #ground update
        self.line.set_data(self.x_line, self.y_line)
        
        #bike: wheels update
        self.cir_mass1.set_data(self.x_mass1[itime], self.y_mass1[itime]) 
        self.cir_mass2.set_data(self.x_mass2[itime], self.y_mass2[itime]) 
        self.cir_wheel1.set_data(self.x_wheel1[itime], self.y_wheel1[itime]) 
        self.cir_wheel2.set_data(self.x_wheel2[itime], self.y_wheel2[itime]) 

        #bike: springs update 
        x_m1w1, y_m1w1 = [self.x_mass1[itime], self.x_wheel1[itime]], [self.y_mass1[itime], self.y_wheel1[itime]]
        x_m1w2, y_m1w2 = [self.x_mass1[itime], self.x_wheel2[itime]], [self.y_mass1[itime], self.y_wheel2[itime]]
        x_m2w1, y_m2w1 = [self.x_mass2[itime], self.x_wheel1[itime]], [self.y_mass2[itime], self.y_wheel1[itime]]
        x_m2w2, y_m2w2 = [self.x_mass2[itime], self.x_wheel2[itime]], [self.y_mass2[itime], self.y_wheel2[itime]]
        x_m1m2, y_m1m2 = [self.x_mass1[itime], self.x_mass2[itime]], [self.y_mass1[itime], self.y_mass2[itime]]
        x_w1w2, y_w1w2 = [self.x_wheel1[itime], self.x_wheel2[itime]], [self.y_wheel1[itime], self.y_wheel2[itime]]

        self.line_m1w1.set_data(x_m1w1, y_m1w1)
        self.line_m1w2.set_data(x_m1w2, y_m1w2)
        self.line_m2w1.set_data(x_m2w1, y_m2w1)
        self.line_m2w2.set_data(x_m2w2, y_m2w2)
        self.line_m1m2.set_data(x_m1m2, y_m1m2)
        self.line_w1w2.set_data(x_w1w2, y_w1w2)

        #bike: spokes update
        cpi = np.pi / 180.0
        rot =  self.x_wheel1[itime] * self.rotation - float(int(self.x_wheel1[itime] * self.rotation / 360) * 360) 
        x_spoke1, y_spoke1 = [self.x_wheel1[itime] - self.bike.bike_rad[2] * np.sin(rot * cpi), self.x_wheel1[itime] + self.bike.bike_rad[2] * np.sin(rot * cpi)], [self.y_wheel1[itime] - self.bike.bike_rad[2] * np.cos(rot * cpi), self.y_wheel1[itime] + self.bike.bike_rad[2] * np.cos(rot * cpi)] 
        rot =  self.x_wheel2[itime] * self.rotation - float(int(self.x_wheel2[itime] * self.rotation / 360) * 360) 
        x_spoke2, y_spoke2 = [self.x_wheel2[itime] - self.bike.bike_rad[3] * np.sin(rot * cpi), self.x_wheel2[itime] + self.bike.bike_rad[3] * np.sin(rot * cpi)], [self.y_wheel2[itime] - self.bike.bike_rad[3] * np.cos(rot * cpi), self.y_wheel2[itime] + self.bike.bike_rad[3] * np.cos(rot * cpi)] 

        self.line_spoke1.set_data(x_spoke1, y_spoke1)
        self.line_spoke2.set_data(x_spoke2, y_spoke2)  

        #text update
        self.time_text.set_text('time = %.1f ms' % float(itime))
        self.dist_text.set_text('distance: %.1f m' % max(self.x_wheel1[itime], self.x_wheel2[itime]))
        self.bike_text.set_text('bike tried: %3i' % self.ibike)

        return self.line, self.line_m1w1, self.line_m1w2, self.line_m2w1, self.line_m2w2, self.line_m1m2, self.line_w1w2, self.line_spoke1, self.line_spoke2, self.cir_mass1, self.cir_mass2, self.cir_wheel1, self.cir_wheel2, self.time_text, self.dist_text, self.bike_text,
 

#sif __name__=='__main__':
  
    #ground = Floor()                          
    #plt.ion()
    #for ibike in range(1,2):
        #bike = Bike()                                                                                      
        #render = Render(ground, bike, ibike)     
        #ani = animation.FuncAnimation(render.fig, render.animate, init_func = render.init_line, frames = render.nframes, interval = 50.0, repeat = False, blit = True) 
        #ani.save('2osc.mp4', writer="ffmpeg")
        #plt.show()
    #ani.save('project_group3.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
    #FFwriter = animation.FFMpegWriter()
    #ani.save('project_group3.mpeg', writer = FFwriter, fps = 30, extra_args=['-vcodec', 'libx264'])




