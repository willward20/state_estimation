"""

This program pulls the three csv files from Drift_Tests (Fall 2022)
and calibrates them using coefficients from each calibration trial. 
The purpose is to compare the drift effect between calibrations. 
What's the difference between them? How consistent is it? 

From each CSV file, only take the data from the axis that was 
facing up, for simplicity. 

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
import csv,datetime
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import cumtrapz, trapz
from scipy import signal
import math
#from graph_mean import mean_array

time.sleep(2) # wait for MPU to load and settle
accel_labels = ['a_x','a_y','a_z']

def accel_fit(x_input,m_x,b):
    #print("x_input: ", x_input)
    #print("m_x: ", m_x)
    #print("b: ", b)
    # takes accelerometer data as input and returns correct acceleration value
    return (m_x*x_input)+b # fit equation for accel calibration

def imu_integrator(time_array, data_array):

    ###################################
    # Integrate Data Twice 
    ###################################
    
    cal_velocity = np.append(0.0, cumtrapz(data_array,x=time_array))
    cal_displace = np.append(0.0, cumtrapz(cal_velocity, x=time_array))
    disp_array = cal_displace
    displacement = cal_displace[-1]
    
    return disp_array, displacement
    

def graph_data(time, displacements, SDOMs, TITLE, FILENAME, c):

    fig = plt.figure()
    axs = fig.add_subplot(1,1,1)

    plt.plot(time, displacements)
    axs.set_ylabel('Actual Acceleration [g]')
    axs.set_xlabel('Accelerometer Acceleration [g]')
    #axs.set_ylim([-2,2])
    axs.set_title(TITLE)
    fig.savefig(FILENAME)

    return



if __name__ == '__main__':
    
    ###################################
    # Read data from Drift Tests (Fall 22)
    ###################################

    X_UP_DATA = open("accel_drift_still_x_up.csv")
    x_data = np.loadtxt(X_UP_DATA, skiprows = 1, delimiter=",", dtype=float)
    x_time = x_data[:, 0]
    x_uncal = x_data[:, 1]

    Y_UP_DATA = open("accel_drift_still_y_up.csv")
    y_data = np.loadtxt(Y_UP_DATA, skiprows = 1, delimiter=",", dtype=float)
    y_time = y_data[:, 0]
    y_uncal = y_data[:, 2]

    Z_UP_DATA = open("accel_drift_still_z_up.csv")
    z_data = np.loadtxt(Z_UP_DATA, skiprows = 1, delimiter=",", dtype=float)
    z_time = z_data[:, 0]
    z_uncal = z_data[:, 3]


    ################################################
    # Calibrate data for each cal trial (Fall 2022) 
    ################################################

    # trial coeffs pulled from 

                    # x slope  x int    y slope   y int    z slope  z int
    trial_coeffs = [[1.00020, -0.08992, 0.99967, -0.04474, 0.97684, 0.24150], # Trial 1 -- Acoustics Lab -- Shortdesk
                    [0.99992, -0.09121, 0.99964, -0.04407, 0.97756, 0.23933], # Trial 2 -- Acoustics Lab -- Shortdesk 
                    [1.00021, -0.09062, 0.99978, -0.04364, 0.97665, 0.24077], # Trial 3 -- Acoustics Lab -- Shortdesk
                    [1.00022, -0.08981, 0.99952, -0.04596, 0.97661, 0.24681], # Trial 4 -- Acoustics Lab -- Shortdesk
                    [1.00037, -0.09000, 0.99948, -0.04423, 0.97692, 0.24754], # Trial 5 -- Acoustics Lab -- Shortdesk
                    [1.00010, -0.09090, 0.99971, -0.04484, 0.97698, 0.24225], # Trial 6 -- Acoustics Lab -- Shortdesk
                    [0.99982, -0.09129, 0.99932, -0.04396, 0.97808, 0.23807], # Trial 7 -- Acoustics Lab -- Shortdesk
                    [1.00035, -0.09132, 0.99984, -0.04384, 0.97784, 0.23989], # Trial 8 -- Acoustics Lab -- Shortdesk
                    [0.99970, -0.09320, 0.99955, -0.04356, 0.97746, 0.24419], # Trial 9 -- Acoustics Lab -- Shortdesk
                    [1.00010, -0.09092, 0.99961, -0.04431, 0.97721, 0.24226]] # Average of 9 Trials


    num_cal_trials = 10
    x_disps = []
    y_disps = []
    z_disps = []

    for ii in range(0, num_cal_trials):
        # call calibration function
        x_calib = accel_fit(x_uncal,trial_coeffs[ii][0], trial_coeffs[ii][1])
        y_calib = accel_fit(y_uncal,trial_coeffs[ii][2], trial_coeffs[ii][3])
        z_calib = accel_fit(z_uncal,trial_coeffs[ii][4], trial_coeffs[ii][5])

        print(x_calib)

        ###################################
        # Convert all data from g to m/s/s
        ###################################

        x_calib *= 9.80665 # converts to m/s/s
        y_calib *= 9.80665 # converts to m/s/s
        z_calib *= 9.80665 # converts to m/s/s


        ###################################
        # Remove gravity component from all
        ###################################

        x_calib -= 9.80665 
        y_calib -= 9.80665 
        z_calib -= 9.80665


        ###################################
        # integration over time
        ###################################
        
        x_disp_array, x_displacements = imu_integrator(x_time, x_calib)
        y_disp_array, y_displacements = imu_integrator(y_time, y_calib)
        z_disp_array, z_displacements = imu_integrator(z_time, z_calib)

        x_disps.append(x_displacements)
        y_disps.append(y_displacements)
        z_disps.append(z_displacements)

    ###################################
    # Analyze data
    ###################################

    print("x_displacements: ", x_disps)
    print("y_displacements: ", y_disps)
    print("z_displacements: ", z_disps)

    #plot_displacement(x_time, x_displacements)
    #plot_displacement(y_time, y_displacements)
    #plot_displacement(z_time, z_displacements)