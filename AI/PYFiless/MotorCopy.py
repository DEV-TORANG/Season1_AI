# -*- coding: utf-8 -*-

#raspberryPi GPIO package
import RPi.GPIO as GPIO
import sys
from time import sleep

GPIO.setwarnings(False)
    
#Motor statement
STOP = 0
FORWARD = 1
BACKWARD = 2

#Motor channel
CH1 = 0
CH2 = 1

#Pin IO set
OUTPUT = 1
INPUT = 0

#Pin set
HIGH = 1
LOW = 0

#Define Pin number in now
#PWM Pin
ENA = 26 #37pin
ENB = 0  #27pin

#GPIO Pin
IN1 = 19 #37pin
IN2 = 13 #35pin
IN3 = 6  #31pin
IN4 = 5  #29pin

#Pin setup function
def setPinConfig(EN, INA, INB):
    GPIO.setup(EN, GPIO.OUT)
    GPIO.setup(INA, GPIO.OUT)
    GPIO.setup(INB, GPIO.OUT)
    #Run PWM test in 100kHz
    pwm = GPIO.PWM(EN, 100)
    #PWM set start 0.
    pwm.start(0)
    return pwm

#Motor Control function
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
        

        
def setReceivedFanSpeed(speed):
    if speed == 0 :
        setMotor(CH1, 0, STOP)
        setMotor(CH2, 0, STOP)
        return
    elif speed < 0 or speed > 20:
        print("Can't accept input power. Please input number. (0 < speed(input) < 21)")
        return
    speed=speed*2+11
    #BACKWARD in 25% speed
    setMotor(CH1, speed, BACKWARD)
    setMotor(CH2, speed, BACKWARD)
    #sleep(5)
        
GPIO.setmode(GPIO.BCM)

pwmA = setPinConfig(ENA, IN1, IN2)
pwmB = setPinConfig(ENB, IN3, IN4)

#setReceivedFanSpeed(0)
#int(sys.argv[1])
#setReceivedFanSpeed(int(sys.argv[1]))
'''
#Start Control
while True:
    
    #FORWARD in 10% speed
    setMotor(CH1, 10, FORWARD)
    setMotor(CH2, 10, FORWARD)
    sleep(5)

    #BACKWARD in 25% speed
    setMotor(CH1, 25, BACKWARD)
    setMotor(CH2, 25, BACKWARD)
    sleep(5)

    #STOP
    setMotor(CH1, 0, STOP)
    setMotor(CH1, 0, STOP)
    sleep(5)

GPIO.cleanup()
'''