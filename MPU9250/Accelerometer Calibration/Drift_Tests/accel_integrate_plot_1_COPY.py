######################################################
# Copyright (c) 2021 Maker Portal LLC
# Author: Joshua Hrisko
# Modified by Will Ward
######################################################
#
# This code (1) reads the csv accelerometer data and 
# integrates it twice to get arrays for velocity and 
# displacement. (2) Plots the acceleration, velocity,
# and displacement in three different png files. The 
# image files show two plots for calibrated and 
# uncalibrated data. On each plot, all three axes are
# plotted together 
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
from graph_mean import mean_array

time.sleep(2) # wait for MPU to load and settle
accel_labels = ['a_x','a_y','a_z']

def imu_integrator(time_array, cal_accel_array, uncal_accel_array):

    ###################################
    # Integrate Data Twice 
    ###################################
    
    cal_x_velocity = np.append(0.0, cumtrapz(cal_accel_array[:,0],x=time_array))
    cal_y_velocity = np.append(0.0, cumtrapz(cal_accel_array[:,1],x=time_array))
    cal_z_velocity = np.append(0.0, cumtrapz(cal_accel_array[:,2],x=time_array))

    uncal_x_velocity = np.append(0.0, cumtrapz(uncal_accel_array[:,0],x=time_array))
    uncal_y_velocity = np.append(0.0, cumtrapz(uncal_accel_array[:,1],x=time_array))
    uncal_z_velocity = np.append(0.0, cumtrapz(uncal_accel_array[:,2],x=time_array))
    
    #plot_velocity(time_array, [uncal_x_velocity, uncal_y_velocity, uncal_z_velocity], [cal_x_velocity, cal_y_velocity, cal_z_velocity])

    cal_x_displacement = np.append(0.0, cumtrapz(cal_x_velocity, x=time_array))
    cal_y_displacement = np.append(0.0, cumtrapz(cal_y_velocity, x=time_array))
    cal_z_displacement = np.append(0.0, cumtrapz(cal_z_velocity, x=time_array))
    
    uncal_x_displacement = np.append(0.0, cumtrapz(uncal_x_velocity, x=time_array))
    uncal_y_displacement = np.append(0.0, cumtrapz(uncal_y_velocity, x=time_array))
    uncal_z_displacement = np.append(0.0, cumtrapz(uncal_z_velocity, x=time_array))
    
    # print out reuslts
    print("Calibrated Displacement of ax: ", cal_x_displacement[-1]," meters")
    print("Calibrated Integration of ay: ", cal_y_displacement[-1]," meters")
    print("Calibrated Integration of az: ", cal_z_displacement[-1]," meters")
    
    print("Uncalibrated Integration of ax: ", uncal_x_displacement[-1]," meters")
    print("Uncalibrated Integration of ay: ", uncal_y_displacement[-1]," meters")
    print("Uncalibrated Integration of az: ", uncal_z_displacement[-1]," meters")
    
    print(cal_x_displacement.shape)

    cal_displacement = [cal_x_displacement, cal_y_displacement, cal_z_displacement]
    uncal_displacement = [uncal_x_displacement, uncal_y_displacement, uncal_z_displacement]

    return cal_displacement, uncal_displacement
    
def plot_displacement(time_array, uncal_accel_array, cal_accel_array):

    # Retrieve the mean displacement array
    mean_x_dis, mean_y_dis, mean_z_dis = mean_array(time_array, 0.04405, 0.17543, -0.01615) # use mean values from the calibrate sheets

    ###################################
    # Plot 
    ###################################
    plt.style.use('ggplot')
    fig,axs = plt.subplots(1,1,figsize=(12,9))
    for ii in range(0,3):
        #axs[0].plot(time_array, (uncal_accel_array)[ii],
        #            label='${}$, Uncalibrated'.format(accel_labels[ii]))
        axs.plot(time_array, (cal_accel_array)[ii],
                    label='${}$, Calibrated'.format(accel_labels[ii]))
    axs.plot(time_array, mean_x_dis, label='X Mean', c='r')
    axs.plot(time_array, mean_y_dis, label='Y Mean', c='b')
    axs.plot(time_array, mean_z_dis, label='Z Mean', c='m')
    #axs[0].legend(fontsize=14)
    axs.legend(fontsize=14)
    #axs[0].set_ylabel('$d_{x,y,z}$ [m]',fontsize=18)
    axs.set_ylabel('$d_{x,y,z}$ [m]',fontsize=18)
    axs.set_xlabel('Time (seconds)',fontsize=18)
    #axs[0].set_ylim([-2,2]);axs[1].set_ylim([-2,2])
    axs.set_title('Drift Test IMU at Rest VS Mean: Z Up [Minus Gravity]',fontsize=18)
    fig.savefig('accel_drift_still_z_up_dist_VS_mean.png',dpi=300,
                bbox_inches='tight',facecolor='#FCFCFC')
    fig.show()

    return



if __name__ == '__main__':
    
    ###################################
    # Read data from .csv file 
    ###################################

    CSVData = open("Drift_Tests/Z_Up_Data/accel_drift_still_z_up.csv")
    csv_data = np.loadtxt(CSVData, skiprows = 1, delimiter=",", dtype=float)

    time_array = csv_data[:, 0]
    uncal_accel_array = csv_data[:, [1, 2, 3]]
    cal_accel_array = csv_data[:, [4, 5, 6]]

    ###################################
    # Convert g to m/s/s
    ###################################
    uncal_accel_array *= 9.80665 # converts to m/s/s
    cal_accel_array *= 9.80665   # converts to m/s/s

    # these change depending on which axis is forward and up/down
    # Z-Forward / X-Down
    # Y-Forward / Z-Up
    # X-Forward / Z-Up
    uncal_accel_array[:, 2] -= (9.80665 * math.cos(math.radians(1))) # remove perpendicular gravity component due to 1 degree incline
    # DON'T remove gravity component from the axis parallel to the track because it is unopposed when in motion. 
    cal_accel_array[:, 2] -= (9.80665 * math.cos(math.radians(1)))   # remove perpendicular gravity component due to 1 degree incline
    # DON'T remove gravity component from the axis parallel to the track because it is unopposed when in motion. 

    #plot_accel(time_array, uncal_accel_array, cal_accel_array)
    #input("press enter")
    #exit()

    ###################################
    # integration over time
    ###################################
    
    cal_displacement, uncal_displacement = imu_integrator(time_array, cal_accel_array, uncal_accel_array)

    plot_displacement(time_array, uncal_displacement, cal_displacement)
    #input("press enter")
