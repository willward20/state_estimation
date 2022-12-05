######################################################
#
# This code works out the theoretical model for what
# the acceleration, velocity, and displacement should
# be for a cart traveling down the ramp, from the 
# perspective of the axis facing forward.
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

# A cart with a mass of m  is released from rest at the top of an approximately 1 degree inclined 
# track. The coefficient of kinetic friction between the cart and the track is approximately 0.003 
# (roughly frictionless track). Graph the cart's acceleration, velocity, and position over time. 
# Assume air resistance in negligible. 

# Let the axis of the cart pointing along the track be "para" and the axis pointing to the surface of the track be "perp"

# F_net,perp = Fg_perp - N = m*a_perp = 0    (the cart is stationary along it's vertical axis)
#           m*g*cos(theta) - N  = 0

#           N = F*g*cos(theta)

# F_net,para = Fg_para - F_fric = ma_para
#         m*g*sin(theta) - mu*N = ma_para

############# a_para = a = g*sin(theta) - mu*g*cos(theta) ####################

# Since theta is constant, we know
#       g = 9.80665 m/s/s
#      mu = 0.003 
#   theta = 1 degree


# Therefore, the acceleration in the direction parallel to the track is
mu = 0.003
a = 9.80665 * math.sin(math.radians(1)) - mu*9.80665 * math.cos(math.radians(1)) # m/s/s

def track_theory(data_length):
    total_time = math.sqrt(2*1.96 / a) # total time the cart is in motion
    step = total_time/data_length  # incremental time step size

    # first, create list of times
    time_array = []
    ii = 0
    while ii < total_time:
        time_array.append(ii)
        ii += step

    # for plotting later, create a list of acceleration values (constant)
    a_array = []
    for ii in range(0, len(time_array)):
        a_array.append(a)

    # Next, we use the kinematic equations to solve for a function of velocity
    #     a = 0.142 m/s/s
    #   v_0 = 0 m/s
    #
    #     v = v_0 + a*t_elapsed

    # next create a list of velocities
    v = []
    for ii in range(0, len(time_array)):
        v.append(a*time_array[ii])


    # Next, we use kinematic equations to solve for a function of position
    #   x_0 = 0 m
    #   x - x_0 = v_0 * time_elapsed + 0.5 * a * time_elapsed**2
    #         x = 0.5 * a * time_elapsed**2

    # create a list of displacements
    d = []
    for ii in range(0, len(time_array)):
        #d.append((v[ii] / 2 ) + time_array[ii])
        d.append(0.5 * a * (time_array[ii])**2)

    """
    # Now, call all of the functions and print the size of the results
    print("Time Traveled: ", total_time)
    print("Time Interval: ", step)
    print("Number of Steps: ", len(time_array))
    print("Length of Velocity Array: ", len(v))
    print("Length of Displacement Array: ", len(d))
    print("Final Displacement: ", d[-1], " meters")
    #print("The time to reach 196 cm is: ", math.sqrt(2*1.96/a))


    # Now, plot the functions on a graph 
    plt.style.use('ggplot')
    fig,axs = plt.subplots(3,1,figsize=(12,9))
    axs[0].plot(time_array, a_array, color = 'k')
    axs[1].plot(time_array, v, color = 'k')
    axs[2].plot(time_array, d, color = 'k')
    axs[0].set_ylabel('Acceleration [m/s/s]',fontsize=18)
    axs[1].set_ylabel('Velocity [m/s]',fontsize=18)
    axs[2].set_ylabel('Displacement [m]',fontsize=18)
    axs[2].set_xlabel('Time (seconds)',fontsize=18)
    axs[0].set_ylim([-7.5, 7.5])
    axs[1].set_ylim([0.00,1.5])
    axs[2].set_ylim([0, 5])
    axs[0].set_title("Theoretical Parallel Accel, Vel, and Dis for Cart on Track",fontsize=18)
    fig.savefig('track_theory.png',dpi=300,
                bbox_inches='tight',facecolor='#FCFCFC')
    fig.show()
    """

    return time_array, a_array, v, d

#track_theory(1425)