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

def imu_integrator(time_array, cal_accel_array, uncal_accel_array):

    ###################################
    # Integrate Data Twice 
    ###################################
    
    cal_x_displacement = trapz(np.append(0.0, cumtrapz(cal_accel_array[:,0],x=time_array)), x=time_array)
    cal_y_displacement = trapz(np.append(0.0, cumtrapz(cal_accel_array[:,1],x=time_array)), x=time_array)
    cal_z_displacement = trapz(np.append(0.0, cumtrapz(cal_accel_array[:,2],x=time_array)), x=time_array)
    
    uncal_x_displacement = trapz(np.append(0.0, cumtrapz(uncal_accel_array[:,0],x=time_array)), x=time_array)
    uncal_y_displacement = trapz(np.append(0.0, cumtrapz(uncal_accel_array[:,1],x=time_array)), x=time_array)
    uncal_z_displacement = trapz(np.append(0.0, cumtrapz(uncal_accel_array[:,2],x=time_array)), x=time_array)
    
    # print out reuslts
    print("Calibrated Displacement of ax: ", cal_x_displacement," meters")
    print("Calibrated Integration of ay: ", cal_y_displacement," meters")
    print("Calibrated Integration of az: ", cal_z_displacement," meters")
    
    print("Uncalibrated Integration of ax: ", uncal_x_displacement," meters")
    print("Uncalibrated Integration of ay: ", uncal_y_displacement," meters")
    print("Uncalibrated Integration of az: ", uncal_z_displacement," meters")
    
    return 0.0, 0.0
    
def plot_integration():

    ###################################
    # Plot 
    ###################################
    """
    plt.style.use('ggplot')
    fig,axs = plt.subplots(2,1,figsize=(12,9))
    for ii in range(0,3):
        axs[0].plot(GYRO_ARRAY[:,ii],
                    label='${}$, Angular Velocity'.format(gyro_labels[ii]))
        axs[1].plot(STDEV[:,ii],
                    label='${}$, Standard Deviation'.format(gyro_labels[ii]))
    axs[0].legend(fontsize=14);axs[1].legend(fontsize=14)
    axs[0].set_ylabel('$w_{x,y,z}$ [$^{\circ}/s$]',fontsize=18)
    axs[1].set_ylabel('$w_{x,y,z}$ [$^{\circ}/s$]',fontsize=18)
    axs[1].set_xlabel('Sample (taken over approximately 60 seconds)',fontsize=18)
    axs[0].set_ylim([-2,2]);axs[1].set_ylim([-2,2])
    axs[0].set_title('MPU9250 Gyroscope Calibrated Collected Data while at Rest',fontsize=22)
    fig.savefig('gyro_collect.png',dpi=300,
                bbox_inches='tight',facecolor='#FCFCFC')
    fig.show()
    """
    return


if __name__ == '__main__':
    
    mpu_labels = ['a_x','a_y','a_z'] # gyro labels for plots 

    ###################################
    # Read data from .csv file 
    ###################################

    CSVData = open("Aluminum_Track_Trials/z_track_1.csv")
    csv_data = np.loadtxt(CSVData, skiprows = 1, delimiter=",", dtype=float)

    time_array = csv_data[:, 0]
    uncal_accel_array = csv_data[:, [1, 2, 3]]
    cal_accel_array = csv_data[:, [4, 5, 6]]

    ###################################
    # Convert g to m/s/s
    ###################################
    uncal_accel_array = (uncal_accel_array * 9.80665)
    cal_accel_array = (uncal_accel_array * 9.80665) 

    uncal_accel_array[:, 0] += (9.80665 * math.cos(math.radians(1))) # remove gravity component due to 1 degree incline
    uncal_accel_array[:, 2] += (9.80665 * math.sin(math.radians(1)))
    cal_accel_array[:, 0] += (9.80665 * math.cos(math.radians(1))) # remove gravity component due to 1 degree incline
    cal_accel_array[:, 2] += (9.80665 * math.sin(math.radians(1)))

    ###################################
    # integration over time
    ###################################
    
    cal_integ_array, uncal_integ_array = imu_integrator(time_array, cal_accel_array, uncal_accel_array)
