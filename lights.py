import RPi.GPIO as GPIO
import time
import os

#We start setting the usage of the pins
GPIO.cleanup()
inpin = (27, 17, 22)
outpin = (2, 4)
GPIO.setmode(GPIO.BCM)
GPIO.setup(outpin, GPIO.OUT)
GPIO.setup(inpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.output(outpin, True)

#We also define some useful variables
previousButtonState = [False, False, False]
lightStateChanges = [0, 0, 0]
actions = [0, 0]
lightState = [False, False]
off = False
print("Running now... (The RaspiLights script)")

#Then, we start the main loop:
while True:
	
	
	#First, we get the button states, store then in buttonState, and compare with the previous ones.
	#The changes are stored in lightStateChanges, and buttonState becomes previousButtonState.
	
	buttonState = [not GPIO.input(inpin[0]), not GPIO.input(inpin[1]), not GPIO.input(inpin[2])]
	for i in range(3):
		if previousButtonState[i] != buttonState[i]:
			lightStateChanges[i] = 1
	previousButtonState = buttonState
	
	
	#Here we check the state of the files that are created thought SSH, and delete the existing files that indicate changes.
	#As this loop runs 10 times a second, we are going to assume that either the file, or the button state is changed.
	
	if os.path.isfile("/home/pi/RaspiLights/switch1"):
		lightStateChanges[0] = 1
		os.system("rm /home/pi/RaspiLights/switch1")
	if os.path.isfile("/home/pi/RaspiLights/switch2"):
		lightStateChanges[1] = 1
		os.system("rm /home/pi/RaspiLights/switch2")
	if os.path.isfile("/home/pi/RaspiLights/switch"):
		lightStateChanges[2] = 1
		os.system("rm /home/pi/RaspiLights/switch")
	if os.path.isfile("/home/pi/RaspiLights/off"):
		off = True
		os.system("rm /home/pi/RaspiLights/off")
	
	
	#Now we are going to calculate the actions that are going to happen, based on the changes calculated before.
        #We are going to prioritize lights being on, so swithing lights with one being on makes both on.
        #In actions, 0 means "doesn't change", 1 means "turns off", and 2 means "turns on".
	
	for i in range(2):
		if lightStateChanges[i]:                    #if there is going to be a change
			if lightState[i]: actions[i] = 1    #if the light is on, we turn it off
			else: actions[i] = 2                #otherwise, we turn it off
	
	if lightStateChanges[2]:                            #if the main switch is switched
		if lightState[0] != lightState[1]:          #if the lamps differ, we turn both on
			actions = [2, 2]
		else:
			if lightState[0]: actions = [1, 1]  #otherwise, we switch their state.
			else: actions = [2, 2]
	
	if off:                      #with the off commmand, we turn both off, regardless of their state
		actions = [1, 1]
		off = False
	
	lightStateChanges = [0, 0, 0]
	
	
	#Finally, we switch the lamps according to "actions"
	
	try:
		if actions[0]:
			if actions[0] == 2:
				print("Light turned on!")
				GPIO.output(outpin[0], False)
				lightState[0] = True
			else:
				print("Light turned off!")
				GPIO.output(outpin[0], True)
				lightState[0] = False
		if actions[1]:
			if actions[1] == 2:
				print("Light turned on!")
				GPIO.output(outpin[1], False)
				lightState[1] = True
			else:
				print("Light turned off!")
				GPIO.output(outpin[1], True)
				lightState[1] = False
	except:
		GPIO.cleanup()  #A GPIO cleanup in this part is usualy good measure.
	
	actions = [0, 0]
	
	
	#Now we wait and restart the loop.
	
	time.sleep(0.1)
