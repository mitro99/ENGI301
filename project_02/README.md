### No Touch Gesture Calculator

Hackster Project can be found at https://www.hackster.io/andrei-mitrofan/no-touch-gesture-calculator-40e7d4

##Story

I work in a research lab and taking my gloves off just to do some basic arithmetic on my phone has always seemed very inefficient and kind of annoying to do, since once you take gloves off it's a nightmare to put them back on immediately afterward. Therefore, I designed this gesture calculator that allows me to do all those basic calculations without having to take my gloves off or worry about contaminating my phone. I've also wanted to dive into tinyML for a while now, so this felt like an appropriate project on which to implement my first TFLite project on the PocketBeagle.

##PCB Design

I have created a PCB for the project in order to minimize its size and make it more comfortable to be used as an actual wearable. This repository contains all the files necessary for manufacturing the board.:

-"docs" contains the original project proposal, as well as PDF files of the schematic, top and bottom of the actual PCB, and the bill of materials.

-"EAGLE" contains all the EAGLE file, including the library with all the components used, the schematic, the board, and the design rules.

-"mfg" contains all the manufacturing files, most notably the Gerber files.

##Operation Instructions

The device is set up to run the inference code upon boot, so you just need to plug in the PocketBeagle and, after waiting for a couple of minutes, it should be up and ready to predict gestures. The flow of the calculator is as follows:

-Draw out the first number in the air

-Flick your wrist (this advances the calculator to the operator selector)

-Draw out a digit 1 - 5 to select the operator you want

-Draw out the second number in the air

-Flick your wrist again to calculate the result
