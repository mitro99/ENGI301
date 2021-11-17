### No Touch Gesture Calculator

Hackster Project can be found at https://www.hackster.io/andrei-mitrofan/no-touch-gesture-calculator-40e7d4

##Story

I work in a research lab and taking my gloves off just to do some basic arithmetic on my phone has always seemed very inefficient and kind of annoying to do, since once you take gloves off it's a nightmare to put them back on immediately afterward. Therefore, I designed this gesture calculator that allows me to do all those basic calculations without having to take my gloves off or worry about contaminating my phone. I've also wanted to dive into tinyML for a while now, so this felt like an appropriate project on which to implement my first TFLite project on the PocketBeagle.

##Build Instructions

From a hardware point of view, this project is pretty simple, all you need is the PocketBeagle, the MPU6050 IMU, and the OLED Screen. Since the PocketBeagle might be an unfamiliar platform for some of you, I am attaching the pin diagram of it here. The top of the diagram corresponds to the micro-USB port.

##Code
There are 4 main documents in this repository, inside the testing folder as well as 2 additional files needed for configuring the PocketBeagle pins and running the script (run.sh, configure_pins.sh): 
-Acquisition.py
-Data Visualization.ipynb
-Training model.ipynb
-Predict.py

##Operation Instructions

The device is set up to run the inference code upon boot, so you just need to plug in the PocketBeagle and, after waiting for a couple of minutes, it should be up and ready to predict gestures. The flow of the calculator is as follows:

-Draw out the first number in the air

-Flick your wrist (this advances the calculator to the operator selector)

-Draw out a digit 1 - 5 to select the operator you want

-Draw out the second number in the air

-Flick your wrist again to calculate the result
