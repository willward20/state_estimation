##################################################################
# 
# Program Name: one_hour_integrate.py
# Written by: Will Ward
#  
# Function:
#     1. Load raw acceleration data from CSV file
#     2. Process the data (calibrate, convert, etc.)
#     3. Integrate the data over time (for velocity and/or distance) 
#     4. Plot the integrated data on a graph
#     5. Save integrated data to a CSV file 
# 
###################################################################


import sys
sys.path.append('../')
import numpy as np  
import matplotlib.pyplot as plt 
from scipy.integrate import cumtrapz    


def integrate_data(times, acceleration):

    ###################################
    # Integrate data twice over time
    ###################################

    print("Integrating Acceleration")   # status update
    velocity = np.append(0.0, cumtrapz(acceleration,x=times))   # outputs an array of velocity values over time

    print("Integrating Velocity")   # status update
    displacement = np.append(0.0, cumtrapz(velocity, x=times))  # outputs an array of displacement values over time
    
    print("Finished Integrating")   # status update


    #################################################################################################
    # If needed, filter the data to only keep data until the displacement drifts past a certain point.
    #################################################################################################
    
    #threshold = 2   # maximum acceptable displacement (meters)
    #time_filter, vel_filter, dis_filter = [], [], []    # empty lists to hold truncated data
    #print("Filtering data beyond displacement threshold = ", threshold, " m")  # status update

    #for ii in range(0, len(time_array)):                                        # Loop over the entire data set.
    #    if displacement[ii] < threshold and displacement[ii] > -1*threshold:    # If displacement is within threshold
    #        time_filter.append(times[ii])                                       # keep the time, vel, and disp values
    #        vel_filter.append(velocity[ii])                                  
    #        dis_filter.append(displacement[ii])    
    #    else:   
    #        return time_filter, vel_filter, dis_filter  # once displacement crosses the threshold, stop saving data
    
    return time_array, velocity, displacement



def graph_data(x_times, y_times, z_times, x, y, z, Y_AXIS, TITLE, FILENAME):   
    
    # Graph x, y, and z data on one plot. Each axis gets its own time value, in case data was filtered

    fig = plt.figure()
    axs = fig.add_subplot(1,1,1)

    plt.plot(x_times, x, color='r', label='x')
    plt.plot(y_times, y, color='b', label='y')
    plt.plot(z_times, z, color='g', label='z')
    axs.set_ylabel(Y_AXIS)
    axs.set_xlabel('Time (seconds)')
    #axs.set_ylim([#, #])
    axs.set_title(TITLE)
    axs.legend()
    fig.savefig(FILENAME)

    return





