import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

pin = 17

GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, GPIO.HIGH)
    
while 1:
    print("Checking pin out")
    time.sleep(5)

GPIO.cleanup()