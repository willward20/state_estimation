import board
import busio
import adafruit_bno055
import time
import matplotlib.pyplot as plt

i2c = busio.I2C(board.SCL, board.SDA) # define board.I2C object
sensor = adafruit_bno055.BNO055_I2C(i2c) # create sensor object

gyro_x = []
gyro_y = []
gyro_z = []
times = []
start_time = time.time()
print(start_time)
#try:
for n in range (0, 500):
    times.append(time.time() - start_time)
    gyro_x.append(sensor.gyro[0])
    gyro_y.append(sensor.gyro[1])
    gyro_z.append(sensor.gyro[2])
    
    time.sleep(0.01)

#except KeyboardInterrupt:
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

# make an xy scatter plot
plt.scatter(times, gyro_x, color='red', label='x')
plt.scatter(times, gyro_y, color='green', label='y')
plt.scatter(times, gyro_z, color='blue', label='z')

plt.ylim(-0.01,0.01)
ax.set_xlabel('Time (seconds)')
ax.set_ylabel('Rotations (unit?)')
ax.set_title('Graphing Gyroscope')
plt.legend(loc = 'upper right')

plt.show()
    
    

