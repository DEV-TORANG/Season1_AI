import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

A=11
B=12

GPIO.setup(A, GPIO.OUT)
GPIO.setup(B, GPIO.OUT)

pwm = GPIO.PWM(A, 100)
pwm.start(30)

try:
    while 1:
        for n in range(0, 100, 5):
            pwm.ChangeDutyCycle(n)
            GPIO.output(B, GPIO.LOW)
            time.sleep(3)
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()