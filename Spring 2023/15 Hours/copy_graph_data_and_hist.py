"""
This program collects data from the MPU-9250 accelerometer.

"""

# wait 5-sec for IMU to connect
import time,sys
sys.path.append('../')
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import math
from scipy.stats import norm



def normal_dist(x , mean , sd):
    prob_density = (1 / (sd*(2*np.pi)**0.5)) * np.exp(-0.5*((x-mean)/sd)**2)
    return prob_density

def graph_data(times, accels, TITLE, FILENAME, c):

    fig = plt.figure()
    axs = fig.add_subplot(1,1,1)

    plt.scatter(times, accels, s=1, color=c)
    axs.set_ylabel('Acceleration [g]')
    axs.set_xlabel('Time (hours)')
    #axs.set_ylim([-2,2])
    axs.set_title(TITLE)
    fig.savefig(FILENAME)

    return

def graph_hist(accels, c, TITLE, FILENAME):

    fig = plt.figure()
    axs = fig.add_subplot(1,1,1)
    
    plt.hist(accels, bins = 10000, density = True, alpha=0.6, color=c) 
    plt.title(TITLE)

    #axs.set_ylabel('')
    axs.set_xlabel('Acceleration [g]')
    fig.savefig(FILENAME)

    return


####################################################################################################################
# MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN #
####################################################################################################################

if __name__ == '__main__':
    
    file = open("accel_over_time.csv")
    read_data = np.loadtxt(file, skiprows = 1, delimiter=",", dtype=float)
    time_array = read_data[:, 0]
    x_accels = read_data[:, 1]
    y_accels = read_data[:, 2]
    z_accels = read_data[:, 3]
    
    #print("Total Time (hours): ", time_array[-1])
    #print("Frequency (Hz): ", len(x_accels)/(time_array[-1]*60*60))

    #graph_data(time_array, x_accels, "Acceleration over 15 Hours (x-axis)", "x_axis_15_hrs.png", 'r')
    #graph_data(time_array, y_accels, "Acceleration over 15 Hours (y-axis)", "y_axis_15_hrs.png", 'b')
    #graph_data(time_array, z_accels, "Acceleration over 15 Hours (z-axis)", "z_axis_15_hrs.png", 'g')
    
    
    # calculate means
    x_mean = np.mean(x_accels)
    y_mean = np.mean(y_accels)
    z_mean = np.mean(z_accels)
    #print("Means: ", x_mean, " ", y_mean, " ", z_mean)

    # calcualte standard deviations
    x_sd = np.std(x_accels)
    y_sd = np.std(y_accels)
    z_sd = np.std(z_accels)
    #print("Std Devs: ", x_sd, " ", y_sd, " ", z_sd)
    
    #graph histograms because normal distribution curve does not fit well
    graph_hist(x_accels, 'r', "Acceleration Histogram X-Axis: mean = %.4f, std = %.4f" % (x_mean, x_sd), "x_prob_15_hrs.png") # 200 bins for x
    graph_hist(y_accels, 'b', "Acceleration Histogram Y-Axis: mean = %.4f, std = %.4f" % (y_mean, y_sd), "y_prob_15_hrs.png") # 300 bins
    graph_hist(z_accels, 'g', "Acceleration Histogram Z-Axis: mean = %.4f, std = %.4f" % (z_mean, z_sd), "z_prob_15_hrs.png") # 300 bins
    
    
