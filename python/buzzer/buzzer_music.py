# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Music
--------------------------------------------------------------------------
License:   
Copyright 2020 Erik Welsh

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
# Note Library
# ------------------------------------------------------------------------
NOTE_B0  = 31
NOTE_C1  = 33
NOTE_CS1 = 35
NOTE_D1  = 37
NOTE_DS1 = 39
NOTE_E1  = 41
NOTE_F1  = 44
NOTE_FS1 = 46
NOTE_G1  = 49
NOTE_GS1 = 52
NOTE_A1  = 55
NOTE_AS1 = 58
NOTE_B1  = 62
NOTE_C2  = 65
NOTE_CS2 = 69
NOTE_D2  = 73
NOTE_DS2 = 78
NOTE_E2  = 82
NOTE_F2  = 87
NOTE_FS2 = 93
NOTE_G2  = 98
NOTE_GS2 = 104
NOTE_A2  = 110
NOTE_AS2 = 117
NOTE_B2  = 123
NOTE_C3  = 131
NOTE_CS3 = 139
NOTE_D3  = 147
NOTE_DS3 = 156
NOTE_E3  = 165
NOTE_F3  = 175
NOTE_FS3 = 185
NOTE_G3  = 196
NOTE_GS3 = 208
NOTE_A3  = 220
NOTE_AS3 = 233
NOTE_B3  = 247
NOTE_C4  = 262
NOTE_CS4 = 277
NOTE_D4  = 294
NOTE_DS4 = 311
NOTE_E4  = 330
NOTE_F4  = 349
NOTE_FS4 = 370
NOTE_G4  = 392
NOTE_GS4 = 415
NOTE_A4  = 440
NOTE_AS4 = 466
NOTE_B4  = 494
NOTE_C5  = 523
NOTE_CS5 = 554
NOTE_D5  = 587
NOTE_DS5 = 622
NOTE_E5  = 659
NOTE_F5  = 698
NOTE_FS5 = 740
NOTE_G5  = 784
NOTE_GS5 = 831
NOTE_A5  = 880
NOTE_AS5 = 932
NOTE_B5  = 988
NOTE_C6  = 1047
NOTE_CS6 = 1109
NOTE_D6  = 1175
NOTE_DS6 = 1245
NOTE_E6  = 1319
NOTE_F6  = 1397
NOTE_FS6 = 1480
NOTE_G6  = 1568
NOTE_GS6 = 1661
NOTE_A6  = 1760
NOTE_AS6 = 1865
NOTE_B6  = 1976
NOTE_C7  = 2093
NOTE_CS7 = 2217
NOTE_D7  = 2349
NOTE_DS7 = 2489
NOTE_E7  = 2637
NOTE_F7  = 2794
NOTE_FS7 = 2960
NOTE_G7  = 3136
NOTE_GS7 = 3322
NOTE_A7  = 3520
NOTE_AS7 = 3729
NOTE_B7  = 3951
NOTE_C8  = 4186
NOTE_CS8 = 4435
NOTE_D8  = 4699
NOTE_DS8 = 4978

# ------------------------------------------------------------------------
# Main Tasks
# ------------------------------------------------------------------------

