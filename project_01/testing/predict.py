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

#time.perfcounter()
import adafruit_mpu6050
import time
import board
import busio
import numpy as np
import pandas as pd
import tflite_runtime.interpreter as tflite
import pywt

i2c = busio.I2C(board.SCL_2, board.SDA_2)
print(board.SCL_2, board.SDA_2)

def wavelet(data, level, wavelet):
    (cA, cD) = pywt.dwt(data, wavelet=wavelet)
    for i in range(1, level):
        (cA, cD) = pywt.dwt(cA, wavelet=wavelet)
    return cA, cD

interpreter = tflite.Interpreter(model_path='test_model.tflite')

interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print(input_details)


mpu = adafruit_mpu6050.MPU6050(i2c)
mpu.accelerometer_range = adafruit_mpu6050.Range.RANGE_4_G
mpu.gyro_range = adafruit_mpu6050.GyroRange.RANGE_500_DPS

parameters = pd.read_csv('dataparameters.csv', index_col=0)

minvals = np.array(parameters.loc['min'], dtype='float32')
maxvals = np.array(parameters.loc['max'], dtype='float32')

level1 = 5
wavetype1 = 'dmey'

level2 = 2
wavetype2 = 'rbio2.2'

num = 0
while True:
    if sum(np.absolute(mpu.acceleration)) > 20:
        num += 1
        n = 0    
        gesture = []
        while(n < 250):
            n += 1
            gesture.append(list(mpu.acceleration + mpu.gyro))
            
        gesture = np.array(gesture, dtype='float32')
        starttime=time.perf_counter()

        gesturewave = np.empty((24,66))
        for i in range(0,11,2):
            gesturewavef = wavelet(gesture[0:,int(i/2)], level1, wavetype1)
            gesturewave[i, 0:] = gesturewavef[0]
            gesturewave[i+1, 0:] = gesturewavef[1]
            del gesturewavef
        
        
        for i in range(12,23):
            gesturewavef = wavelet(gesture[0:,int(i/2)-6], level1, wavetype1)
            gesturewave[i, 0:] = gesturewavef[0]
            gesturewave[i+1, 0:] = gesturewavef[1]
            del gesturewavef
        
        endtime = time.perf_counter()
        gesturewave = np.transpose(gesturewave).flatten()
        print(gesturewave)
        
        
        input_data = np.float32(np.resize(gesturewave, (1, 1584)))
        interpreter.set_tensor(input_details[0]['index'], input_data)
        
        interpreter.invoke()
        
        output_data = interpreter.get_tensor(output_details[0]['index'])
        output_data
        #output = predictor(data_input=np.float32(gesturewave))
        #print(output)
        print(endtime-starttime)