import board
import busio
import adafruit_bno055
import time

i2c = busio.I2C(board.SCL, board.SDA) # define board.I2C object
sensor = adafruit_bno055.BNO055_I2C(i2c) # create sensor object
"""
def temperature():
    global last_val
    result = sensor.temperature
    if abs(result - last_val) == 128:
        result = sensor.temperature
        if abs(result - last_val) == 128:
            return 0b00111111 & result
    last_val = result
    return result
"""
while True:
    #print("temperature: ", sensor.temperature)
    print("acceleration: ", sensor.acceleration)
    print("magnetic: ", sensor.magnetic)
    print("gyro: ", sensor.gyro)
    #print("euler: ", sensor.euler)
    #print("quaternion: ", sensor.quaternion)
    #print("linear_acceleration: ", sensor.linear_acceleration)
    #print("gravity: ", sensor.gravity)
    print("")
    time.sleep(1)
