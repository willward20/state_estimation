######################################################
# Copyright (c) 2021 Maker Portal LLC
# Author: Joshua Hrisko
######################################################
#
# This code graphs the calibration coefficients with 
# standard deviation error margins.
#
######################################################
#
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
import csv,datetime
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import cumtrapz, trapz
from scipy import signal
import math

    
###################################
# Create data arrays
###################################
              #x-slope	x-intercept	y-slope	y-intercept	z-slope	z-intercept
october_24 = [[1.00020, -0.0899, 0.99967, -0.0447, 0.9768, 0.2415], #Trial 1
              [0.99992, -0.0912, 0.99964, -0.0441, 0.9776, 0.2393], #Trial 2
              [1.00021, -0.0906, 0.99978, -0.0436, 0.9766, 0.2408]] #Trial 3
october_24_analysis = [[0.00017, 0.0006, 0.00007, 0.0006, 0.0005, 0.0011],    #standard deviations
                       [1.0001, -0.0906, 0.99970, -0.04415, 0.97701, 0.2405], #averages
                       [0.0001, 0.0004, 0.00004, 0.00032, 0.00028, 0.0006]]   #SDOMs

october_27 = [[1.00022, -0.0898, 0.99952, -0.0460, 0.9766, 0.247], #Trial 4
              [1.00037, -0.0900, 0.99948, -0.0442, 0.9769, 0.248], #Trial 5
              [1.00010, -0.0909, 0.99971, -0.0448, 0.9770, 0.242]] #Trial 6
october_27_analysis =[[0.00014, 0.0006, 0.00012, 0.0009, 0.0002, 0.003],      #standard deviations
                      [1.0002, -0.0902, 0.99957, -0.04501, 0.97684, 0.2455],  #averages
                      [0.0001, 0.0003, 0.00007, 0.00051, 0.00011, 0.0017]]    #SDOMS

december_11 = [[0.9998, -0.0913, 0.9993, -0.0440, 0.9781, 0.238], #Trial 7
               [1.0004, -0.0913, 0.9998, -0.0438, 0.9778, 0.240], #Trial 8
               [0.9997, -0.0932, 0.9995, -0.0436, 0.9775, 0.244]] #Trial 9
december_11_analysis = [[0.0003, 0.0011, 0.0003, 0.0002, 0.0003, 0.003],      #standard deviations
               [1.0000, -0.0919, 0.99957, -0.04379, 0.97779, 0.2407],         #averages
               [0.0002, 0.0006, 0.00015, 0.00012, 0.00018, 0.0018]]           #SDOMS

total_analysis = [[0.0002, 0.0010, 0.00016, 0.0008, 0.0005, 0.003],        #total standard deviations
                  [1.00010, -0.0909, 0.99961, -0.0443, 0.97721, 0.2423],   #total averages
                  [0.00008, 0.0003, 0.00005, 0.0003, 0.00018, 0.0011]]	   #total SDOM



x_slope_average = [october_24[0][0], october_24[1][0], october_24[2][0], october_24_analysis[1][0],
                   october_27[0][0], october_27[1][0], october_27[2][0], october_27_analysis[1][0], 
                   december_11[0][0], december_11[1][0], december_11[2][0], december_11_analysis[1][0], 
                   total_analysis[1][0]]
x_slope_errbars = [0, 0, 0, october_24_analysis[2][0], 
                   0, 0, 0, october_27_analysis[2][0], 
                   0, 0, 0, december_11_analysis[2][0], 
                   total_analysis[2][0]]
x_intercept_average = [october_24[0][1], october_24[1][1], october_24[2][1], october_24_analysis[1][1],
                    october_27[0][1], october_27[1][1], october_27[2][1], october_27_analysis[1][1], 
                    december_11[0][1], december_11[1][1], december_11[2][1], december_11_analysis[1][1], 
                    total_analysis[1][1]]
x_intercept_errbars = [0, 0, 0, october_24_analysis[2][1], 
                    0, 0, 0, october_27_analysis[2][1], 
                    0, 0, 0, december_11_analysis[2][1], 
                    total_analysis[2][1]]

#x_labels = ['Oct 24','Oct 27','Dec 11','Total']
x_labels = ['Trial 1', 'Trial 2', 'Trial 3', 'AVG 1-3', 
            'Trial 4', 'Trial 5', 'Trial 6', 'AVG 4-6',
            'Trial 7', 'Trial 8', 'Trial 9 ', 'AVG 7-9',
            'AVG 1-9']



plt.style.use('ggplot')
fig,axs = plt.subplots(2,1,figsize=(12,9))
axs[0].errorbar(range(len(x_labels)), x_slope_average, yerr=x_slope_errbars, color='r', fmt='o')
axs[1].errorbar(range(len(x_labels)), x_intercept_average, yerr=x_intercept_errbars, color = 'r', fmt='o')
axs[0].set_ylabel('X Slope Averages [?]',fontsize=18)
axs[1].set_ylabel('X Intercept Averages [?]',fontsize=18)
axs[1].set_xlabel('Oct 24 (1-3), October 27 (4-6), December 11 (7-9)',fontsize=18)
axs[0].ticklabel_format(useOffset=False)
axs[0].set_title('Accelerometer Calibration X Coefficient Averages',fontsize=18)
plt.setp(axs, xticks=range(len(x_labels)), xticklabels=x_labels)
fig.savefig('accel_cal_x_coeff_avg.png',dpi=300,
            bbox_inches='tight',facecolor='#FCFCFC')
fig.show()