if __name__ == '__main__':
    

    ################################
    # Read and process the raw data
    ################################

    # Read data from CSV file
    file = open("one_hour_raw_data.csv") # containts raw acceleration data collected 179 Hz over one hour (stationarys)
    read_data = np.loadtxt(file, skiprows = 2, delimiter=",", dtype=float) 
        # to only load data over a certain time interval, include the parameter --> max_rows=179*NUM_SEC*NUM_MIN
    
    # Divide data into seperate arrays
    time_array = read_data[:, 0]
    x_accels = read_data[:, 1]
    y_accels = read_data[:, 2]
    z_accels = read_data[:, 3]

    # If using a different CSV file, convert time to seconds, if it's not already in seconds
    # time_array = time_array*60*60
    

    # DATASET 1: Convert from units of g to m/s/s
    x_accels = x_accels * 9.80665
    y_accels = y_accels * 9.80665
    z_accels = z_accels * 9.80665


    # DATASET 2: Remove offset using the mean of each axis
    x_corrected = x_accels - np.mean(x_accels)
    y_corrected = y_accels - np.mean(y_accels)
    z_corrected = z_accels - np.mean(z_accels)
    # Print the mean of the data with bias removed (should be very close to zero)
    #print("Means: ", np.mean(x_corrected), " ", np.mean(y_corrected), " ", np.mean(z_corrected))
    

    # DATASET 3: Remove all noise -- Create a dataset where every value is the mean 
    x_no_noise = np.empty(len(time_array))
    x_no_noise.fill(np.mean(x_corrected))
    y_no_noise = np.empty(len(time_array))
    y_no_noise.fill(np.mean(y_corrected))
    z_no_noise = np.empty(len(time_array))
    z_no_noise.fill(np.mean(z_corrected))
    


    ##################################
    # Integrate and Graph Each Dataset
    ##################################

    # DATASET 1 - integrate
    x_time, x_vel, x_dis = integrate_data(time_array, x_accels)
    y_time, y_vel, y_dis = integrate_data(time_array, y_accels)
    z_time, z_vel, z_dis = integrate_data(time_array, z_accels)
    
    # DATASET 1 - graph displacement
    y_axis_label = "Displacement (m)"
    title = "Displacement (m) - Raw Accel Data"
    image_file_name = "one_hour_raw_dis.png"
    graph_data(x_time, y_time, z_time, x_dis, y_dis, z_dis, Y_AXIS=y_axis_label, TITLE=title, FILENAME=image_file_name)
    
    ###############################################################################################################
    
    # DATASET 2 - integrate
    x_time, x_vel_cor, x_dis_cor = integrate_data(time_array, x_corrected)
    y_time, y_vel_cor, y_dis_cor = integrate_data(time_array, y_corrected)
    z_time, z_vel_cor, z_dis_cor = integrate_data(time_array, z_corrected)

    # DATASET 2 - graph displacement
    y_axis_label = "Displacement (m)"
    title = "Displacement (m) - Bias Corrected Accel Data"
    image_file_name = "one_hour_corrected_dis.png"
    graph_data(x_time, y_time, z_time, x_dis_cor, y_dis_cor, z_dis_cor, Y_AXIS=y_axis_label, TITLE=title, FILENAME=image_file_name)

    ###############################################################################################################

    # DATASET 3 - integrate
    x_time, x_vel_no_noise, x_dis_no_noise = integrate_data(time_array, x_no_noise)
    y_time, y_vel_no_noise, y_dis_no_noise = integrate_data(time_array, y_no_noise)
    z_time, z_vel_no_noise, z_dis_no_noise = integrate_data(time_array, z_no_noise)

    # DATASET 3 - graph displacement
    y_axis_label = "Displacement (m)"
    title = "Displacement (m) - Bias and Noise Corrected Accel Data"
    image_file_name = "one_hour_no_noise_dis.png"
    graph_data(x_time, y_time, z_time, x_dis_no_noise, y_dis_no_noise, z_dis_no_noise, Y_AXIS=y_axis_label, TITLE=title, FILENAME=image_file_name)
    
    

    ######################################################################################################
    # Save to CSV File (ONLY if no filtering occured, otherwise time arrays will not be the same size)
    ######################################################################################################

    file = open('one_hour_displacement.csv', 'a') # name csv after calibration trial and axis
    file.write('Integrated acceleration collected at rest over one hour.\n')
    file.write('Time (s), Raw Displacement (m), , , , Bias Corrected Displacement (m), , , , Bias and Noise Corrected Displacement (m)')
    file.write('        ,          x, y, z, ,                 x, y, z, ,                                 x, y, z\n')
    for ii in range(0, len(time_array)):
        file.write(str(time_array[ii]) + ',' + str(x_dis[ii]) + ',' + str(y_dis[ii]) + ',' + str(z_dis[ii]) + ','
                                 + str(x_dis_cor[ii]) + ',' + str(y_dis_cor[ii]) + ',' + str(z_dis_cor[ii]) + ','
                  + str(x_dis_no_noise[ii]) + ',' + str(y_dis_no_noise[ii]) + ',' + str(z_dis_no_noise[ii]) + '\n')
    file.close()
    
    
    
    

