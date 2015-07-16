import pigpio
import time

def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

servos = 18

pi = pigpio.pi()

while True:
	pw = input("Enter pulse width from 500 - 2500, or 0: ")
	
	if is_number(pw) == False:
		break
	
	if pw < 500 and pw != 0:
		print("Value cannot be below 500. Setting pw to 500...")
		pw = 500
	elif pw > 2500:
		print("Value cannot be above 2500. Setting pw to 2500...")
		pw = 2500
	
	pi.set_servo_pulsewidth(servos, pw)
	print("Servo {} {} micro pulses".format(servos, pw))

pi.stop()
