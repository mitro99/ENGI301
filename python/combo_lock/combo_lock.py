
"""
--------------------------------------------------------------------------
Combination Lock
--------------------------------------------------------------------------
License:   
Copyright 2020 <NAME>

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

Use the following hardware components to make a programmable combination lock:  
  - HT16K33 Display
  - Button
  - Red LED
  - Green LED
  - Potentiometer (analog input)
  - Servo

Requirements:
  - Hardware:
    - When locked:   Red LED is on; Green LED is off; Servo is "closed"; Display is unchanged
    - When unlocked: Red LED is off; Green LED is on; Servo is "open"; Display is "----"
    - Display shows value of potentiometer (raw value of analog input divided by 8)
    - Button
      - Waiting for a button press should allow the display to update (if necessary) and return any values
      - Time the button was pressed should be recorded and returned
    - User interaction:
      - Needs to be able to program the combination for the “lock”
        - Need to be able to input three values for the combination to program or unlock the “lock”
      - Combination lock should lock when done programming and wait for combination input
      - If combination is unsuccessful, the lock should go back to waiting for combination input
      - If combination was successful, the lock should unlock
        - When unlocked, pressing button for less than 2s will re-lock the lock; greater than 2s will allow lock to be re-programmed

Uses:
  - HT16K33 display library developed in class
    - Library updated to add "set_digit_raw()", "set_colon()"

"""
import time

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.PWM as PWM

import ht16k33 as HT16K33
import buzzer_music

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

SG90_FREQ   = 50                  # 20ms period (50Hz)
SG90_POL    = 0                   # Rising Edge polarity
SG90_CLOSE  = 5                   # 1ms pulse (5% duty cycle)  -- All the way right
SG90_OPEN   = 10                  # 2ms pulse (10% duty cycle) -- All the way Left

SG90_OFF    = SG90_CLOSE          # Set the "off" state to "closed"


# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------

# None

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

