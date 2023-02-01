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
        file.write('time' + ',' + 'x (g)' + ',' + 'y (g)' + ',' + 'z (g)' + '\n') # label each column
        file.write(str(elapsed_time / 60 / 60) + ',' + str(x_accel) + ',' + str(y_accel) + ',' + str(z_accel) + '\n')
        file.close()

    return

def normal_dist(x , mean , sd):
    prob_density = (np.pi*sd) * np.exp(-0.5*((x-mean)/sd)**2)
    return prob_density

def graph_data(times, x_accels, y_accels, z_accels, TITLE, FILENAME):

    fig = plt.figure()
    axs = fig.add_subplot(3,1,1)

    plt[0].plot(times, x_accels, color='r')
    plt[1].plot(times, y_accels, color='b')
    plt[2].plot(times, z_accels, color='g')
    axs[0].set_ylabel('X Accel. [g]')
    axs[1].set_ylabel('Y Accel. [g]')
    axs[2].set_ylabel('Z Accel. [g]')
    axs[2].set_xlabel('Time (hours)')
    #axs.set_ylim([-2,2])
    axs[0].set_title(TITLE)
    fig.savefig(FILENAME)

    return

def graph_prob(x_prob, y_prob, z_prob):

    fig = plt.figure()
    axs = fig.add_subplot(3,1,1)

    plt[0].plot(x_prob, color='r')
    plt[1].plot(y_prob, color='b')
    plt[2].plot(z_prob, color='g')
    axs[0].set_ylabel('X')
    axs[1].set_ylabel('Y')
    axs[2].set_ylabel('Z')
    axs[2].set_xlabel('Data Points')
    #axs.set_ylim([-2,2])
    axs[0].set_title("Probability Density of Data Collected Over 15 Hours")
    fig.savefig("prob_density_15_hrs.png")

    return


####################################################################################################################
# MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN #
####################################################################################################################

if __name__ == '__main__':
    #start_bool = True # COMMENT OUT WHEN USING THE IMU
    if not start_bool:
        print("IMU not Started - Check Wiring and I2C")
    else:
        
        ###################################
        # Collect data for a period of time
        ###################################

        accel_cal(total_time=60) # collect over 15 hours

        file = open("accel_over_time.csv")
        read_data = np.loadtxt(file, skiprows = 1, delimiter=",", dtype=float)
        time_array = read_data[:, 0]
        x_accels = read_data[:, 1]
        y_accels = read_data[:, 2]
        z_accels = read_data[:, 3]

        graph_data(time_array, x_accels, y_accels, z_accels, "Acceleration over Time", "accel_over_time.png")

        # calculate means
        x_mean = np.mean(x_accels)
        y_mean = np.mean(y_accels)
        z_mean = np.mean(z_accels)

        # calcualte standard deviations
        x_sd = np.std(x_accels)
        y_sd = np.std(y_accels)
        z_sd = np.std(z_accels)

        # Calcualte probability densitis
        x_prob_density = normal_dist(x_accels, x_mean, x_sd)
        y_prob_density = normal_dist(y_accels, y_mean, y_sd)
        z_prob_density = normal_dist(z_accels, z_mean, z_sd)

        # graph prob densities
        graph_prob(x_prob_density, y_prob_density, z_prob_density)