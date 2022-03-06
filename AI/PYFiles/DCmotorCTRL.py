#RaspberryPI GPIO Packages
import RPi.GPIO as GPIO
from time import sleep

#GPIO.cleanup()

#Motor Statement
STOP = 0
FORWARD = 1
BACKWARD = 2

#Motor Channel
CH1 = 0
CH2 = 1

#Pin IO Set
OUTPUT = 1
INPUT = 0

#Pin Set
HIGH = 1
LOW = 0

#PWM PIN
ENA = 26 #37 Pin
ENB = 0  #27 Pin

#GPIO PIN
IN1 = 19 #37 Pin
IN2 = 13 #35 Pin
IN3 = 6  #31 Pin
IN4 = 5  #29 Pin

#Pin Set Function
def setPinConfig(EN, INA, INB):
    GPIO.setup(EN, GPIO.OUT)
    GPIO.setup(INA, GPIO.OUT)
    GPIO.setup(INB, GPIO.OUT)
    # 100Khz PWM set
    pwm = GPIO.PWM(EN, 100)
    pwm.start(0)
    return pwm

#Motor control function
def setMotorControl(pwm, INA, INB, speed, stat):
    #Motor speed control PWM
    pwm.ChangeDutyCycle(speed)
    if stat == FORWARD:
        GPIO.output(INA, HIGH)
        GPIO.output(INB, LOW)
    elif stat == BACKWARD:
        GPIO.output(INA, LOW)
        GPIO.output(INB, HIGH)
    elif stat == STOP:
        GPIO.output(INA, LOW)
        GPIO.output(INB, LOW)
        
#Rapping
def setMotor(ch, speed, stat):
    if ch == CH1:
        setMotorControl(pwmA, IN1, IN2, speed, stat)
    else :
        setMotorControl(pwmB, IN3, IN4, speed, stat)
        
GPIO.setmode(GPIO.BCM)

pwmA = setPinConfig(ENA, IN1, IN2)
pwmB = setPinConfig(ENB, IN3, IN4)

#Start Control

#FORWARD in 80% speed
setMotor(CH1, 80, FORWARD)
setMotor(CH2, 80, FORWARD)
sleep(5)

#BACKWARD in 40% speed
setMotor(CH1, 40, BACKWARD)
setMotor(CH2, 40, BACKWARD)
sleep(5)

#STOP
setMotor(CH1, 0, STOP)
setMotor(CH1, 0, STOP)

GPIO.cleanup()