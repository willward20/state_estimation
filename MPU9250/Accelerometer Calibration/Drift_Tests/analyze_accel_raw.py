"""
This code is used to graph the raw and calibrated data of 
each axis, along with the mean of the calibrated data. This
shows how noisy the data gets. 
"""

import time,sys
sys.path.append('../')
t0 = time.time()
import numpy as np
import csv,datetime
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import cumtrapz, trapz
from scipy import signal
import math

CSVData = open("Drift_Tests/Z_Up_Data/accel_drift_still_z_up.csv")
csv_data = np.loadtxt(CSVData, skiprows = 1, delimiter=",", dtype=float)

time_array = csv_data[:, 0]
raw_accel = csv_data[:, 3]
cal_accel = csv_data[:, 6]

raw_accel *= 9.80665   # converts to m/s/s
cal_accel *= 9.80665   # converts to m/s/s

raw_accel -= 9.80665  
cal_accel -= 9.80665  

raw_std_dev = np.std(raw_accel)
cal_std_dev = np.std(cal_accel)
cal_mean = np.mean(cal_accel)
cal_mean_array = []
for ii in range(0, len(time_array)):
    cal_mean_array.append(cal_mean)

print("raw_std_dev: ", raw_std_dev)
print("cal_std_dev: ", cal_std_dev)

plt.style.use('ggplot')
fig,axs = plt.subplots(2,1,figsize=(12,9))
axs[0].errorbar(time_array, raw_accel, color='r', fmt='o', label='Raw Z Data')
axs[1].errorbar(time_array, cal_accel, color='b', fmt='o', label='Calibrated Z Data')
axs[1].errorbar(time_array, cal_mean_array, color='k', label='Mean = '+str(round(cal_mean, 5)))
axs[0].set_ylabel('Acceleration [m/s/s]',fontsize=18)
axs[1].set_ylabel('Acceleration [m/s/s]',fontsize=18)
axs[1].set_xlabel('Time (seconds)',fontsize=18)
axs[0].legend(fontsize=16, loc='lower right');axs[1].legend(fontsize=16, loc='lower right')
#axs.ticklabel_format(useOffset=False)
axs[0].set_title('Accelerometer Z Up Data (minus gravity)',fontsize=18)
fig.savefig('accel_z_up.png',dpi=300,
            bbox_inches='tight',facecolor='#FCFCFC')
fig.show()