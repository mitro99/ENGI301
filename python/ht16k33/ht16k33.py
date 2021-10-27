# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
HT16K33 I2C Library
--------------------------------------------------------------------------
License:   
Copyright 2018-2021 Erik Welsh

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
Software API:

  HT16K33(bus, address=0x70)
    - Provide i2c bus that dispaly is on
    - Provide i2c address for the display
    
    clear()
      - Sets value of display to "0000"
    
    blank()
      - Turns off all LEDs on display
    
    set_colon(enable)
      - Turns on / off the colon on the display.  Enable must be True/False.
    
    update(value)
      - Update the value on the display.  Value must be between 0 and 9999.

    text(value)
      - Update the value on the display with text.
        The following characters are supported:
            "abcdefghijlnopqrstuyABCDEFGHIJLNOPQRSTUY? -"
  
--------------------------------------------------------------------------
Background Information: 
 
  * Using seven-segment digit LED display for Adafruit's HT16K33 I2C backpack:
    * http://adafruit.com/products/878
    * https://learn.adafruit.com/assets/36420
    * https://cdn-shop.adafruit.com/datasheets/ht16K33v110.pdf
    
    * Base code (adapted below):
        * https://github.com/emcconville/HT16K33/blob/master/FourDigit.py
        * https://github.com/emcconville/HT16K33/blob/master/_HT16K33.py
        * https://github.com/adafruit/Adafruit_Python_LED_Backpack/blob/master/Adafruit_LED_Backpack/HT16K33.py
        * https://github.com/adafruit/Adafruit_Python_LED_Backpack/blob/master/Adafruit_LED_Backpack/SevenSegment.py
        * https://github.com/adafruit/Adafruit_Python_LED_Backpack/blob/master/examples/sevensegment_test.py

    * Letters Supported from:
        * https://en.wikichip.org/wiki/seven-segment_display/representing_letters
        
