"""

This program takes an accelerometer dataset (where values
are collected at different angles) and runs a
nonlinear least square regression to find the best cosine
curve fit function. 

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


def cos_four_params(angles, A, B, C, D):
    # y = A*cos(B*x - C) + D
    return A * np.cos(B * (angles * math.pi / 180) - C) + D

def cos_two_params(angles, A, D):
    return A * np.cos(angles*math.pi / 180) + D

def linear_fit(x_input,m_x,b):
    # takes accelerometer data as input and returns correct acceleration value
    return (m_x*x_input)+b # fit equation for accel calibration

def graph_data(angles, means, coeffs, TITLE, FILENAME):

    #curve_fit = cos_four_params(angles, coeffs[0], coeffs[1], coeffs[2], coeffs[3]) # fit curve w/ four parameters
    curve_fit = cos_two_params(angles, coeffs[0], coeffs[1]) # fit curve w/ two parameters
    #old_linear_calibration = linear_fit(means, 0.99887002, -0.09019459) # coefficients from accel vs. accel (markersportal)
    ideal_cos = cos_four_params(angles, 1.0, 1.0, 0.0, 0.0) # calculates data points for theoretical accel. values

    fig = plt.figure()
    axs = fig.add_subplot(1,1,1)

    plt.scatter(angles, means, color='r', label="Measured Data")
    #plt.plot(angles, curve_fit, color='k', label=f'y = {coeffs[0]:.3f}*cos({coeffs[1]:.3f}$\\theta$ - {coeffs[2]:0.3f}) + {coeffs[3]:.3f}')
    plt.plot(angles, curve_fit, color='k', label=f'y = {coeffs[0]:.3f}*cos$\\theta$ + {coeffs[1]:.3f}')
    plt.plot(angles, ideal_cos, color='b', label="Theoretical Ideal Model") # plot the ideal curve of what accelerometer readings should look like
    #plt.plot(angles, old_linear_calibration, color='m', label='Old Method of Calibration') # old method calibration (just to keep in mind)
    axs.set_ylabel('Acceleration [g]')
    axs.set_xlabel('Angle Relative to Gravity [degrees]')
    plt.yticks([-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1])
    axs.set_title(TITLE)
    axs.legend()
    fig.savefig(FILENAME)

    return


if __name__ == '__main__':
    
    ###################################
    # Read data from calibrate 19 pts
    ###################################

    CSV = open("calibrate_x_19pts.csv")
    csv_data = np.loadtxt(CSV, skiprows = 1, delimiter=",", dtype=float)
    angle_deg = csv_data[:, 0]
    mean_accel = csv_data[:, 1]

    ###################################
    # Run scipy curve_fit
    ###################################

    #popt, pcov = curve_fit(cos_four_params,  # cosine function w/ FOUR parameters
    #                   angle_deg,  # measured angles
    #                   mean_accel,  # measured accelerations
    #                   p0=(1.0, 1.0, 0.0, 0.09))  # the initial guess for the four parameters
    
    popt, pcov = curve_fit(cos_two_params,  # cosine function w/ TWO parameters
                       angle_deg,  # measured angles
                       mean_accel,  # measured accelerations
                       p0=(1.0, 0.09))  # the initial guess for the two parameters

    print("coeffs: ", popt)
    #print("covariance: ", pcov)

    # Graph the data, trend fit, and ideal curve
    graph_data(angle_deg, mean_accel, popt, "Accelerometer Inclined at Rest: x Axis (Fit with TWO Params)", "_.png")