class CombinationLock():
    """ CombinationLock """
    reset_time = None
    button     = None
    red_led    = None
    green_led  = None
    analog_in  = None
    servo      = None
    display    = None
    music      = None
    
    def __init__(self, reset_time=2.0, button="P2_2", 
                       red_led="P2_6", green_led="P2_4",
                       analog_in="P1_19", servo="P1_36", 
                       i2c_bus=1, i2c_address=0x70, buzzer = "P2_1"):
        """ Initialize variables and set up display """
        self.reset_time = reset_time
        self.button     = button
        self.red_led    = red_led
        self.green_led  = green_led
        self.analog_in  = analog_in
        self.servo      = servo
        self.display    = HT16K33.HT16K33(i2c_bus, i2c_address)
        self.music      = buzzer_music.BuzzerMusic(buzzer)
        self._setup()
    
    # End def
    
    
    def _setup(self):
        """Setup the hardware components."""

        # Initialize Display
        self.set_display_dash()

        # Initialize Button
        GPIO.setup(self.button, GPIO.IN)
        
        # Initialize LEDs
        GPIO.setup(self.red_led, GPIO.OUT)
        GPIO.setup(self.green_led, GPIO.OUT)
        
        # Initialize Analog Input
        ADC.setup()
        
        # Initialize Servo; Servo should be "off"
        PWM.start(self.servo, SG90_OFF, SG90_FREQ, SG90_POL)

    # End def


    def lock(self):
        """Lock the lock:
               - Turn on red LED; Turn off green LED
               - Set servo to closed
        """
        # Set LEDs
        GPIO.output(self.red_led, GPIO.HIGH)
        GPIO.output(self.green_led, GPIO.LOW)

        # Set servo
        PWM.set_duty_cycle(self.servo, SG90_CLOSE)

    # End def


    def unlock(self):
        """Unlock the lock.
               - Turn off red LED; Turn on green LED
               - Set servo to open
               - Set display to "----"
        """
        pass    # REMOVE
        
        # Set LEDs
        GPIO.output(self.red_led, GPIO.LOW)
        GPIO.output(self.green_led, GPIO.HIGH)
        

        # Set servo
        PWM.set_duty_cycle(self.servo, SG90_CLOSE)
        
        #Play tone
        self.music.zelda_secret()
        
        # Set display to dash
        self.set_display_dash()
        
    # End def


    def show_analog_value(self):
        """Show the analog value on the screen:
               - Read raw analog value
               - Divide by 8 (remove two LSBs)
               - Display value
               - Return value
        """
        
        # Read raw value from ADC
        value = ADC.read_raw(self.analog_in)
        
        # Divide value by 8
        
        value = value // 8
        
        # Update display (must be an integer)
        self.display.update(int(value))
        
        
        # Return value
        return value

    # End def


    def button_press(self, function=None):
        """Button press
               - Optional function to execute while waiting for the button to be pressed
                 - Returns the last value of the function when the button was pressed
               - Waits for a full button press
               - Returns the time the button was pressed as tuple
        """
        button_press_time            = 0.0                 # Time button was pressed (in seconds)
        ret_val                      = None                # Optional return value for provided function

        # Optinally execute function pointer that is provided
        #   - This is so that function is run at least once in case of a quick button press
        if function is not None:
            ret_val = function()
        
        
        # Wait for button press
        while(GPIO.input(self.button) == 1):
            # Optinally execute function pointer that is provided
            if function is not None:
                ret_val = function()


            # Sleep for a short period of time to reduce CPU load
            time.sleep(0.1)

        # Record time
        button_press_time = time.time()

        # Wait for button release
        while(GPIO.input(self.button) == 0):
            # Sleep for a short period of time to reduce CPU load
            time.sleep(0.1)

        # Compute button press time
        button_press_time = time.time() - button_press_time

        # Return button press time and optionally ret_val
        if function is not None:
            return (button_press_time, ret_val)
        else:
            return (button_press_time)

    # End def

        
    def input_combination(self):
        """Input a combination for the lock:
               - Wait for a button press doing nothing (start of user inputing combination)
               - Repeat 3 time:
                 - Wait for button press; show analog value
                 - Record analog value
               - Return combination
        """
        # Initialize combination array
        combination = [None, None, None]

        # Wait for button press (do nothing)

        time.sleep(1)
        
        for i in range(3):
            # Update display with current input
            self.set_display_input(i + 1)
            # Wait for button press while showing analog value
            value = None

            # Wait for button press (show analog value)
            (button_press_time, value) = self.button_press(function=self.show_analog_value)
            # Record Analog value
            combination[i] = value

        # print(combination)                       # For debug only
        return combination

    # End def


    def run(self):
        """Execute the main program."""
        combination                  = [None, None, None]  # Combination
        combo_attempt                = [None, None, None]  # Combination attempt
        program                      = True
        
        # Unlock the lock

        while(1):
            
            # Program the lock
            if (program):
                

                # Set display
                self.set_display_prog()
                # Get combination
                combination = self.input_combination()
                # Lock the lock
                self.lock()
                # Set program lock to False
                program = False
            # Set Display to try combination
            self.set_display_try
            # Get combination
            combo_attempt = self.input_combination()
            # Compare attempt against combination
            combo_pass = True
            
            for i in range(3):
                if combination[i] != combo_attempt[i]:
                    combo_pass = False

            # If combination passed
            if combo_pass:
                print('Pass')

                # Unlock the lock
                self.unlock()
                # Wait for button press
                self.button_press_time = self.button_press()
                # If greater than reset_time, program lock, else lock the lock
                if button_press_time > self.reset_time:
                    program = True
    # End def


    def set_display_prog(self):
        """Set display to word "Prog" """
        self.display.text("Prog")

    # End def


    def set_display_try(self):
        """Set display to word " go " """
        self.display.text(" go ")

    # End def


    def set_display_input(self, number):
        """Set display to word "in: #" """
        self.display.text("in {0}".format(number))
        self.display.set_colon(True)

        time.sleep(1)
        
        self.display.set_colon(False)

    # End def


    def set_display_dash(self):
        """Set display to word "----" """
        self.display.text("----")

    # End def


    def cleanup(self):
        """Cleanup the hardware components."""
        
        # Set Display to something fun to show program is complete
        self.display.text("DEAD")
        self.display.set_colon(False)

        # Clean up GPIOs
        GPIO.output(self.red_led, GPIO.LOW)
        GPIO.output(self.green_led, GPIO.LOW)

        # Clean up GPIOs
        GPIO.cleanup()

        # Stop servo
        PWM.stop(self.servo)
        PWM.cleanup()
        
    # End def

# End class



# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':

    print("Program Start")

    # Create instantiation of the lock
    combo_lock = CombinationLock()

    try:
        # Run the people counter
        combo_lock.run()

    except KeyboardInterrupt:
        # Clean up hardware when exiting
        combo_lock.cleanup()

    print("Program Complete")

