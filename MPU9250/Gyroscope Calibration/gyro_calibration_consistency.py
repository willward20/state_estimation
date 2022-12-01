######################################################
# Copyright (c) 2021 Maker Portal LLC
# Author: Joshua Hrisko
######################################################
#
# This code reads data from the MPU9250 gyroscope,
# averaging readings every 0.1 seconds. The data
# is calibrated using coefficients averaged from 9
# calibration trials. The calibrated data and the
# calculated stdev are both graphed. 
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
    cal_size = 1000
    print("-"*50)
    print('Gyro Calibrating - Keep the IMU Steady')
    [get_gyro() for ii in range(0,cal_size)] # clear buffer before calibration
    mpu_array = []
    gyro_offsets = [0.0,0.0,0.0]
    start_time = time.time()
    
    while True:
        try:
            wx,wy,wz = get_gyro() # get gyro vals
        except:
            continue

        mpu_array.append([wx,wy,wz])
        
        if np.shape(mpu_array)[0]==cal_size:
            print('Gyro Calibration Complete. Sample Rate: ', cal_size / (time.time() - start_time))
            for qq in range(0,3):
                gyro_offsets[qq] = np.mean(np.array(mpu_array)[:,qq]) # average
            break
        
        time.sleep(0.01)
        
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
        gyro_offsets = gyro_cal()
        print("gyro_offsets: ", gyro_offsets)
        
        ###################################
        # Record new data 
        ###################################
        
        GYRO_ARRAY = []
        #STDEV = []
        
        START_TIME = time.time()
        while (time.time() - START_TIME) < 60*5: # collect for a total of approximately 60 seconds
            gyro_array = []
            start_time = time.time()
            while (time.time() - start_time) < 1: # collect for no more than 0.1 seconds
                wx,wy,wz = get_gyro() # get gyro vals
                gyro_array.append([wx,wy,wz])
            
            gyro_array = np.array(gyro_array) # convert to np array to perform operations
            gyro_array = np.subtract(gyro_array, np.array(gyro_offsets)) # subtraqct offsets
            
            mean_gyro_x = np.mean(gyro_array[:,0]) # average all of the x measurements
            mean_gyro_y = np.mean(gyro_array[:,1]) # average all of the y measurements
            mean_gyro_z = np.mean(gyro_array[:,2]) # average all of the z measurements
            
            GYRO_ARRAY.append([mean_gyro_x, mean_gyro_y, mean_gyro_z]) # record average readings over 0.1 seconds
            
            #stdev_x = statistics.stdev(gyro_array.T[0]) / (len(gyro_array[0])**0.5) # calculate estimated uncertainty in the average (SDOM)
            #stdev_y = statistics.stdev(gyro_array.T[1]) / (len(gyro_array[1])**0.5) # calculate estimated uncertainty in the average (SDOM)
            #stdev_z = statistics.stdev(gyro_array.T[2]) / (len(gyro_array[2])**0.5) # calculate estimated uncertainty in the average (SDOM)
            if (time.time() - START_TIME) < 60*1:
                print("1 Z UP")
            elif (time.time() - START_TIME) > 60*1 and (time.time() - START_TIME) < 60*2:
                print("2 Y UP")
            elif (time.time() - START_TIME) > 60*2 and (time.time() - START_TIME) < 60*3:
                print("3 X UP")
            elif (time.time() - START_TIME) > 60*3 and (time.time() - START_TIME) < 60*4:
                print("4 X DOWN")
            elif (time.time() - START_TIME) > 60*4 and (time.time() - START_TIME) < 60*5:
                print("5 Z UP")
            #STDEV.append([stdev_x, stdev_y, stdev_z])
            
                
        GYRO_ARRAY = np.array(GYRO_ARRAY)
        #STDEV = np.array(STDEV)
        
        print("size of data: ", (GYRO_ARRAY.T).shape)
        #print(data.T[0])
        #print("Standard deviations of all data is: ",
        #      "\n    w_x: ", statistics.stdev(GYRO_ARRAY.T[0]), " deg/sec",
        #      "\n    w_y: ", statistics.stdev(GYRO_ARRAY.T[1]), " deg/sec",
        #      "\n    w_z: ", statistics.stdev(GYRO_ARRAY.T[2]), " deg/sec")
        
        ###################################
        # Plot 
        ###################################
        
        
        plt.style.use('ggplot')
        fig,axs = plt.subplots(3,1,figsize=(12,9))
        axs[0].plot(GYRO_ARRAY[:,0], color = 'r', label='${}$, Angular Velocity'.format(gyro_labels[0]))
        axs[1].plot(GYRO_ARRAY[:,1], color = 'g', label='${}$, Angular Velocity'.format(gyro_labels[1]))
        axs[2].plot(GYRO_ARRAY[:,2], color = 'b', label='${}$, Angular Velocity'.format(gyro_labels[2]))
        
        axs[0].legend(fontsize=14)
        axs[1].legend(fontsize=14)
        axs[2].legend(fontsize=14)
        
        axs[0].set_ylabel('$w_{x}$ [$^{\circ}/s$]',fontsize=18)
        axs[1].set_ylabel('$w_{y}$ [$^{\circ}/s$]',fontsize=18)
        axs[2].set_ylabel('$w_{z}$ [$^{\circ}/s$]',fontsize=18)
        
        axs[2].set_xlabel('Sample (taken over approximately 5 Minutes)',fontsize=18)
        axs[0].set_ylim([-0.2,0.2])
        axs[1].set_ylim([-0.2,0.2])
        axs[2].set_ylim([-0.2,0.2])
        axs[0].set_title('MPU9250 Gyroscope Calibrated 2D Rotate90cw-Return (Avg each second)',fontsize=22)
        fig.savefig('calibrate_rotate_2D_return_5_min.png',dpi=300,
                    bbox_inches='tight',facecolor='#FCFCFC')
        fig.show()


