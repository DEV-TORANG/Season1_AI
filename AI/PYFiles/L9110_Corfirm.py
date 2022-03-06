import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

A=3
B=5

GPIO.setup(A, GPIO.OUT)
GPIO.setup(B, GPIO.OUT)

try:
    while 1:
        GPIO.output(A, GPIO.HIGH)
        GPIO.output(B, GPIO.LOW)
        time.sleep(5)
        GPIO.output(A, GPIO.LOW)
        GPIO.output(B, GPIO.LOW)
        time.sleep(2)
        GPIO.output(A, GPIO.LOW)
        GPIO.output(B, GPIO.HIGH)
        time.sleep(5)
        GPIO.output(A, GPIO.LOW)
        GPIO.output(B, GPIO.LOW)
        time.sleep(2)
except KeyboardInterrupt:
    GPIO.output(A, GPIO.LOW)
    GPIO.output(B, GPIO.LOW)
    GPIO.cleanup()