######################################################
# Copyright (c) 2021 Maker Portal LLC
# Author: Joshua Hrisko
######################################################
#
# This code (1) reads the csv accelerometer data and 
# integrates it twice to get arrays for velocity and 
# displacement. (2) Creates three image files (one for
# each axis x,y,z) that graphs the acceleration, 
# velocity, and displacement on seperate plots. In these
# plots, calibrated data is NOT compared with uncalibrated
# data. In the forward axis graph, theoretical values are
# plotted against experimental values. 
#
######################################################
#
# wait 5-sec for IMU to connect
import time,sys
sys.path.append('../')
t0 = time.time()
start_bool = False # if IMU start fails - stop calibration
while time.time()-t0<5:
    try: 
        from mpu9250_i2c import *
        start_bool = True
        break
    except:
        continue
import numpy as np
import csv,datetime
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import cumtrapz, trapz
from scipy import signal
import math
from track_theory import track_theory

time.sleep(2) # wait for MPU to load and settle
accel_labels = ['a_x','a_y','a_z']

def imu_integrator(time_array, cal_z_accel):

    ###################################
    # Integrate Data Twice 
    ###################################
    
    cal_z_velocity = np.append(0.0, cumtrapz(cal_z_accel,x=time_array))
    
    #plot_velocity(time_array, [uncal_x_velocity, uncal_y_velocity, uncal_z_velocity], [cal_x_velocity, cal_y_velocity, cal_z_velocity])

    cal_z_displacement = np.append(0.0, cumtrapz(cal_z_velocity, x=time_array))

    return cal_z_velocity, cal_z_displacement


def plot_total(time_array, cal_accel, cal_vel, cal_dis, TITLE, FILENAME, c):
    ###################################
    # Plot 
    ###################################

    # get theoretical forward axes values
    time_theory, accel_theory, vel_theory, dis_theory = track_theory(len(time_array))

    plt.style.use('ggplot')
    fig,axs = plt.subplots(3,1,figsize=(12,9))
    axs[0].plot(time_array, cal_accel, color = c, label="Experimental")
    #axs[0].plot(time_theory, accel_theory, color = 'k', label="Theoretical")
    axs[1].plot(time_array, cal_vel, color = c, label="Experimental")
    #axs[1].plot(time_theory, vel_theory, color = 'k', label="Theoretical")
    axs[2].plot(time_array, cal_dis, color = c, label="Experimental")
    #axs[2].plot(time_theory, dis_theory, color = 'k', label="Theoretical")
    axs[0].legend(fontsize=14, loc='lower right');axs[1].legend(fontsize=14, loc='lower right');axs[2].legend(fontsize=14, loc='lower right')
    axs[0].set_ylabel('Acceleration [m/s/s]',fontsize=18)
    axs[1].set_ylabel('Velocity [m/s]',fontsize=18)
    axs[2].set_ylabel('Displacement [m]',fontsize=18)
    axs[2].set_xlabel('Time (seconds)',fontsize=18)
    #axs[0].set_ylim([-2,2]);axs[1].set_ylim([-2,2])
    axs[0].set_title(TITLE,fontsize=18)
    fig.savefig(FILENAME,dpi=300,
                bbox_inches='tight',facecolor='#FCFCFC')
    fig.show()

    return

if __name__ == '__main__':
    
    mpu_labels = ['a_x','a_y','a_z'] # gyro labels for plots 

    ###################################
    # Read data from .csv file 
    ###################################

    CSVData = open("Aluminum_Track_Trials/Track_Bounce_Trials/bounce_1.csv")
    csv_data = np.loadtxt(CSVData, skiprows = 1, delimiter=",", dtype=float)

    time_array = csv_data[:, 0]
    cal_x_accel = csv_data[:, 4]
    cal_y_accel = csv_data[:, 5]
    cal_z_accel = csv_data[:, 6]

    ###################################
    # Graph .csv data to double check 
    ###################################

    #plot_csv(time_array, uncal_accel_array, cal_accel_array)
    #exit()

    ###################################
    # Convert g to m/s/s
    ###################################
    cal_x_accel *= 9.80665   # converts to m/s/s
    cal_y_accel *= 9.80665   # converts to m/s/s
    cal_z_accel *= 9.80665   # converts to m/s/s

    # Remove gravity component
    #cal_x_accel += (9.80665 * math.cos(math.radians(1)))   # remove perpendicular gravity component due to 1 degree incline
    # DON'T remove gravity component from the axis parallel to the track because it is unopposed when in motion. 
    
    ###################################
    # integration over time
    ###################################
    cal_x_vel, cal_x_dis = imu_integrator(time_array, cal_x_accel)
    cal_y_vel, cal_y_dis = imu_integrator(time_array, cal_y_accel)
    cal_z_vel, cal_z_dis = imu_integrator(time_array, cal_z_accel)

    #plot_total(time_array, cal_x_accel, cal_x_vel, cal_x_dis, 'X Forward Trial 3: X Axis', 'x_track_3_x.png', c='r')
    #plot_total(time_array, cal_y_accel, cal_y_vel, cal_y_dis, 'Y Forward Trial 3: Y Axis', 'y_track_3_y.png', c='b')
    plot_total(time_array, cal_z_accel, cal_z_vel, cal_z_dis, 'Bounce Z Forward Trial 1: Z Axis', 'bounce_1_z.png', c='m') # (Experimental vs. Theoretical)
