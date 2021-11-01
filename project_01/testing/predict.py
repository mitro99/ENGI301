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

def wavelet(data, level, wavelet):
    (cA, cD) = pywt.dwt(data, wavelet=wavelet)
    for i in range(1, level):
        (cA, cD) = pywt.dwt(cA, wavelet=wavelet)
    return cA, cD

def predict(gesture):
    gesture = np.array(gesture, dtype='float32')
    starttime=time.perf_counter()

    gesturewave = np.empty((24,48))
    for i in range(0,11,2):
        gesturewavef = wavelet(gesture[0:,int(i/2)], level1, wavetype1)
        gesturewave[i, 0:] = gesturewavef[0]
        gesturewave[i+1, 0:] = gesturewavef[1]
        del gesturewavef
    
    
    for i in range(12,23,2):
        gesturewavef = wavelet(gesture[0:,int(i/2)-6], level2, wavetype2)
        gesturewave[i, 0:] = gesturewavef[0]
        gesturewave[i+1, 0:] = gesturewavef[1]
        del gesturewavef
    
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
    print(endtime-starttime)

    return output_data

operators = {
    "+" : op.add,
    "-" : op.sub,
    "*" : op.mul,
    "/" : op.truediv,
    "^" : op.pow 
}


# setup
i2c = busio.I2C(board.SCL_2, board.SDA_2)
print(board.SCL_2, board.SDA_2)

interpreter = tflite.Interpreter(model_path='number_model.tflite')

interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

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

#Set up accelerometer
mpu = adafruit_mpu6050.MPU6050(i2c)
mpu.accelerometer_range = adafruit_mpu6050.Range.RANGE_4_G
mpu.gyro_range = adafruit_mpu6050.GyroRange.RANGE_500_DPS

parameters = pd.read_csv('dataparameters.csv', index_col=0)

minvals = np.array(parameters.loc['min'], dtype='float32')

maxvals = np.array(parameters.loc['max'], dtype='float32')

level1 = 5
wavetype1 = 'db20'

level2 = 3
wavetype2 = 'rbio2.2'

n = 0
gesture = []

gesture_dict = {0:'0', 1:'1', 2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 9:'9', 10:'cont'}
op_dict = {1:'+', 2:'-', 3:'*', 4:'/', 5:'^'}
cont = False;
complete = False;
eqn = str()
digit = str()


disp.fill(0)
disp.show()

width = disp.width
height = disp.height
image = Image.new("1", (width, height))

draw = ImageDraw.Draw(image)

padding = -2
top = padding
bottom = height - padding
draw.rectangle((0, 0, width, height), outline=0, fill=0)
draw.text((0, top), 'Test', font=font, fill = 255)
disp.image(image)
disp.show()
time.sleep(1)
disp.fill(0)
disp.show()
while True:

    
    if cont == False:
        if sum(np.absolute(mpu.acceleration)) > 20 or n != 0:
            
            if n < 350:
                n += 1
                gesture.append(list(mpu.acceleration + mpu.gyro))
            
            elif n == 350:
                digit = str()
                prediction = predict(gesture)
                print(np.round(prediction, decimals=3))
                number = np.argmax(prediction)

                if(prediction.max() > 0.5):
                    digit = gesture_dict[number]
                    print(digit)
                    eqn = eqn + digit
                    print(eqn)
                    if digit == 'cont':
                        cont = True
                    else:
                        draw.rectangle((0, 0, width, height), outline=0, fill=0)
                        draw.text((0, top), eqn, font=font, fill = 255)
                        disp.image(image)
                        disp.show()
                else:
                    print('fail')
                gesture = []
                n = 0

    elif cont == True and complete == False:
        if sum(np.absolute(mpu.acceleration)) > 20 or n != 0:
            
            if n < 350:
                n += 1
                gesture.append(list(mpu.acceleration + mpu.gyro))
            
            elif n == 350:
                oper = str()
                prediction = predict(gesture)
                print(np.round(prediction, decimals=3))
                number = np.argmax(prediction)

                if(prediction.max() > 0.5):
                    oper = op_dict[number]
                    eqn = eqn + oper
                    print(eqn)
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
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((0, top), eqn, font=font, fill = 255)
        disp.image(image)
        disp.show()
        eqn = str()
        cont = False
        complete = False
        