"""
This program collects data from the MPU-9250 accelerometer.

"""

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
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import math

time.sleep(2) # wait for MPU to load and settle


def get_accel():
    ax,ay,az,_,_,_ = mpu6050_conv() # read and convert accel data
    return ax,ay,az

    
def accel_cal(total_time):

    ##############################
    # Collect data for each angle
    ##############################

    start_time = time.time()

    file = open('accel_over_time.csv', 'a') # name csv after calibration trial and axis
    file.write('time' + ',' + 'x (g)' + ',' + 'y (g)' + ',' + 'z (g)' + '\n') # label each column
    file.close()

    while (time.time() - start_time) < total_time:

        ##############################################
        # Collect accelerometer readings over time
        ##############################################

        x_accel, y_accel, z_accel = get_accel()
        elapsed_time = time.time() - start_time
        
        ###########################
        # Save analyzed data to CSV
        ###########################

        file = open('accel_over_time.csv', 'a') # name csv after calibration trial and axis
        file.write(str(elapsed_time / 60 / 60) + ',' + str(x_accel) + ',' + str(y_accel) + ',' + str(z_accel) + '\n')
        file.close()

    return


def graph_data(times, x_accels, y_accels, z_accels, TITLE, FILENAME):

    fig,axs = plt.subplots(3,1)

    axs[0].scatter(times, x_accels, s=1, color='r')
    axs[1].scatter(times, y_accels, s=1, color='b')
    axs[2].scatter(times, z_accels, s=1, color='g')
    axs[0].set_ylabel('X Accel. [g]')
    axs[1].set_ylabel('Y Accel. [g]')
    axs[2].set_ylabel('Z Accel. [g]')
    axs[2].set_xlabel('Time (hours)')
    #axs.set_ylim([-2,2])
    axs[0].set_title(TITLE)
    fig.savefig(FILENAME)

    return




####################################################################################################################
# MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN #
####################################################################################################################

if __name__ == '__main__':
    #start_bool = True # COMMENT OUT WHEN USING THE IMU
    if not start_bool:
        print("IMU not Started - Check Wiring and I2C")
    else:
        
        time.sleep(60) # sleep for 60 seconds
        print("Starting collection")
        
        ###################################
        # Collect data for a period of time
        ###################################

        accel_cal(total_time=60*60*15) # collect over 15 hours

        file = open("accel_over_time.csv")
        read_data = np.loadtxt(file, skiprows = 1, delimiter=",", dtype=float)
        time_array = read_data[:, 0]
        x_accels = read_data[:, 1]
        y_accels = read_data[:, 2]
        z_accels = read_data[:, 3]

        graph_data(time_array, x_accels, y_accels, z_accels, "Acceleration over Time", "accel_over_time.png")


