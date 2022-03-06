from gpiozero import Motor
import time

motor = Motor(forward = 20, backward = 21)

while True:
    print('Forward')
    motor.forward(speed = 0.3)
    time.sleep(3)
    
    print('Backward')
    motor.backward(speed = 0.5)
    time.sleep(3)