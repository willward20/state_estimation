######################################################
# Copyright (c) 2021 Maker Portal LLC
# Author: Joshua Hrisko
######################################################
#
# This code reads data from the MPU9250/MPU9265 board
# (MPU6050 - accel/gyro, AK8963 - mag)
# and solves for calibration coefficients for the
# accelerometer
#
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
    
    plot_velocity(time_array, [uncal_x_velocity, uncal_y_velocity, uncal_z_velocity], [cal_x_velocity, cal_y_velocity, cal_z_velocity])

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

    ###################################
    # Plot 
    ###################################
    plt.style.use('ggplot')
    fig,axs = plt.subplots(2,1,figsize=(12,9))
    for ii in range(0,3):
        axs[0].plot(time_array, (uncal_accel_array)[ii],
                    label='${}$, Uncalibrated'.format(accel_labels[ii]))
        axs[1].plot(time_array, (cal_accel_array)[ii],
                    label='${}$, Calibrated'.format(accel_labels[ii]))
    axs[0].legend(fontsize=14);axs[1].legend(fontsize=14)
    axs[0].set_ylabel('$d_{x,y,z}$ [m]',fontsize=18)
    axs[1].set_ylabel('$d_{x,y,z}$ [m]',fontsize=18)
    axs[1].set_xlabel('Time (seconds)',fontsize=18)
    #axs[0].set_ylim([-2,2]);axs[1].set_ylim([-2,2])
    axs[0].set_title('Y-Forward 1: Displacement Over Time (meters)',fontsize=18)
    fig.savefig('y_track_1_dist.png',dpi=300,
                bbox_inches='tight',facecolor='#FCFCFC')
    fig.show()

    return

def plot_velocity(time_array, uncal_accel_array, cal_accel_array):

    ###################################
    # Plot 
    ###################################
    plt.style.use('ggplot')
    fig,axs = plt.subplots(2,1,figsize=(12,9))
    for ii in range(0,3):
        axs[0].plot(time_array, (uncal_accel_array)[ii],
                    label='${}$, Uncalibrated'.format(accel_labels[ii]))
        axs[1].plot(time_array, (cal_accel_array)[ii],
                    label='${}$, Calibrated'.format(accel_labels[ii]))
    axs[0].legend(fontsize=14);axs[1].legend(fontsize=14)
    axs[0].set_ylabel('$v_{x,y,z}$ [m/s]',fontsize=18)
    axs[1].set_ylabel('$v_{x,y,z}$ [m/s]',fontsize=18)
    axs[1].set_xlabel('Time (seconds)',fontsize=18)
    #axs[0].set_ylim([-2,2]);axs[1].set_ylim([-2,2])
    axs[0].set_title('Y-Forward 1: Velocity Over Time (meters/second)',fontsize=18)
    fig.savefig('y_track_1_vel.png',dpi=300,
                bbox_inches='tight',facecolor='#FCFCFC')
    fig.show()

    return


def plot_accel_no_g(time_array, uncal_accel_array, cal_accel_array):

    ###################################
    # Plot 
    ###################################
    plt.style.use('ggplot')
    fig,axs = plt.subplots(2,1,figsize=(12,9))
    for ii in range(0,3):
        axs[0].plot(time_array, np.transpose(uncal_accel_array)[ii],
                    label='${}$, Uncalibrated'.format(accel_labels[ii]))
        axs[1].plot(time_array, np.transpose(cal_accel_array)[ii],
                    label='${}$, Calibrated'.format(accel_labels[ii]))
    axs[0].legend(fontsize=14);axs[1].legend(fontsize=14)
    axs[0].set_ylabel('$a_{x,y,z}$ [m/s/s]',fontsize=18)
    axs[1].set_ylabel('$a_{x,y,z}$ [m/s/s]',fontsize=18)
    axs[1].set_xlabel('Time (seconds)',fontsize=18)
    #axs[0].set_ylim([-2,2]);axs[1].set_ylim([-2,2])
    axs[0].set_title('Y-Forward 1: Acceleration of the Cart Minus Gravity (m/s/s)',fontsize=18)
    fig.savefig('y_track_1_accel_no_g.png',dpi=300,
                bbox_inches='tight',facecolor='#FCFCFC')
    fig.show()

    return

if __name__ == '__main__':
    
    mpu_labels = ['a_x','a_y','a_z'] # gyro labels for plots 

    ###################################
    # Read data from .csv file 
    ###################################

    CSVData = open("Aluminum_Track_Trials/Track_Trials_Y_Forward/Trial_1/y_track_1.csv")
    csv_data = np.loadtxt(CSVData, skiprows = 1, delimiter=",", dtype=float)

    time_array = csv_data[:, 0]
    uncal_accel_array = csv_data[:, [1, 2, 3]]
    cal_accel_array = csv_data[:, [4, 5, 6]]

    ###################################
    # Graph .csv data to double check 
    ###################################

    #plot_csv(time_array, uncal_accel_array, cal_accel_array)
    #exit()

    ###################################
    # Convert g to m/s/s
    ###################################
    uncal_accel_array *= 9.80665 # converts to m/s/s
    cal_accel_array *= 9.80665   # converts to m/s/s

    # these change depending on which axis is forward and up/down
    # Z-Forward / X-Down
    # Y-Forward / Z-Up
    # X-Forward / Z-Up
    uncal_accel_array[:, 0] += (9.80665 * math.cos(math.radians(1))) # remove perpendicular gravity component due to 1 degree incline
    uncal_accel_array[:, 2] += (9.80665 * math.sin(math.radians(1))) # remove parallel gravity component due to 1 degree incline
    cal_accel_array[:, 0] += (9.80665 * math.cos(math.radians(1)))   # remove perpendicular gravity component due to 1 degree incline
    cal_accel_array[:, 2] += (9.80665 * math.sin(math.radians(1)))   # remove parallel gravity component due to 1 degree incline

    plot_accel_no_g(time_array, uncal_accel_array, cal_accel_array)
    #input("press enter")
    #exit()

    ###################################
    # integration over time
    ###################################
    
    cal_displacement, uncal_displacement = imu_integrator(time_array, cal_accel_array, uncal_accel_array)

    plot_displacement(time_array, uncal_displacement, cal_displacement)
    #input("press enter")
