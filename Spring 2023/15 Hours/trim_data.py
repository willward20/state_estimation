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
    
    # convert time to seconds
    time_array = time_array*60*60
    

    
    file = open('one_hour_raw_data.csv', 'a') # name csv after calibration trial and axis
    file.write('Acceleration [g] collected at rest over one hour. Mean NOT removed.\n')
    file.write('Time (s), x, y, z\n')
    for ii in range(0, len(time_array)):
        file.write(str(time_array[ii]) + ',' + str(x_accels[ii]) + ',' + str(y_accels[ii]) + ',' + str(z_accels[ii]) + '\n')
    file.close()
    
    
    
    #graph_data(x_time, y_time, z_time, x_vel, y_vel, z_vel, "Velocity (m/s)", "Velocity (m/s) - Corrected Constant Accel", "first two min_ideal_mean_vel.png")
    #graph_data(x_time, y_time, z_time, x_dis, y_dis, z_dis, "Displacement (m)", "Displacement (m) - Corrected Constant Accel", "first_two_min_ideal_mean_dis.png")
    
    
    


