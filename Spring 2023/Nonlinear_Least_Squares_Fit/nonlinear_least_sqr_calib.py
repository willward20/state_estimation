"""

This program takes an accelerometer dataset, creates
a curve fit function using cosine (two or four params), 
and then calibrates the ideal function to the ideal
expected data. 

Plots generated from this program: 
    calibrate_2_param_fit.png
    calibrate_4_param_fit.png
    error_in_cal_fits.png
    error_in_cal_real_data.png

y_theory = cosx
y_m = A * cos(Bx - C) + D   (four parameters)
y_n = A * cosx + D          (two parameters)

y_theory = cos ( (1/B) * arccos((y_m - D)/A) ) + C  (four parameters)
y_theory = (y_n - D) / A    (two parameters)

#1 Pull data from CSV
#2 Generate curvefits (use nonlin_lst_sqr_fit.py)
#3 Calibrate and calculate error between real and ideal

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

def cos_arrcos_func(mean_accel, A, B, C, D):
    return np.cos( (1 / B) * np.arccos( (mean_accel - D) / A) + C)

def graph_data(angles, means, curve_fit, ideal_fit, cal_curve_fit, TITLE, FILENAME):

    fig = plt.figure()
    axs = fig.add_subplot(1,1,1)

    plt.scatter(angles, means, color='r', label="Measured Data")
    #plt.plot(angles, curve_fit, color='k', label=f'y = {coeffs[0]:.3f}*cos({coeffs[1]:.3f}$\\theta$ - {coeffs[2]:0.3f}) + {coeffs[3]:.3f}')
    plt.plot(angles, curve_fit, color='k', label='Four Parameter Fit')
    plt.plot(angles, cal_curve_fit, color='m', label='Calibrated Four Parameter Fit')
    plt.plot(angles, ideal_fit, color='b', label="Theoretical Ideal Model") # plot the ideal curve of what accelerometer readings should look like
    #plt.plot(angles, old_linear_calibration, color='m', label='Old Method of Calibration') # old method calibration (just to keep in mind)
    axs.set_ylabel('Acceleration [g]')
    axs.set_xlabel('Angle Relative to Gravity [degrees]')
    plt.yticks([-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1])
    axs.set_title(TITLE)
    axs.legend()
    fig.savefig(FILENAME)

    return


def graph_error(angles, error4, error2, TITLE, FILENAME):

    fig = plt.figure()
    axs = fig.add_subplot(1,1,1)

    plt.plot(angles, error4, color='r', label="Calibrated 4 Param Fit - Ideal")
    plt.plot(angles, error2, color='b', label="Calibrated 2 Param Fit - Ideal")
    axs.set_ylabel('Error [g]')
    axs.set_xlabel('Angle Relative to Gravity [degrees]')
    #plt.yticks([-1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1])
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

    popt4, pcov4 = curve_fit(cos_four_params,  # cosine function w/ FOUR parameters
                       angle_deg,  # measured angles
                       mean_accel,  # measured accelerations
                       p0=(1.0, 1.0, 0.0, 0.09))  # the initial guess for the four parameters
    
    popt2, pcov2 = curve_fit(cos_two_params,  # cosine function w/ TWO parameters
                       angle_deg,  # measured angles
                       mean_accel,  # measured accelerations
                       p0=(1.0, 0.09))  # the initial guess for the two parameters

    print("Standard Deviation of Parameters (4): ", np.sqrt(np.diag(pcov4)))
    print("Standard Deviation of Parameters (2): ", np.sqrt(np.diag(pcov2)))

    A4 = popt4[0]
    B4 = popt4[1]
    C4 = popt4[2]
    D4 = popt4[3]

    A2 = popt2[0]
    D2 = popt2[1]


    ###################################
    # Generate Arrays of Trend Curves
    ###################################

    curve_fit4 = cos_four_params(angle_deg, popt4[0], popt4[1], popt4[2], popt4[3]) # fit curve w/ four parameters
    curve_fit2 = cos_two_params(angle_deg, popt2[0], popt2[1]) # fit curve w/ two parameters
    ideal_cos = cos_four_params(angle_deg, 1.0, 1.0, 0.0, 0.0) # calculates data points for theoretical accel. values


    ###################################
    # Compare error in curve fits
    ###################################

    error_fit_4 = abs(curve_fit4 - mean_accel)
    error_fit_2 = abs(curve_fit2 - mean_accel)

    print("Fit four mean error: ", np.mean(error_fit_4), ". Standard Deviation: ", np.std(error_fit_4))
    print("Fit two  mean error: ", np.mean(error_fit_2), ". Standard Deviation: ", np.std(error_fit_2))


    ###################################
    # Calibrate the trend curves and data
    ###################################

    calib_accel_4 = np.cos((1 / B4) * np.arccos((curve_fit4 - D4) / A4) + C4)
    calib_accel_2 = (curve_fit2 - D2) / A2

    calib_accel_4_real = np.cos((1 / B4) * np.arccos((mean_accel - D4) / A4) + C4)
    calib_accel_2_real = (mean_accel - D2) / A2

    # Graph the data, trend fit, and ideal curve
    #graph_data(angle_deg, mean_accel, curve_fit4, ideal_cos, calib_accel_4, "Calibrating Accelerometer Inclined at Rest: x Axis", "four_param_cal.png")
    #graph_data(angle_deg, mean_accel, curve_fit2, ideal_cos, calib_accel_2, "Calibrating Accelerometer Inclined at Rest: x Axis", "two_param_cal.png")
    
    
    ###################################
    # Compare calibrations
    ###################################
    
    error_four_param = calib_accel_4 - ideal_cos
    error_two_param = calib_accel_2 - ideal_cos
    error_four_param_real = calib_accel_4_real - ideal_cos
    error_two_param_real = calib_accel_2_real - ideal_cos

    #graph_error(angle_deg, error_four_param, error_two_param, "Error Between Calibrated Fit Data and Theory", "error_in_cal_fits.png")
    #graph_error(angle_deg, error_four_param_real, error_two_param_real, "Error Between Calibrated Real Data and Theory", "error_in_cal_real_data.png")

    exit()