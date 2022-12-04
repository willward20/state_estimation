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
    plt.style.use('ggplot')
    fig,axs = plt.subplots(3,1,figsize=(12,9))
    axs[0].plot(time_array, cal_accel, color = c)
    axs[1].plot(time_array, cal_vel, color = c)
    axs[2].plot(time_array, cal_dis, color = c)
    axs[0].set_ylabel('Accel (NO g) [m/s/s]',fontsize=18)
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

    CSVData = open("Aluminum_Track_Trials/Track_Trials_Z_Forward/Trial_3/z_track_3.csv")
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

    # These change depending on which axis is forward and which axis is up/down
    cal_x_accel += (9.80665 * math.cos(math.radians(1)))   # remove perpendicular gravity component due to 1 degree incline
    cal_z_accel -= (9.80665 * math.sin(math.radians(1)))   # remove parallel gravity component due to 1 degree incline
    
    ###################################
    # integration over time
    ###################################
    cal_x_vel, cal_x_dis = imu_integrator(time_array, cal_x_accel)
    cal_y_vel, cal_y_dis = imu_integrator(time_array, cal_y_accel)
    cal_z_vel, cal_z_dis = imu_integrator(time_array, cal_z_accel)

    #plot_total(time_array, cal_x_accel, cal_x_vel, cal_x_dis, 'Z Forward Trial 2: X Axis', 'z_track_2_x.png', c='r')
    #plot_total(time_array, cal_y_accel, cal_y_vel, cal_y_dis, 'Z Forward Trial 2: Y Axis', 'z_track_2_y.png', c='b')
    plot_total(time_array, cal_z_accel, cal_z_vel, cal_z_dis, 'Z Forward Trial 3: Z Axis', 'z_track_3_z.png', c='m')
