"""
Write a new calibration data collection program that 
    (a) takes 1000 acceleration measurements 
    (b) calculates the mean, the standard deviation, and the SDOM
    (c) repeats a and b for many angles using the hinge platform
    (d) repeats a, b, and c for all three axes
    (e) saves all of the means, standard deviations, and SDOMs to a CSV file

Using the new CSV file, graph the experimentally measured gravity (with uncertainty 
bars from the SDOM) versus the theoretical gravity component (with uncertainty bars 
from the protractor). 

Looking at the graph, does a linear fit model still make sense with all the new data 
between -1 g, 0 g, and +1 g? Run linear fit and plot with the data. Does the function 
fall within both uncertainty bars for every point?

Use the coefficients reported from the new calibration to calibrate a new set of data. 
Compare the drift displacement with the old way of calibrating (only using three angles)

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


def accel_fit(x_input,m_x,b):
    #print("x_input: ", x_input)
    #print("m_x: ", m_x)
    #print("b: ", b)
    # takes accelerometer data as input and returns correct acceleration value
    return (m_x*x_input)+b # fit equation for accel calibration


def get_accel():
    ax,ay,az,_,_,_ = mpu6050_conv() # read and convert accel data
    return ax,ay,az

    
def accel_cal(num_angles, cal_size, axis):

    ##############################
    # Collect data for each angle
    ##############################

    angles = []
    mean_data = []
    stdev_data = []
    SDOM_data = []

    for n in range(0, num_angles):

        angle = float(input("-"*8+" Type the angle. "))
        # FIGURE TIHS OUT LATER. YOU WILL NEED TO FACTOR THIS INTO GRAVITY CALCULATIONS
        #angle_uncertainty = float(input("-"*8+" Type the uncertainty in the angle measurement. "))
        
        ##############################################
        # Collect accelerometer readings for the angle
        ##############################################

        angle_data = []
        for m in range(0, cal_size):
            #[mpu6050_conv() for ii in range(0,cal_size)] # clear buffer between readings
            if axis == 'ax':
                collect_data, _, _ = 0, 1, 2 # get_accel()
            elif axis == 'ay':
                _, collect_data, _ = 0, 1, 2 # get_accel()
            elif axis == 'az':
                _, _, collect_data = 0, 1, 2 # get_accel()
            else:
                print("You did not specify correct axis")
                exit()
            angle_data.append(collect_data)

        #################################################
        # Calculate the mean, stdev, and SDOM of the data
        #################################################

        angle_mean = np.mean(np.array(angle_data))
        angle_stdev = np.std(np.array(angle_data))
        angle_SDOM = angle_stdev / cal_size

        #############################################
        # Append data to arrays for CSV and returning
        #############################################

        angles.append(angle) 
        mean_data.append(angle_mean)
        stdev_data.append(angle_stdev) 
        SDOM_data.append(angle_SDOM) 

    ###########################
    # Save analyzed data to CSV
    ###########################

    file = open('calibration_1_'+axis+'.csv', 'a') # name csv after calibration trial and axis
    file.write('angle' + ',' + 'mean' + ',' + 'stdev' + ',' + 'SDOM' + '\n') # label each column
    for i in range(0, num_angles): # for every angle
        file.write(str(angles[i]) + ',' + str(mean_data[i]) + ',' + str(stdev_data[i]) + ',' + str(SDOM_data[i]) + '\n')
    file.close()

    return angles, mean_data, stdev_data, SDOM_data


def calc_grav(angles):
    grav_array = []

    for ii in range(0, len(angles)):
        grav_array.append(math.cos(math.radians(angles[ii]))) # in units of g

    return grav_array


def calc_coef(theory, measured):
    # Use three calibrations (+1g, -1g, 0g) for linear fit
    popts,_ = curve_fit(accel_fit,measured,theory,maxfev=10000)
    coeffs = popts # place slope and intercept in offset array
    print(coeffs)
    return coeffs


####################################################################################################################
# MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN ###### MAIN #
####################################################################################################################

if __name__ == '__main__':
    start_bool = True # REMOVE WHEN USING THE IMU!!!!!!!!!!!!!!!!!!!!!!!!!!
    if not start_bool:
        print("IMU not Started - Check Wiring and I2C")
    else:
        
        ###################################
        # Retrieve data for multiple angles
        ###################################

        number_angles = 3 # how many angles to collect data from
        cal_size = 3 # number of points to use for calibration 
        input("Ready to collect for X? Press Enter.")
        x_angles, x_means, x_stdevs, x_SDOMs = accel_cal(number_angles, cal_size, "ax") # collect mean, stdev, and SDOM for each angle
        input("Ready to collect for Y? Press Enter.")
        y_angles, y_means, y_stdevs, y_SDOMs = accel_cal(number_angles, cal_size, "ay") # collect mean, stdev, and SDOM for each angle
        input("Ready to collect for Z? Press Enter.")
        z_angles, z_means, z_stdevs, z_SDOMs = accel_cal(number_angles, cal_size, "az") # collect mean, stdev, and SDOM for each angle

        #############################################
        # Calculate Theoretical Gravity for each axis
        #############################################

        x_grav_theory = calc_grav(x_angles)
        y_grav_theory = calc_grav(y_angles)
        z_grav_theory = calc_grav(z_angles)

        ###################################
        # Calculate Linear Fit Coefficients
        ###################################

        x_coefficients = calc_coef(x_grav_theory, x_means)
        y_coefficients = calc_coef(y_grav_theory, y_means)
        z_coefficients = calc_coef(z_grav_theory, z_means)

        #####################################################
        # Graph theory vs data with trend line and error bars
        #####################################################


        exit()

        

        print("accel_coeffs: ", accel_coeffs)

        ###################################
        # Record new data 
        ###################################
        
        data = np.array([get_accel() for ii in range(0,cal_size)]) # new values
        
        ###################################
        # Plot with and without offsets
        ###################################
        accel_labels = ['a_x','a_y','a_z'] # gyro labels for plots
        plt.style.use('ggplot')
        fig,axs = plt.subplots(2,1,figsize=(12,9))
        for ii in range(0,3):
            axs[0].plot(data[:,ii],
                        label='${}$, Uncalibrated'.format(accel_labels[ii]))
            axs[1].plot(accel_fit(data[:,ii],*accel_coeffs[ii]),
                        label='${}$, Calibrated'.format(accel_labels[ii]))
        axs[0].legend(fontsize=14);axs[1].legend(fontsize=14)
        axs[0].set_ylabel('$a_{x,y,z}$ [g]',fontsize=18)
        axs[1].set_ylabel('$a_{x,y,z}$ [g]',fontsize=18)
        axs[1].set_xlabel('Sample',fontsize=18)
        axs[0].set_ylim([-2,2]);axs[1].set_ylim([-2,2])
        axs[0].set_title('Accelerometer Calibration Calibration Correction',fontsize=18)
        fig.savefig('accel_calibration_output.png',dpi=300,
                    bbox_inches='tight',facecolor='#FCFCFC')
        fig.show()