"""
import os


# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

# See https://en.wikipedia.org/wiki/Seven-segment_display for reference 

HEX_DIGITS                  = [0x3f, 0x06, 0x5b, 0x4f,     # 0, 1, 2, 3
                               0x66, 0x6d, 0x7d, 0x07,     # 4, 5, 6, 7
                               0x7f, 0x6f, 0x77, 0x7c,     # 8, 9, A, b
                               0x39, 0x5e, 0x79, 0x71]     # C, d, E, F

LETTERS                     = { "a" : 0x77, "A" : 0x77,    # "A"
                                "b" : 0x7c, "B" : 0x7c,    # "b"
                                "c" : 0x58, "C" : 0x39,    # "c", "C"
                                "d" : 0x5e, "D" : 0x5e,    # "d"
                                "e" : 0x79, "E" : 0x79,    # "E"
                                "f" : 0x71, "F" : 0x71,    # "F"
                                "g" : 0x6F, "G" : 0x6F,    # "g"
                                "h" : 0x74, "H" : 0x76,    # "h", "H"
                                "i" : 0x04, "I" : 0x30,    # "i", "I"
                                "j" : 0x0e, "J" : 0x0e,    # "J"
# Cannot be implemented         "k" : None, "K" : None,    
                                "l" : 0x38, "L" : 0x38,    # "L"
# Cannot be implemented         "m" : None, "M" : None,    
                                "n" : 0x54, "N" : 0x54,    # "n"
                                "o" : 0x5c, "O" : 0x3f,    # "o", "O"
                                "p" : 0x73, "P" : 0x73,    # "P"
                                "q" : 0x67, "Q" : 0x67,    # "q"
                                "r" : 0x50, "R" : 0x50,    # "r"
                                "s" : 0x6D, "S" : 0x6D,    # "S"
                                "t" : 0x78, "T" : 0x78,    # "t"
                                "u" : 0x1c, "U" : 0x3e,    # "u", "U"
# Cannot be implemented         "v" : None, "V" : None,    
# Cannot be implemented         "w" : None, "W" : None,    
# Cannot be implemented         "x" : None, "X" : None,    
                                "y" : 0x6e, "Y" : 0x6e,    # "y"
# Cannot be implemented         "z" : None, "Z" : None,    
                                " " : 0x00,                # " "
                                "-" : 0x40,                # "-"
                                "0" : 0x3f,                # "0"
                                "1" : 0x06,                # "1"
                                "2" : 0x5b,                # "2"
                                "3" : 0x4f,                # "3"
                                "4" : 0x66,                # "4"
                                "5" : 0x6d,                # "5"
                                "6" : 0x7d,                # "6"
                                "7" : 0x07,                # "7"
                                "8" : 0x7f,                # "8"
                                "9" : 0x6f,                # "9"
                                "?" : 0x53                 # "?"
                              }                               

CLEAR_DIGIT                 = 0x7F
POINT_VALUE                 = 0x80

DIGIT_ADDR                  = [0x00, 0x02, 0x06, 0x08]
COLON_ADDR                  = 0x04

HT16K33_BLINK_CMD           = 0x80
HT16K33_BLINK_DISPLAYON     = 0x01
HT16K33_BLINK_OFF           = 0x00
HT16K33_BLINK_2HZ           = 0x02
HT16K33_BLINK_1HZ           = 0x04
HT16K33_BLINK_HALFHZ        = 0x06

HT16K33_SYSTEM_SETUP        = 0x20
HT16K33_OSCILLATOR          = 0x01

HT16K33_BRIGHTNESS_CMD      = 0xE0
HT16K33_BRIGHTNESS_HIGHEST  = 0x0F
HT16K33_BRIGHTNESS_DARKEST  = 0x00


# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------
class HT16K33():
    """ Class to manage a HT16K33 I2C display """
    bus     = None
    address = None
    command = None
    
    def __init__(self, bus, address=0x70):
        """ Initialize variables and set up display """
        self.bus     = bus
        self.address = address
        self.command = "/usr/sbin/i2cset -y {0} {1}".format(bus, address)
        
        self.setup(blink=HT16K33_BLINK_OFF, brightness=HT16K33_BRIGHTNESS_HIGHEST)
        
        self.blank()
    
    # End def
    
    def setup(self, blink, brightness):
        """Initialize the display itself"""
        # i2cset -y 1 0x70 0x21
        os.system("{0} {1}".format(self.command, (HT16K33_SYSTEM_SETUP | HT16K33_OSCILLATOR)))
        # i2cset -y 1 0x70 0x81
        os.system("{0} {1}".format(self.command, (HT16K33_BLINK_CMD | blink | HT16K33_BLINK_DISPLAYON)))
        # i2cset -y 1 0x70 0xEF
        os.system("{0} {1}".format(self.command, (HT16K33_BRIGHTNESS_CMD | brightness)))

    # End def    


    def encode(self, data, double_point=False):
        """Encode data to TM1637 format.
        
        This function will convert the data from decimal to the TM1637 data fromt
        
        :param value: Value must be between 0 and 15
        
        Will throw a ValueError if number is not between 0 and 15.
        """
        ret_val = 0
        
        try:
            if (data != CLEAR_DIGIT):
                if double_point:
                    ret_val = HEX_DIGITS[data] + POINT_VALUE
                else:
                    ret_val = HEX_DIGITS[data]
        except:
            raise ValueError("Digit value must be between 0 and 15.")
    
        return ret_val

    # End def


    def set_digit(self, digit_number, data, double_point=False):
        """Update the given digit of the display."""
        os.system("{0} {1} {2}".format(self.command, DIGIT_ADDR[digit_number], self.encode(data, double_point)))    

    # End def


    def set_digit_raw(self, digit_number, data, double_point=False):
        """Update the given digit of the display using raw data value"""
        os.system("{0} {1} {2}".format(self.command, DIGIT_ADDR[digit_number], data))    

    # End def


    def set_colon(self, enable):
        """Set the colon on the display."""
        if enable:
            os.system("{0} {1} {2}".format(self.command, COLON_ADDR, 0x02))
        else:
            os.system("{0} {1} {2}".format(self.command, COLON_ADDR, 0x00))

    # End def        


    def blank(self):
        """Clear the display to read nothing"""
        self.set_colon(False)

        self.set_digit_raw(3, 0x00)
        self.set_digit_raw(2, 0x00)
        self.set_digit_raw(1, 0x00)
        self.set_digit_raw(0, 0x00)

    # End def


    def clear(self):
        """Clear the display to read '0000'"""
        self.set_colon(False)

        self.set_digit(3, 0)
        self.set_digit(2, 0)
        self.set_digit(1, 0)
        self.set_digit(0, 0)

    # End def


    def update(self, value):
        """Update the value on the display.  
        
        This function will clear the display and then set the appropriate digits
        
        :param value: Value must be between 0 and 9999.
        
        Will throw a ValueError if number is not between 0 and 9999.
        """
        if ((value < 0) or (value > 9999)):
            raise ValueError("Value is not between 0 and 9999")
        
        self.set_digit(3, (value % 10))
        self.set_digit(2, (value // 10) % 10)
        self.set_digit(1, (value // 100) % 10)
        self.set_digit(0, (value // 1000) % 10)

    # End def
    
    def text(self, value):
        """ Update the value on the display with text
        
        :param value:  Value must have between 1 and 4 characters
        
        Will throw a ValueError if there are not the appropriate number of 
        characters or if characters are used that are not supported.
        """
        if ((len(value) < 1) or (len(value) > 4)):
            raise ValueError("Must have between 1 and 4 characters")        
        
        # Clear the display
        self.blank()

        # Set the display to the correct characters        
        for i, char in enumerate(value):
            try:
                char_value = LETTERS[char]
                self.set_digit_raw(i, char_value)
            except:
                raise ValueError("Character {0} not supported".format(char))
    

# End class


# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    import time

    delay = 0.1
    
    print("Test HT16K33 Display:")
    
    display = HT16K33(1, 0x70)

    for i in range(0, 10):
        display.update(i)
        time.sleep(delay)

    for i in range(0, 100, 10):
        display.update(i)
        time.sleep(delay)

    for i in range(0, 1000, 100):
        display.update(i)
        time.sleep(delay)
        
    for i in range(0, 10000, 1000):
        display.update(i)
        time.sleep(delay)

    for value in [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x00]:
        display.set_digit_raw(0, value)
        time.sleep(delay)

    # Test letters
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ?"
    
    for char in letters:
        try:
            display.text(char)
            time.sleep(delay)
        except:
            print("Character not supported:  {0}".format(char))
    
    display.text("done")
    time.sleep(1)
    
    display.set_colon(True)
    time.sleep(1)

    display.clear()    
    print("Test Finished.")



