"""
--------------------------------------------------------------------------
Servo Test
--------------------------------------------------------------------------
License:   
Copyright 2021 Erik Welsh

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

Test SG90 Servo

"""
import time

import Adafruit_BBIO.PWM as PWM

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

SG90_FREQ   = 50                  # 20ms period (50Hz)
SG90_POL    = 0                   # Rising Edge polarity
SG90_OFF    = 5                   # 0ms pulse -- Servo is inactive
SG90_RIGHT  = 5                   # 1ms pulse (5% duty cycle)  -- All the way right
SG90_LEFT   = 10                  # 2ms pulse (10% duty cycle) -- All the way Left


# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

# None

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class Servo():
    """ CombinationLock """
    servo      = None
    
    def __init__(self, servo="P1_36"):
        """ Initialize variables and set up display """
        self.servo      = servo
        
        self._setup()
    
    # End def
    
    
    def _setup(self):
        """Setup the hardware components."""
        # Initialize Servo; Servo should be "off"
        PWM.start(self.servo, SG90_OFF, SG90_FREQ, SG90_POL)

    # End def


    def left(self):
        """Lock the lock:
               - Turn on red LED; Turn off green LED
               - Set servo to closed
        """
        # Set servo
        PWM.set_duty_cycle(self.servo, SG90_LEFT)

    # End def


    def right(self):
        """Unlock the lock.
               - Turn off red LED; Turn on green LED
               - Set servo to open
               - Set display to "----"
        """
        # Set servo
        PWM.set_duty_cycle(self.servo, SG90_RIGHT)

    # End def


    def cleanup(self):
        """Cleanup the hardware components."""
        
        # Stop servo
        PWM.stop(self.servo)
        PWM.cleanup()
        
    # End def

# End class



# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':

    print("Servo Test")

    # Create instantiation of the servo
    servo = Servo()

    try:
        time.sleep(1)
        print("Turn left")
        servo.left()
        time.sleep(1)
        print("Turn right")
        servo.right()
        time.sleep(1)

    except KeyboardInterrupt:
        pass

    # Clean up hardware when exiting
    servo.cleanup()

    print("Test Complete")

