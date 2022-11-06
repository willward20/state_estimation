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

time.sleep(2) # wait for MPU to load and settle

#####################################
# Collect Accel Data using Calibration Coefficients
#####################################

accel_labels = ['a_x','a_y','a_z'] # gyro labels for plots
accel_coeffs = [[ 0.99993400, -0.09561477],
                [ 0.99952689 , -0.04496953], [0.97564724, 0.25164068]]


def calibrate(data):
    calibrated_data = []
    for ii in range(0, len(data)):
        calibrated_data.append([(accel_fit(data[ii][0], accel_coeffs[0][0],accel_coeffs[0][1])),
                                (accel_fit(data[ii][1], accel_coeffs[1][0],accel_coeffs[1][1])),
                                (accel_fit(data[ii][2], accel_coeffs[2][0],accel_coeffs[2][1]))])
    
    return calibrated_data

def accel_fit(x_input,m_x,b):
    return (m_x*x_input)+b # fit equation for accel calibration

def get_accel():
    accels = [0, 0, 0]
    ax,ay,az,_,_,_ = mpu6050_conv() # read and convert accel data
    accels[0] = ax
    accels[1] = ay
    accels[2] = az
    return accels

if __name__ == '__main__':
    if not start_bool:
        print("IMU not Started - Check Wiring and I2C")
    else:
        #
        ###################################
        # Accelerometer Gravity Calibration
        ###################################
        #
        print("Starting Up")
        
        data = []
        time_elapsed = []
        
        input("Press Enter to Begin")
        start_time = time.time()
        
        while True:
            try:
                data.append(get_accel()) # new values
                time_elapsed.append(time.time() - start_time)
            
            except KeyboardInterrupt:
                break
            
        calibrated_data = calibrate(data)
        
        # Save data point to a file 
        file = open('bounce_5.csv', 'a')
        file.write('time (seconds)' + ',' + 'uncal_x' + ',' + 'uncal_y' + ',' + 'uncal_z' + ',' +
                   'cal_x' + ',' + 'cal_y' + ',' + 'cal_z' + '\n')
        for i in range(0, len(time_elapsed)):
            file.write(str(time_elapsed[i]) + ',' + str(data[i][0]) + ',' + str(data[i][1]) + ',' + str(data[i][2])
                       + ',' + str(calibrated_data[i][0]) + ',' + str(calibrated_data[i][1]) + ','
                       + str(calibrated_data[i][2]) + '\n')
        file.close()
        
        
        #
        ###################################
        # Plot with and without offsets
        ###################################
        #
        
        #print("data: ", data)
        #print("calibrated_data: ", calibrated_data)
        #print("time_elapsed: ", time_elapsed)
        
        plt.style.use('ggplot')
        fig,axs = plt.subplots(2,1,figsize=(12,9))
        for ii in range(0,3):
            axs[0].plot(time_elapsed, np.transpose(data)[ii],
                        label='${}$, Uncalibrated'.format(accel_labels[ii]))
            axs[1].plot(time_elapsed, np.transpose(calibrated_data)[ii],
                        label='${}$, Calibrated'.format(accel_labels[ii]))
        axs[0].legend(fontsize=14);axs[1].legend(fontsize=14)
        axs[0].set_ylabel('$a_{x,y,z}$ [g]',fontsize=18)
        axs[1].set_ylabel('$a_{x,y,z}$ [g]',fontsize=18)
        axs[1].set_xlabel('Time (seconds)',fontsize=18)
        axs[0].set_ylim([-2,2]);axs[1].set_ylim([-2,2])
        axs[0].set_title('Bounce Cart on Track: Z Forward (Trial 5)',fontsize=18)
        fig.savefig('bounce_5.png',dpi=300,
                    bbox_inches='tight',facecolor='#FCFCFC')
        fig.show()
        


