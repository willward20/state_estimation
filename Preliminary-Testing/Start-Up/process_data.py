##################################################################
# Program Name: process_data.py
# Written by: Will Ward 
#  
# Function:
#     1. Extract all of the start-up collect data
#     2. Calcualte the mean and standard deviation of each trial
#     3. Graph the means and standard deviations  
###################################################################



import time,sys
sys.path.append('../')
import numpy as np
import matplotlib.pyplot as plt



def graph_data(x, y, z, x_std, y_std, z_std, TITLE, FILENAME):

    # Graph x, y, and z data on seperate plots.

    fig,axs = plt.subplots(3,1)

    trials = range(60)

    axs[0].errorbar(trials, x, yerr=x_std, color='r')
    axs[1].errorbar(trials, y, yerr=y_std, color='b')
    axs[2].errorbar(trials, z, yerr=z_std, color='g')
    axs[0].set_ylabel('X [g]')
    axs[1].set_ylabel('Y [g]')
    axs[2].set_ylabel('Z [g]')
    axs[2].set_xlabel('Trial Number')
    #axs.set_ylim([-2,2])
    axs[0].set_title(TITLE)
    fig.savefig(FILENAME)

    return






if __name__ == '__main__':
    
    x_means = []
    y_means = []
    z_means = []
    x_std_devs = []
    y_std_devs = []
    z_std_devs = []

    for ii in range (1, 61):
        # Open the CSV file again and graph the data
        file = open('Data/start_up_data_'+str(ii)+'.csv')
        read_data = np.loadtxt(file, skiprows = 1, delimiter=",", dtype=float)
        time_array = read_data[:, 0] # seperate data into arays
        x_accels = read_data[:, 1]
        y_accels = read_data[:, 2]
        z_accels = read_data[:, 3]
        
        x_means.append(np.mean(x_accels))
        y_means.append(np.mean(y_accels))
        z_means.append(np.mean(z_accels))
        x_std_devs.append(np.std(x_accels))
        y_std_devs.append(np.std(y_accels))
        z_std_devs.append(np.std(z_accels))
    
    #for ii in range (0,3):
    print("X mean mean: ", np.mean(x_means))
    print("X mean std_dev: ", np.std(x_means))
    print("Y mean mean: ", np.mean(y_means))
    print("Y mean std_dev: ", np.std(y_means))
    print("Z mean mean: ", np.mean(z_means))
    print("Z mean std_dev: ", np.std(z_means))

    #graph_data(x_means, y_means, z_means, TITLE="Mean (g) of Each One Minute Trial", FILENAME="means_over_trials.png")
    #graph_data(x_std_devs, y_std_devs, z_std_devs, TITLE="Standard Deviations (g) of Each One Minute Trial", FILENAME="std_over_trials.png")


