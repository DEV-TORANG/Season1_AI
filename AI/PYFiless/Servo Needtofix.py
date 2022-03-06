import RPi.GPIO as GPIO
from time import sleep

servoPin = 8
SERVO_MAX_DUTY = 12 #20ms*12%
SERVO_MIN_DUTY = 3  #20ms*3%

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPin, GPIO.OUT)

servo = GPIO.PWM(servoPin, 50)
servo.start(100)

def setServoPos(degree):
    if degree > 180:
        degree = 180
    
    duty = SERVO_MIN_DUTY+(degree*(SERVO_MAX_DUTY-SERVO_MIN_DUTY)/180.0)
    
    print("Degree : {} to {}(Duty)".format(degree, duty))
    
    servo.ChangeDutyCycle(duty)
    
if __name__ == "__main__":
    setServoPos(0)
    sleep(3)
    setServoPos(90)
    sleep(3)
    setServoPos(50)
    sleep(3)
    setServoPos(120)
    sleep(3)
    setServoPos(180)
    sleep(3)
    
    servo.stop()
    GPIO.cleanup()