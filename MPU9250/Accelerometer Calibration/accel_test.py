######################################################
# Copyright (c) 2021 Maker Portal LLC
# Author: Joshua Hrisko
# Modified by Will Ward
######################################################
#
# I'm fairly confident that I used this script to create 
# the graphs in the Calibration Trials folder. I must 
# have used a differnt script to record calibration constants,
# and then I used thos constants to calibrated accel data
# when the device is stationary for three orientations:
# x down, y up, and z up. I don't know exactly what constants
# were used, but I can assume that the same constants were
# at least used for each of the three images in one Trial. 
# Whether the same constants were used for each of the 
# three trials is unknown. 
#
# It would not be hard to repeat this test in the future,
# if I needed to. I think the point is to show that the 
# accuracy of the calibration is not significantly impacted
# by the ortientation of the cube. 
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

time.sleep(2) # wait for MPU to load and settle

#####################################
# Accel Calibration Test
#####################################

def accel_fit(x_input,m_x,b):
    return (m_x*x_input)+b # fit equation for accel calibration
#
def get_accel():
    ax,ay,az,_,_,_ = mpu6050_conv() # read and convert accel data
    return ax,ay,az

if __name__ == '__main__':
    if not start_bool:
        print("IMU not Started - Check Wiring and I2C")
    else:
        #
        ###################################
        # Accelerometer Gravity Calibration
        ###################################
        #
        accel_labels = ['a_x','a_y','a_z'] # gyro labels for plots
        cal_size = 100 # number of points to use for calibration 
        # Sample calibration values collected on 10/24
        accel_coeffs = [np.array([ 0.99991705, -0.09120736]),
                        np.array([ 0.9996431 , -0.04407273]), np.array([0.97755523, 0.23932943])] 
        print("accel_coeffs: ", accel_coeffs)
        ###################################
        # Record new data 
        ###################################
        #
        
        while True:
            try:
                data = np.array([get_accel()]) # new values
                calibrated_data = []
                for ii in range(0, len(accel_labels)):
                    calibrated_data.append(accel_fit(data[:,ii],*accel_coeffs[ii]))
                print("x: ", calibrated_data[0], "   y: ", calibrated_data[1], "   z: ", calibrated_data[2])
                time.sleep(0.5)
            
            except:
                break
        
        input("Press Enter and Keep IMU Steady to Calibrate the Accelerometer")
       
        data = np.array([get_accel() for ii in range(0,cal_size)]) # new values
        
        #
        ###################################
        # Plot with and without offsets
        ###################################
        #
        
        plt.style.use('ggplot')
        fig,axs = plt.subplots(2,1,figsize=(12,9))
        for ii in range(0,3):
            axs[0].plot(data[:,ii],
                        label='${}$, Uncalibrated'.format(accel_labels[ii]))
            axs[1].plot(accel_fit(data[:,ii],*accel_coeffs[ii]),
                        label='${}$, Calibrated'.format(accel_labels[ii]))
        axs[0].legend(fontsize=14);axs[1].legend(fontsize=14)
        axs[0].set_ylabel('$a_{x,y,z}$ [g]',fontsize=18)
        axs[1].set_ylabel('$a_{x,y,z}$ [g]',fontsize=18)
        axs[1].set_xlabel('Sample',fontsize=18)
        axs[0].set_ylim([-2,2]);axs[1].set_ylim([-2,2])
        axs[0].set_title('Accelerometer Calibration Trial 3: z Pointed Up',fontsize=18)
        fig.savefig('accel_calibration_trial_3_z_up.png',dpi=300,
                    bbox_inches='tight',facecolor='#FCFCFC')
        fig.show()
        

