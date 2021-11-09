# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Gesture Calculator
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

This program interprets gestures obtained from an MPU6050 IMU and 
transforms them into numbers and operators, functioning as a calculator.
The results are displayed on a screen in a real time and a vibration motor 
has been incorporated to provide feedback during gesturing.

"""
# ------------------------------------------------------------------------

#Import all necessary modules and functions

import adafruit_mpu6050
import operator as op
import re
import time
import board
import busio
import numpy as np
import pandas as pd
import tflite_runtime.interpreter as tflite
import pywt
import adafruit_ssd1306
import Adafruit_BBIO.PWM as PWM
from PIL import Image, ImageDraw, ImageFont

#define wavelet transform function
def wavelet(data, level, wavelet):
    (cA, cD) = pywt.dwt(data, wavelet=wavelet)
    for i in range(1, level):
        (cA, cD) = pywt.dwt(cA, wavelet=wavelet)
    return cA, cD

#set up prediction function
def predict(gesture):
    gesture = np.array(gesture, dtype='float32')
    starttime=time.perf_counter()

    #Wavelet transforms here are the same as in the jupyter notebook
    #However, they are done with numpy instead of pandas to optimize speed
    
    #Perform first transform
    gesturewave = np.empty((24,48))
    for i in range(0,11,2):
        gesturewavef = wavelet(gesture[0:,int(i/2)], level1, wavetype1)
        gesturewave[i, 0:] = gesturewavef[0]
        gesturewave[i+1, 0:] = gesturewavef[1]
        del gesturewavef
    
    #Perform second transform
    for i in range(12,23,2):
        gesturewavef = wavelet(gesture[0:,int(i/2)-6], level2, wavetype2)
        gesturewave[i, 0:] = gesturewavef[0]
        gesturewave[i+1, 0:] = gesturewavef[1]
        del gesturewavef
    
    #normalize data
    for i in range(0,23):
        gesturewave[i] = (gesturewave[i] - minvals[i]) / (maxvals[i] - minvals[i])
    
    gesturewave = np.transpose(gesturewave).flatten()

    input_data = np.float32(np.resize(gesturewave, (1, 1152)))
    interpreter.set_tensor(input_details[0]['index'], input_data)
    
    interpreter.invoke()
    
    output_data = interpreter.get_tensor(output_details[0]['index'])
    output_data
    endtime = time.perf_counter()

    #print(output_data)
    #print(endtime-starttime)

    return output_data


#Table of operator conversions
operators = {
    "+" : op.add,
    "-" : op.sub,
    "*" : op.mul,
    "/" : op.truediv,
    "^" : op.pow 
}

#Set up TensorFlow inference
interpreter = tflite.Interpreter(model_path='number_model.tflite')

interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

#Prepare parameters for normalization
parameters = pd.read_csv('dataparameters.csv', index_col=0)
minvals = np.array(parameters.loc['min'], dtype='float32')
maxvals = np.array(parameters.loc['max'], dtype='float32')

#Prepare wavelet parameters
level1 = 5
wavetype1 = 'db20'
level2 = 3
wavetype2 = 'rbio2.2'

# ------------------------------------------------------------------------

# Hardware component setup

i2c2 = busio.I2C(board.SCL_2, board.SDA_2)
i2c = busio.I2C(board.SCL, board.SDA)
#print(board.SCL_2, board.SDA_2)

#Set up display
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

disp.fill(0)
disp.show()

width = disp.width
height = disp.height
image = Image.new("1", (width, height))

draw = ImageDraw.Draw(image)

padding = -2
top = padding
bottom = height - padding
x = 0

font = ImageFont.truetype('Oswald-Regular.ttf', 30)

draw.rectangle((0, 0, width, height), outline=0, fill=0)
draw.text((0, top), 'Initializing...', font=font, fill = 255)

disp.image(image)
disp.show()
time.sleep(2)
disp.fill(0)
disp.show()


#Set up accelerometer
mpu = adafruit_mpu6050.MPU6050(i2c2)
mpu.accelerometer_range = adafruit_mpu6050.Range.RANGE_4_G
mpu.gyro_range = adafruit_mpu6050.GyroRange.RANGE_500_DPS


# ------------------------------------------------------------------------
#Main Script

#Set up dictionaries to convert from prediction result to useful information
gesture_dict = {0:'0', 1:'1', 2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 9:'9', 10:'cont'}
op_dict = {1:'+', 2:'-', 3:'*', 4:'/', 5:'^'}

cont = False;
complete = False;
eqn = str()
digit = str()

n = 0
gesture = []

while True:
    
    #Condition for obtaining numbers from inference
    if cont == False:
        if sum(np.absolute(mpu.acceleration)) > 20 or n != 0:
            
            if n < 350:
                n += 1
                gesture.append(list(mpu.acceleration + mpu.gyro))
            
            elif n == 350:
                digit = str()
                prediction = predict(gesture)
                #print(np.round(prediction, decimals=3))
                number = np.argmax(prediction)
                
                #consider a prediction only if confidence level is above 0.5
                if(prediction.max() > 0.5):
                    digit = gesture_dict[number]
                    #print(digit)

                    #print(eqn)
                    if digit == 'cont':
                        cont = True
                    else:
                        eqn = eqn + digit
                        #display on screen
                        draw.rectangle((0, 0, width, height), outline=0, fill=0)
                        draw.text((0, top), eqn, font=font, fill = 255)
                        disp.image(image)
                        disp.show()
                        print(eqn)
                else:
                    print('fail')
                gesture = []
                n = 0
    
    #condition for detecting operation between numbers after
    #first number has been inputted
    elif cont == True and complete == False:
        if sum(np.absolute(mpu.acceleration)) > 20 or n != 0:
            
            if n < 350:
                n += 1
                gesture.append(list(mpu.acceleration + mpu.gyro))
            
            elif n == 350:
                oper = str()
                prediction = predict(gesture)
                #print(np.round(prediction, decimals=3))
                number = np.argmax(prediction)

                #consider a prediction only if confidence level is above 0.5
                if(prediction.max() > 0.5):
                    oper = op_dict[number]
                    eqn = eqn + oper
                    print(eqn)
                    #display on screen
                    draw.rectangle((0, 0, width, height), outline=0, fill=0)
                    draw.text((0, top), eqn, font=font, fill = 255)
                    disp.image(image)
                    disp.show()
                    cont = False
                    complete = True
                else:
                    print('fail')
                gesture = []
                n = 0
    
    #condition to actually perform calculations if
    #both numbers and operator have been inputted
    elif cont == True and complete == True:
        if eqn[0] in op_dict.values():
            eqn = str(result) + eqn[1:]
        
        number1 = int(re.split(r'\W', eqn)[0])
        number2 = int(re.split(r'\W', eqn)[1])
        operator = re.findall(r'\W', eqn)[0]                
        
        function = op.get(operator, None)   
        
        result = function(number1, number2)
        eqn = eqn + '='
        eqn = eqn + str(result)
        print(eqn)
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((0, top), eqn, font=font, fill = 255)
        disp.image(image)
        disp.show()
        
        eqn = str()
        cont = False
        complete = False
        