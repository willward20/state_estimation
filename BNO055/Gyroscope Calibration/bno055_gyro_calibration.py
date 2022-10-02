######################################################
# Copyright (c) 2021 Maker Portal LLC
# Author: Joshua Hrisko
######################################################
#
# This code reads data from the MPU9250/MPU9265 board
# (MPU6050 - accel/gyro, AK8963 - mag)
# and solves for calibration coefficients for the
# gyroscope
#
# I modified his original file to calibrate the bno055
######################################################
#
# wait 5-sec for IMU to connect
import time,sys
sys.path.append("../")
t0 = time.time()
import board
import busio
import adafruit_bno055

import numpy as np
import csv,datetime
import matplotlib.pyplot as plt

time.sleep(2) # wait for MPU to load and settle

i2c = busio.I2C(board.SCL, board.SDA) # define board.I2C object
sensor = adafruit_bno055.BNO055_I2C(i2c) # create sensor object

PI = 3.14159265359

# 
#####################################
# Gyro calibration (Steady)
#####################################
#
def get_gyro():
    wx = sensor.gyro[0] * 180 / PI # read gyro data
    wy = sensor.gyro[1] * 180 / PI
    wz = sensor.gyro[2] * 180 / PI
    return wx,wy,wz

def gyro_cal():
    print("-"*50)
    print('Gyro Calibrating - Keep the IMU Steady')
    [get_gyro() for ii in range(0,cal_size)] # clear buffer before calibration
    bno_array = []
    gyro_offsets = [0.0,0.0,0.0]
    while True:
        try:
            wx,wy,wz = get_gyro() # get gyro vals
        except:
            continue

        bno_array.append([wx,wy,wz])

        if np.shape(bno_array)[0]==cal_size:
            for qq in range(0,3):
                gyro_offsets[qq] = np.mean(np.array(bno_array)[:,qq]) # average
            break
    print('Gyro Calibration Complete')
    return gyro_offsets

if __name__ == '__main__':
    #
    ###################################
    # Gyroscope Offset Calculation
    ###################################
    #
    gyro_labels = ['w_x','w_y','w_z'] # gyro labels for plots
    cal_size = 500 # points to use for calibration
    gyro_offsets = gyro_cal() # calculate gyro offsets
    #
    ###################################
    # Record new data 
    ###################################
    #
    data = np.array([get_gyro() for ii in range(0,cal_size)]) # new values
    #
    ###################################
    # Plot with and without offsets
    ###################################
    #
    plt.style.use('ggplot')
    fig,axs = plt.subplots(2,1,figsize=(12,9))
    for ii in range(0,3):
        axs[0].plot(data[:,ii],
                    label='${}$, Uncalibrated'.format(gyro_labels[ii]))
        axs[1].plot(data[:,ii]-gyro_offsets[ii],
                    label='${}$, Calibrated'.format(gyro_labels[ii]))
    axs[0].legend(fontsize=14);axs[1].legend(fontsize=14)
    axs[0].set_ylabel('$w_{x,y,z}$ [$^{\circ}/s$]',fontsize=18)
    axs[1].set_ylabel('$w_{x,y,z}$ [$^{\circ}/s$]',fontsize=18)
    axs[1].set_xlabel('Sample',fontsize=18)
    axs[0].set_ylim([-4, 4]);axs[1].set_ylim([-4, 4])
    axs[0].set_title('BNO055 Gyroscope Calibration Offset Correction',fontsize=22)
    fig.savefig('bno055_gyro_calibration_output.png',dpi=300,
                bbox_inches='tight',facecolor='#FCFCFC')
    #fig.show()

