# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Simple LED Blink
--------------------------------------------------------------------------
License:   
Copyright 2021 Andrei Mitrofan

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, 
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Simple program that will blink the USR3 LED on the PocketBeagle at 5 Hz

"""

import adafruit_mpu6050
import time
import board
import busio
import numpy as np
import pandas as pd

#Set up IMU
i2c = busio.I2C(board.SCL_2, board.SDA_2)
print(board.SCL_2, board.SDA_2)

mpu = adafruit_mpu6050.MPU6050(i2c)
mpu.accelerometer_range = adafruit_mpu6050.Range.RANGE_4_G
mpu.gyro_range = adafruit_mpu6050.GyroRange.RANGE_500_DPS

# -------------------------------------------------------------------------
# Main Script

#what gesture is being recorded
gesture_num = 0
num = 0
while True:
    gesture = []
    n = 0
    
    #define threshold for identifying a gesture
    if (sum(np.absolute(mpu.acceleration)) > 20)):
        
        #number of samples fixed for consistency
        while n < 350:
            n += 1
            gesture.append(list(mpu.acceleration + mpu.gyro))
        
        #create dataframe for the gesture and save as csv
        data = pd.DataFrame(gesture, columns = ['aX','aY','aZ','gX','gY','gZ'])
        data.to_csv('hand/hand_{0}_{1}'.format(gesture_num, num), index = False)
        
        num += 1
        