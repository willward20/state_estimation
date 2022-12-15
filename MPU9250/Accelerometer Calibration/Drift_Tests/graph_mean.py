######################################################
#
# This code graphs the displacement over time of the 
# mean of the accleration from the Drift Tests. The goal
# is to see how much the displacement changes if noise 
# is removed. This might help me understand what has a 
# bigger impact on drift: bad mean or noisy data?
#
######################################################
#
# wait 5-sec for IMU to connect
import time,sys
sys.path.append('../')
t0 = time.time()
start_bool = False # if IMU start fails - stop calibration
import numpy as np
import csv,datetime
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import cumtrapz, trapz
from scipy import signal
import math



def mean_array(time_array, mean_x, mean_y, mean_z):
    total_time = len(time_array) # total time the cart is in motion

    # for plotting later, create a list of acceleration values (constant)
    ax_array = []
    for ii in range(0, total_time):
        ax_array.append(mean_x)
    ay_array = []
    for ii in range(0, total_time):
        ay_array.append(mean_y)
    az_array = []
    for ii in range(0, total_time):
        az_array.append(mean_z)

    cal_x_velocity = np.append(0.0, cumtrapz(ax_array,x=time_array))
    cal_y_velocity = np.append(0.0, cumtrapz(ay_array,x=time_array))
    cal_z_velocity = np.append(0.0, cumtrapz(az_array,x=time_array))

    cal_x_displacement = np.append(0.0, cumtrapz(cal_x_velocity, x=time_array))
    cal_y_displacement = np.append(0.0, cumtrapz(cal_y_velocity, x=time_array))
    cal_z_displacement = np.append(0.0, cumtrapz(cal_z_velocity, x=time_array))

    return cal_x_displacement, cal_y_displacement, cal_z_displacement

