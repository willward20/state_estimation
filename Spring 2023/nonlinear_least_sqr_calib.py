"""

This program takes the 19 points data set and runs a
nonlinear least square regression to find the best cosine
curve fit function. I hope that we can use this model 
function to calibrate the system to what how the cosine
function should ideally behave. 

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
from scipy.integrate import cumtrapz, trapz
import math


def cos_func(angles, A, B, C, D):
    # y = A*cos(B*x - C) + D
    return A * np.cos(B * (angles * math.pi / 180) - C) + D

def cos_arrcos_func(mean_accel, A, B, C, D):
    return np.cos( (1 / B) * np.arccos( (mean_accel - D) / A) + C)


def linear_fit(x_input,m_x,b):
    # takes accelerometer data as input and returns correct acceleration value
    return (m_x*x_input)+b # fit equation for accel calibration


def graph_data(angles, means, coeffs, calib_accel, TITLE, FILENAME):

    curve_fit = cos_func(angles, coeffs[0], coeffs[1], coeffs[2], coeffs[3])
    ideal_cos = cos_func(angles, 1.0, 1.0, 0.0, 0.0)

    fig = plt.figure()
    axs = fig.add_subplot(1,1,1)

    plt.scatter(angles, means, color='r', label="Measured Data")
    #plt.scatter(angles, calib_accel, color='r')
    plt.plot(angles, curve_fit, color='k', label=f'y = {coeffs[0]:.3f}*cos({coeffs[1]:.3f}$\\theta$ - {coeffs[2]:0.3f}) + {coeffs[3]:.3f}')
    #plt.plot(angles, ideal_cos, color='b')
    axs.set_ylabel('Acceleration [g]')
    axs.set_xlabel('Angle Relative to Gravity [degrees]')
    #axs.set_ylim([-2,2])
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

    popt, pcov = curve_fit(cos_func,  # cosine function
                       angle_deg,  # measured angles
                       mean_accel,  # measured accelerations
                       p0=(1.0, 1.0, 0.0, 0.09))  # the initial guess for the four parameters

    print("coeffs: ", popt)
    print("covariance: ", pcov)
    A = popt[0]
    B = popt[1]
    C = popt[2]
    D = popt[3]

    ###################################
    # Calibrate using trend curves
    ###################################

    calib_accel = np.cos((1 / B) * np.arccos((mean_accel - D) / A) + C)

    # Graph the data, trend fit, and ideal curve
    graph_data(angle_deg, mean_accel, popt, calib_accel, "Accelerometer Inclined at Rest: x Axis", "_.png")



    ###################################
    # Compare calibrations
    ###################################
    ideal_cos = cos_func(angle_deg, 1.0, 1.0, 0.0, 0.0) # calculate ideal accel data for each angle

    # calibrate the raw data using the original linear fit method
    popts,_ = curve_fit(linear_fit,mean_accel,ideal_cos)
    #print(popts)
    linear_calib = linear_fit(mean_accel, popts[0], popts[1])

    # calibrate the ideal cosine fit data using the cos/arccos function
    trend_cos_fit = cos_func(angle_deg, A, B, C, D)
    calib_ideal_accel = np.cos((1 / B) * np.arccos((trend_cos_fit - D) / A) + C)

    # calibrate the ideal cosine fit data using the original linear fit method
    popts,_ = curve_fit(linear_fit,trend_cos_fit,ideal_cos)
    linear_calib_ideal_cos = linear_fit(trend_cos_fit, popts[0], popts[1])

    error_uncalb = mean_accel - ideal_cos
    error_linear_fit = linear_calib - ideal_cos
    error_cos_fit = calib_accel - ideal_cos
    error_ideal_cos_fit = calib_ideal_accel - ideal_cos
    error_linear_ideal_cos_fit = linear_calib_ideal_cos - ideal_cos

    fig = plt.figure()
    axs = fig.add_subplot(1,1,1)

    plt.plot(angle_deg, error_uncalb, color='r', label="Error Uncalibrated")
    plt.plot(angle_deg, error_linear_fit, color='b', label="Error Linear Fit Cal")
    plt.plot(angle_deg, error_cos_fit, color='g', label="Error Cos Fit Cal")
    plt.plot(angle_deg, error_ideal_cos_fit, color='m', label="Error Ideal Cos Fit Cal")
    plt.plot(angle_deg, error_linear_ideal_cos_fit, color='k', label="Error Linear Ideal Cos Fit Cal")
    axs.set_ylabel('Error [g]')
    axs.set_xlabel('Angle Relative to Gravity [degrees]')
    #axs.set_ylim([-2,2])
    axs.set_title("Compare Uncalibrated and Calibrated Error")
    axs.legend()
    fig.savefig("compare_calb.png")