class BuzzerMusic():
    pin       = None
    song_list = None

    def __init__(self, pin, song_list=None):
        self.pin = pin
        
        if song_list is not None:
            self.song_list = song_list
        else:
            self.song_list = [
                self.zelda_secret, self.zelda_lullaby, self.zelda_epona_song,
                self.zelda_saria_song, self.zelda_sun_song, self.zelda_song_of_time,
                self.zelda_minuet_of_forest, self.zelda_bolero_of_fire, self.zelda_serenade_of_water,
                self.zelda_requiem_of_spirit, self.zelda_nocturne_of_shadow, self.zelda_preulde_of_light]
    
    # End def
    
    def play_song(self, number):
        if number < len(self.song_list):
            song = self.song_list[number]
            song()
    # End def
    
    def play_note(self, note, length):
        """Plays a given note for a given length."""
        PWM.start(self.pin, 50, note)
        time.sleep(length)
    # end def
    
    def stop(self):
        PWM.stop(self.pin)
    # End def
    
    def cleanup(self):
        PWM.cleanup()
    # End def
    
    
    def zelda_secret(self):
        """Plays the Uncover Secret song from The Legend of Zelda."""
        self.play_note(NOTE_G5, 0.15)
        self.play_note(NOTE_FS5, 0.15)
        self.play_note(NOTE_DS5, 0.15)
        self.play_note(NOTE_A4, 0.15)
        self.play_note(NOTE_GS4, 0.15)
        self.play_note(NOTE_E5, 0.15)
        self.play_note(NOTE_GS5, 0.15)
        self.play_note(NOTE_C6, 0.15)
        self.stop()
    # end def

    def zelda_lullaby(self):
        """Plays Zelda's Lullaby from The Legend of Zelda."""
        self.play_note(NOTE_B4, 1.2)
        self.play_note(NOTE_D5, 0.6)
        self.play_note(NOTE_A4, 1.8)
        self.play_note(NOTE_B4, 1.2)
        self.play_note(NOTE_D5, 0.6)
        self.play_note(NOTE_A4, 1.8)
        self.stop()
    # end def

    def zelda_epona_song(self):
        """Plays Epona's Song from The Legend of Zelda."""
        self.play_note(NOTE_D5, 0.35)
        self.play_note(NOTE_B4, 0.35)
        self.play_note(NOTE_A4, 1.4)
        self.play_note(NOTE_D5, 0.35)
        self.play_note(NOTE_B4, 0.35)
        self.play_note(NOTE_A4, 1.4)
        self.play_note(NOTE_D5, 0.35)
        self.play_note(NOTE_B4, 0.35)
        self.play_note(NOTE_A4, 0.7)
        self.play_note(NOTE_B4, 0.7)
        self.play_note(NOTE_A4, 1.5)
        self.stop()
    # end def

    def zelda_saria_song(self):
        """Plays Saria's Song from The Legend of Zelda."""
        self.play_note(NOTE_F4, 0.15)
        self.play_note(NOTE_A4, 0.15)
        self.play_note(NOTE_B4, 0.3)
        self.play_note(NOTE_F4, 0.15)
        self.play_note(NOTE_A4, 0.15)
        self.play_note(NOTE_B4, 0.3)
        self.play_note(NOTE_F4, 0.15)
        self.play_note(NOTE_A4, 0.15)
        self.play_note(NOTE_B4, 0.15)
        self.play_note(NOTE_E4, 0.15)
        self.play_note(NOTE_D5, 0.3)
        self.play_note(NOTE_B4, 0.15)
        self.play_note(NOTE_C5, 0.15)
        self.play_note(NOTE_B4, 0.15)
        self.play_note(NOTE_G4, 0.15)
        self.play_note(NOTE_E4, 0.6)
        self.stop()
    # end def

    def zelda_song_of_storms(self):
        """Plays the Song of Storms from The Legend of Zelda."""
        self.play_note(NOTE_D4, 0.15)
        self.play_note(NOTE_F4, 0.15)
        self.play_note(NOTE_D5, 0.6)
        self.play_note(NOTE_D4, 0.15)
        self.play_note(NOTE_F4, 0.15)
        self.play_note(NOTE_D5, 0.6)
        self.play_note(NOTE_E5, 0.45)
        self.play_note(NOTE_F5, 0.15)
        self.play_note(NOTE_E5, 0.15)
        self.play_note(NOTE_F5, 0.15)
        self.play_note(NOTE_E5, 0.15)
        self.play_note(NOTE_C5, 0.15)
        self.play_note(NOTE_A4, 0.6)
        self.stop()
    # end def

    def zelda_sun_song(self):
        """Plays the Sun's Song from The Legend of Zelda."""
        self.play_note(NOTE_A4, 0.15)
        self.play_note(NOTE_F4, 0.15)
        self.play_note(NOTE_D5, 0.3)
        self.stop()
        time.sleep(0.3)
        self.play_note(NOTE_A4, 0.15)
        self.play_note(NOTE_F4, 0.15)
        self.play_note(NOTE_D5, 0.3)
        self.stop()
        time.sleep(0.3)
        self.play_note(NOTE_G4, 0.1)
        self.play_note(NOTE_A4, 0.1)
        self.play_note(NOTE_B4, 0.1)
        self.play_note(NOTE_C5, 0.1)
        self.play_note(NOTE_D5, 0.1)
        self.play_note(NOTE_E5, 0.1)
        self.play_note(NOTE_F5, 0.1)
        self.play_note(NOTE_G5, 0.125)
        self.play_note(NOTE_G5, 0.125)
        self.play_note(NOTE_G5, 0.125)
        self.play_note(NOTE_G5, 0.125)
        self.play_note(NOTE_G5, 0.125)
        self.play_note(NOTE_G5, 0.125)
        self.play_note(NOTE_G5, 0.125)
        self.play_note(NOTE_G5, 0.125)
        self.stop()
    # end def

    def zelda_song_of_time(self):
        """Plays the Song of Time from The Legend of Zelda."""
        self.play_note(NOTE_A4, 0.5)
        self.play_note(NOTE_D4, 1.0)
        self.play_note(NOTE_F4, 0.5)
        self.play_note(NOTE_A4, 0.5)
        self.play_note(NOTE_D4, 1.0)
        self.play_note(NOTE_F4, 0.5)
        self.play_note(NOTE_A4, 0.25)
        self.play_note(NOTE_C5, 0.25)
        self.play_note(NOTE_B4, 0.5)
        self.play_note(NOTE_G4, 0.5)
        self.play_note(NOTE_F4, 0.25)
        self.play_note(NOTE_G4, 0.25)
        self.play_note(NOTE_A4, 0.5)
        self.play_note(NOTE_D4, 0.5)
        self.play_note(NOTE_C4, 0.25)
        self.play_note(NOTE_E4, 0.25)
        self.play_note(NOTE_D4, 1.5)
        self.stop()
    # end def

    def zelda_minuet_of_forest(self):
        """Plays the Minuet of Forest from The Legend of Zelda."""
        self.play_note(NOTE_D5, 0.225)
        self.play_note(NOTE_D6, 0.225)
        self.play_note(NOTE_B5, 0.9)
        self.play_note(NOTE_A5, 0.225)
        self.play_note(NOTE_B5, 0.225)
        self.play_note(NOTE_A5, 0.9)
        self.stop()
    # end def

    def zelda_bolero_of_fire(self):
        """Plays the Bolero of Fire from The Legend of Zelda."""
        self.play_note(NOTE_F4, 0.225)
        self.play_note(NOTE_D4, 0.225)
        self.play_note(NOTE_F4, 0.225)
        self.play_note(NOTE_D4, 0.225)
        self.play_note(NOTE_A4, 0.225)
        self.play_note(NOTE_F4, 0.225)
        self.play_note(NOTE_A4, 0.225)
        self.play_note(NOTE_F4, 0.9375)
        self.stop()
    # end def

    def zelda_serenade_of_water(self):
        """Plays the Serenade of Water from The Legend of Zelda."""
        self.play_note(NOTE_D5, 0.5)
        self.play_note(NOTE_F5, 0.5)
        self.play_note(NOTE_A5, 0.5)
        self.play_note(NOTE_A5, 0.5)
        self.play_note(NOTE_B5, 1.0)
        self.stop()
    # end def

    def zelda_requiem_of_spirit(self):
        """Plays the Requiem of Spirit from The Legend of Zelda."""
        self.play_note(NOTE_D5, 0.75)
        self.play_note(NOTE_F5, 0.375)
        self.play_note(NOTE_D5, 0.375)
        self.play_note(NOTE_A5, 0.75)
        self.play_note(NOTE_F5, 0.75)
        self.play_note(NOTE_D5, 1.5)
        self.stop()
    # end def

    def zelda_nocturne_of_shadow(self):
        """Plays the Nocturne of Shadow from The Legend of Zelda."""
        self.play_note(NOTE_B4, 0.67)
        self.play_note(NOTE_A4, 0.67)
        self.play_note(NOTE_A4, 0.33)
        self.play_note(NOTE_D4, 0.33)
        self.play_note(NOTE_B4, 0.33)
        self.play_note(NOTE_A4, 0.33)
        self.play_note(NOTE_F4, 1.5)
        self.stop()
    # end def

    def zelda_preulde_of_light(self):
        """Plays the Prelude of Light from The Legend of Zelda."""
        self.play_note(NOTE_D5, 0.25)
        self.play_note(NOTE_A4, 0.75)
        self.play_note(NOTE_D5, 0.25)
        self.play_note(NOTE_A4, 0.25)
        self.play_note(NOTE_B4, 0.25)
        self.play_note(NOTE_D5, 1.25)
        self.stop()
    # end def

# End class

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    
    music = BuzzerMusic("P2_1")
    
    for i in range(1):
        print("Song {0}".format(i))
        music.play_song(i)

        