#!/usr/bin/env python

import time
import pigpio
import sys
sys.path.append('/root/lidar/Lidar-Lite/python')

from lidar_lite import Lidar_Lite


SERVO_GPIO   = 18       #GPIO number of the attached servo
PULSE_CONST  = 10.588   #10.588 PWM per 1 degree
cur_pulse    = 0
cur_angle    = 0

pi = pigpio.pi()
lidar = Lidar_Lite()
distance = -1
velocity = -1

lidar_connected = lidar.connect(1)

def debug_print():
    print("Servo angle: {}, pulse: {}".format(cur_angle, cur_pulse))
    print("Lidar distance: {}".format(distance))
    return

def set_servo(pulse):
    pi.set_servo_pulsewidth(SERVO_GPIO, pulse)
#   distance = lidar.getDistance()
#   velocity = lidar.getVelocity()
    time.sleep(.005) # Sleep time for lidar_thread to finish
#   debug_print()
    return

CENTER_PULSE   = 1550   #PWM for servo center/middle
angle_movement = 45     #Number of degrees to rotate left+right of center
ANGLE_CHANGE   = 1      #Move servo 2 deegrees each pulse
degree_change  = ANGLE_CHANGE * PULSE_CONST  #1 degree change = 10.588 PWM

#Max PWM for left and right
max_left   = CENTER_PULSE - (angle_movement * PULSE_CONST)
max_right  = CENTER_PULSE + (angle_movement * PULSE_CONST)

cur_pulse = max_left
cur_angle = (cur_pulse / PULSE_CONST) - (CENTER_PULSE / PULSE_CONST)

if lidar_connected < -1:
    print("Lidar not connected...")
    sys.exit(0)
else:
    print("Lidar connected")

try:
    #Start servo at the left
    set_servo(max_left)
    #distance = lidar.getDistance()
    debug_print()

    while True:
        #Servo position all the way to the left, start moving right
        while cur_pulse < max_right:
            cur_pulse = cur_pulse + degree_change
            cur_angle = cur_angle + ANGLE_CHANGE
            set_servo(cur_pulse)
     #       distance = lidar.getDistance()
            debug_print()

        #Servo position all the way to the right, start moving left
        while cur_pulse > max_left:
            cur_pulse = cur_pulse - degree_change
            cur_angle = cur_angle - ANGLE_CHANGE
            set_servo(cur_pulse)
      #      distance = lidar.getDistance()
            debug_print()



except KeyboardInterrupt:
    #Switch servo off
    set_servo(0)

    pi.stop()
