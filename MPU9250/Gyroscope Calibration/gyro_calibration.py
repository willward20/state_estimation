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
#
######################################################
#
# wait 5-sec for IMU to connect
import time,sys
sys.path.append("../")
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
import statistics

time.sleep(2) # wait for MPU to load and settle
# 
#####################################
# Gyro calibration (Steady)
#####################################
#
def get_gyro():
    _,_,_,wx,wy,wz = mpu6050_conv() # read and convert gyro data
    return wx,wy,wz

def gyro_cal():
    print("-"*50)
    print('Gyro Calibrating - Keep the IMU Steady')
    [get_gyro() for ii in range(0,cal_size)] # clear buffer before calibration
    mpu_array = []
    gyro_offsets = [0.0,0.0,0.0]
    while True:
        try:
            wx,wy,wz = get_gyro() # get gyro vals
        except:
            continue

        mpu_array.append([wx,wy,wz])

        if np.shape(mpu_array)[0]==cal_size:
            for qq in range(0,3):
                gyro_offsets[qq] = np.mean(np.array(mpu_array)[:,qq]) # average
            break
    print('Gyro Calibration Complete')
    return gyro_offsets

if __name__ == '__main__':
    if not start_bool:
        print("IMU not Started - Check Wiring and I2C")
    else:
        #
        ###################################
        # Gyroscope Offset Calculation
        ###################################
        #
        gyro_labels = ['w_x','w_y','w_z'] # gyro labels for plots
        cal_size = 10000 # points to use for calibration
        gyro_offsets = gyro_cal() # calculate gyro offsets
        print("gyro_offsets: ", gyro_offsets)
        #
        ###################################
        # Record new data 
        ###################################
        #
        print("collecting")
        data = np.array([get_gyro() for ii in range(0,cal_size)]) # new values
        print("size of data: ", (data.T).shape)
        print(data.T[0])
        print("Standard deviation of uncalibrated sample is: ",
              "\n    w_x: ", statistics.stdev(data.T[0]), " deg/sec",
              "\n    w_y: ", statistics.stdev(data.T[1]), " deg/sec",
              "\n    w_z: ", statistics.stdev(data.T[2]), " deg/sec")
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
        axs[0].set_ylim([-4,4]);axs[1].set_ylim([-4,4])
        axs[0].set_title('MPU9250 Gyroscope Calibration Offset Correction',fontsize=22)
        fig.savefig('gyro_calibration_output.png',dpi=300,
                    bbox_inches='tight',facecolor='#FCFCFC')
        fig.show()
        
