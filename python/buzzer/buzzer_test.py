# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Buzzer Test
--------------------------------------------------------------------------
License:   
Copyright 2021 Erik Welsh

Based on library from

Copyright 2018 Nicholas Lester

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------



"""
import sys

import time
import math
import random

import Adafruit_BBIO.PWM as PWM

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------


# ------------------------------------------------------------------------
# Main Tasks
# ------------------------------------------------------------------------

class BuzzerSound():
    pin       = None
    
    def __init__(self, pin):
        self.pin = pin
    
    # End def
    
    def play_tone(self, frequency, length):
        """Plays a given note for a given length."""
        PWM.start(self.pin, 50, frequency)
        time.sleep(length)
    # end def
    
    def end(self):
        PWM.stop(self.pin)
        PWM.cleanup()
    # End def
    
    
# End class

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    print("Buzzer Test")
    
    buzzer = BuzzerSound("P2_1")
    
    print("Play tone")
    
    buzzer.play_tone(440, 1)        # Play 440Hz for 1 second

    buzzer.end()
    
    print("Test Complete")

