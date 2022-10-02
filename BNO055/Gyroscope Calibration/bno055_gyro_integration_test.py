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
from scipy.integrate import cumtrapz

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
    gyro_labels = ['\omega_x','\omega_y','\omega_z'] # gyro labels for plots
    cal_size = 500 # points to use for calibration
    gyro_offsets = gyro_cal() # calculate gyro offsets
    #
    ###################################
    # Record new data 
    ###################################
    #
    input("Press Enter and Rotate Gyro 360 degrees")
    print("Recording Data...")
    record_time = 20 # how long to record
    data,t_vec = [],[]
    t0 = time.time()
    while time.time()-t0<record_time:
        wx,wy,wz = get_gyro()
        if ((wz < -500) or (wz > 500)):
            print(wz)
        else:
            data.append(get_gyro())
            t_vec.append(time.time()-t0)
    samp_rate = np.shape(data)[0]/(t_vec[-1]-t_vec[0]) # sample rate
    print("Stopped Recording\nSample Rate: {0:2.0f} Hz".format(samp_rate))
    #
    ##################################
    # Offset and Integration of gyro
    # and plotting results
    ##################################
    #
    rot_axis = 2 # axis being rotated (2 = z-axis)
    data_offseted = np.array(data)[:,rot_axis]-gyro_offsets[rot_axis]
    integ1_array = cumtrapz(data_offseted,x=t_vec) # integrate once in time
    #
    # print out reuslts
    print("Integration of {} in {}".format(gyro_labels[rot_axis],
                   gyro_labels[rot_axis].split("_")[1])+\
          "-dir: {0:2.2f} degrees".format(integ1_array[-1]))
    #
    # plotting routine
    plt.style.use('ggplot')
    fig,axs = plt.subplots(2,1,figsize=(12,9))
    axs[0].plot(t_vec,data_offseted,label="$"+gyro_labels[rot_axis]+"$")
    axs[1].plot(t_vec[1:],integ1_array,
                label=r"$\theta_"+gyro_labels[rot_axis].split("_")[1]+"$")
    [axs[ii].legend(fontsize=16) for ii in range(0,len(axs))]
    axs[0].set_ylabel('Angular Velocity, $\omega_{}$ [$^\circ/s$]'.format(gyro_labels[rot_axis].\
                                       split("_")[1]),fontsize=16)
    axs[1].set_ylabel(r'Rotation, $\theta_{}$ [$^\circ$]'.format(gyro_labels[rot_axis].\
                                           split("_")[1]),fontsize=16)
    axs[1].set_xlabel('Time [s]',fontsize=16)
    axs[0].set_title('BNO055 Gyroscope Integration over 360 then back to 0 (Edited)$^\circ$ Rotation',
                     fontsize=18)
    fig.savefig('bno055_gyroscope_integration_net_zero_edited.png',dpi=300,
                bbox_inches='tight',facecolor='#FFFFFF')
    plt.show()


