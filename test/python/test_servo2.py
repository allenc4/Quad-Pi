#!/usr/bin/env python

import time
import pigpio
import sys
sys.path.append('/root/lidar/Lidar-Lite/python')

from lidar_lite import Lidar_Lite

servos = 18
cur_pulse = 0
cur_angle = 0
pi = pigpio.pi()
lidar = Lidar_Lite()
distance = -1
velocity = -1

l_connected = lidar.connect(1)

def debug_print():
	print("Current angle: {}, current pulse: {}".format(cur_angle, cur_pulse))
	print("Lidar distance: {}, Lidar velocity: {}".format(distance, velocity))

def set_servo(pulse):
	pi.set_servo_pulsewidth(servos, pulse)
	distance = lidar.getDistance()
#	velocity = lidar.getVelocity()
#	time.sleep(.02)
#	debug_print()

degree_change = 21.16 #1 degree = 10.588
center_pulse = 1500
angle_movement = 25

max_left = center_pulse - (angle_movement * degree_change)
max_right = center_pulse + (angle_movement * degree_change)

cur_pulse = max_left
cur_angle = 90 - ((center_pulse - cur_pulse) / degree_change)

if l_connected < -1:
	print("Not connected")
	sys.exit(0)
else:
	print("Connected")

try:
	#start at the left
	set_servo(max_left)

	while True:
		#servo position all the way to the left, start moving right
		
#        print lidar.getDistance()
        while cur_pulse < max_right:
			cur_pulse = cur_pulse + degree_change
			cur_angle = cur_angle + 1
			set_servo(cur_pulse)

		#servo position all the way to the right, start moving left
		while cur_pulse > max_left:
			cur_pulse = cur_pulse - degree_change
			cur_angle = cur_angle - 1
			set_servo(cur_pulse)


	"""pi.set_servo_pulsewidth(servos, 1000) #safe anti-clockwise
        print("Servo {} {} micro pulses".format(servos, 1000))
        time.sleep(2)

        pi.set_servo_pulsewidth(servos, 1500) #center
        print("Servo {} {} micro pulses".format(servos, 1500))
        time.sleep(2)

        pi.set_servo_pulsewidth(servos, 2000) #safe clockwise
        print("Servo {} {} micro pulses".format(servos, 2500))
        time.sleep(2)

        pi.set_servo_pulsewidth(servos, 1500) #center
        print("Servo {} {} micro pulses".format(servos, 1500))
        time.sleep(2)"""

    #switch all servos off
except KeyboardInterrupt:
    pi.set_servo_pulsewidth(servos, 0);

pi.stop()
