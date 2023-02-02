"""
This program takes the 15 hours data, removes the mean bias, and
integrates to observe the effect of noise.

"""

# wait 5-sec for IMU to connect
import time,sys
sys.path.append('../')
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import cumtrapz, trapz
import math
from scipy.stats import norm


def imu_integrator(time_array, cal_accel):

    ###################################
    # Integrate Data Twice 
    ###################################
    print("integrating now")
    cal_velocity = np.append(0.0, cumtrapz(cal_accel,x=time_array))
    
    #plot_velocity(time_array, [uncal_x_velocity, uncal_y_velocity, uncal_z_velocity], [cal_x_velocity, cal_y_velocity, cal_z_velocity])

    cal_displacement = np.append(0.0, cumtrapz(cal_velocity, x=time_array))
    print("done integrating")
    #i = 0
    #time_filter, vel_filter, dis_filter = [], [], []
    #for ii in range(0, len(time_array)):
    #    if cal_displacement[ii] < 2 and cal_displacement[ii] > -2:
    #        time_filter.append(time_array[ii])
    #        vel_filter.append(cal_velocity[ii])
    #        dis_filter.append(cal_displacement[ii])
    #    else:
    #        break
    
    #print("done filtering")
    return time_array, cal_velocity, cal_displacement


def graph_data(x_times, y_times, z_times, x, y, z, Y_AXIS, TITLE, FILENAME):

    fig = plt.figure()
    axs = fig.add_subplot(1,1,1)

    plt.plot(x_times, x, color='r', label='x')
    plt.plot(y_times, y, color='b', label='y')
    plt.plot(z_times, z, color='g', label='z')
    axs.set_ylabel(Y_AXIS)
    axs.set_xlabel('Time (seconds)')
    #axs.set_ylim([-2,2])
    axs.set_title(TITLE)
    axs.legend()
    fig.savefig(FILENAME)

    return




####################################################################################################################
# MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN #
####################################################################################################################

if __name__ == '__main__':
    
    file = open("accel_over_time.csv")
    read_data = np.loadtxt(file, skiprows = 1, delimiter=",", dtype=float, max_rows=645714) # only load data from one hour
    time_array = read_data[:, 0]
    x_accels = read_data[:, 1]
    y_accels = read_data[:, 2]
    z_accels = read_data[:, 3]
    
    
    # remove mean offset and convert to m/s/s
    x_corrected = (x_accels - np.mean(x_accels)) * 9.80665
    y_corrected = (y_accels - np.mean(y_accels)) * 9.80665
    z_corrected = (z_accels - np.mean(z_accels)) * 9.80665
    
    print(np.mean(x_corrected), " ", np.mean(y_corrected), " ", np.mean(z_corrected))
    
    # convert time to seconds
    time_array = time_array*60*60
    
    x_time, x_vel, x_dis = imu_integrator(time_array, x_corrected) # replace with x_corrected 
    y_time, y_vel, y_dis = imu_integrator(time_array, y_corrected)
    z_time, z_vel, z_dis = imu_integrator(time_array, z_corrected)
    
    x_mean = np.empty(len(time_array))
    x_mean.fill(np.mean(x_corrected))
    y_mean = np.empty(len(time_array))
    y_mean.fill(np.mean(y_corrected))
    z_mean = np.empty(len(time_array))
    z_mean.fill(np.mean(z_corrected))
    
    x_time, x_vel, x_dis_no_noise = imu_integrator(time_array, x_mean) # replace with x_corrected 
    y_time, y_vel, y_dis_no_noise = imu_integrator(time_array, y_mean)
    z_time, z_vel, z_dis_no_noise = imu_integrator(time_array, z_mean)
    
    
    file = open('one_hour_bias_removed.csv', 'a') # name csv after calibration trial and axis
    file.write('Acceleration collected at rest over one hour with mean (DC bias) removed from both data columns. ' +
                'Data integrated for displacement with and without noise.\n')
    file.write('Time (s), With Noise, , , Without Noise\n')
    file.write('        ,   x (m), y (m) , z (m) , x (m), y (m) , z ( m)\n')
    for ii in range(0, len(time_array)):
        file.write(str(time_array[ii]) + ',' + str(x_dis[ii]) + ',' + str(y_dis[ii]) + ',' + str(z_dis[ii]) + ','
                                           + str(x_dis_no_noise[ii]) + ',' + str(y_dis_no_noise[ii]) + ',' + str(z_dis_no_noise[ii]) +'\n')
    file.close()
    
    
    
    #graph_data(x_time, y_time, z_time, x_vel, y_vel, z_vel, "Velocity (m/s)", "Velocity (m/s) - Corrected Constant Accel", "first two min_ideal_mean_vel.png")
    #graph_data(x_time, y_time, z_time, x_dis, y_dis, z_dis, "Displacement (m)", "Displacement (m) - Corrected Constant Accel", "first_two_min_ideal_mean_dis.png")
    
    
    

