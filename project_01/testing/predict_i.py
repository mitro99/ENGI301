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
import adafruit_ssd1306

def wavelet(data, level, wavelet):
    (cA, cD) = pywt.dwt(data, wavelet=wavelet)
    for i in range(1, level):
        (cA, cD) = pywt.dwt(cA, wavelet=wavelet)
    return cA, cD

def predict(gesture):

    starttime=time.perf_counter()

    gesture = np.transpose(gesture)
    for i in range(0, 6):
        gesture[i] = (gesture[i] - minvals[i]) / (maxvals[i] - minvals[i])

    gesture = gesture.flatten()
    print(len(gesture))
    input_data = np.float32(np.resize(gesture, (1, 2100)))
    interpreter.set_tensor(input_details[0]['index'], input_data)
    
    interpreter.invoke()
    
    output_data = interpreter.get_tensor(output_details[0]['index'])
    output_data
    endtime = time.perf_counter()
    #output = predictor(data_input=np.float32(gesturewave))
    print(output_data)
    print(endtime-starttime)

    return output_data



# setup
i2c = busio.I2C(board.SCL_2, board.SDA_2)
print(board.SCL_2, board.SDA_2)

interpreter = tflite.Interpreter(model_path='number_model_full.tflite')

interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print(input_details)

#display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
#display.fill(0)
#display_width = display.width
#display_height = display.height

mpu = adafruit_mpu6050.MPU6050(i2c)
mpu.accelerometer_range = adafruit_mpu6050.Range.RANGE_4_G
mpu.gyro_range = adafruit_mpu6050.GyroRange.RANGE_500_DPS

parameters = pd.read_csv('parameters_full.csv', index_col=0)
print(parameters.iloc[0])


minvals = np.array(parameters.iloc[0], dtype='float32')
maxvals = np.array(parameters.iloc[1], dtype='float32')
print(minvals)





n = 0
gesture = []

while True:
    if sum(np.absolute(mpu.acceleration)) > 20 or n != 0:
        
        if n < 350:
            n += 1
            gesture.append(list(mpu.acceleration + mpu.gyro))
            
        
        elif n == 350:
            prediction = predict(gesture)
            number = np.argmax(prediction)
            print(number)
            if(prediction.max() < 0.5):
                print('fail')
            gesture = []
            n = 0
            
            
        
