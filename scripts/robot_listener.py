#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import RPi.GPIO as GPIO
import os
import time

#Define nombre de las entradas del puente H
ena = 18			
in1 = 23
in2 = 24

enb = 19
in3 = 6
in4 = 5

#configura los pines segun el microprocesador Broadcom
GPIO.setmode(GPIO.BCM)
#configura los pines como salidas
GPIO.setup(ena,GPIO.OUT)
GPIO.setup(enb,GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
#Define las salidas PWM q
pwm_a = GPIO.PWM(ena,500)
pwm_b = GPIO.PWM(enb,500)
#inicializan los PWM con un duty Cicly de cero
pwm_a.start(0)
pwm_b.start(0)
# funciones de sentido de giro de los motores
# def  Giro_Favor_Reloj_MotorA():
# 	GPIO.output(in2,False)
# 	GPIO.output(in1,True)

# def Giro_Contra_Reloj_MotorA():
# 	GPIO.output(in2,True)
# 	GPIO.output(in1,False)

# def  Giro_Favor_Reloj_MotorB():
# 	GPIO.output(in3,False)
# 	GPIO.output(in4,True)

# def Giro_Contra_Reloj_MotorB():
# 	GPIO.output(in3,True)
# 	GPIO.output(in4,False)

def Adelante():
    GPIO.output(in2,False)
    GPIO.output(in1,True)
    GPIO.output(in3,False)
    GPIO.output(in4,True)
def Reversa():
	GPIO.output(in2,True)
	GPIO.output(in1,False)
	GPIO.output(in3,True)
	GPIO.output(in4,False)




def callback_move(data):
    velocidad = int(data.linear.x)
    if velocidad > 0:
        Adelante()
        pwm_a.ChangeDutyCycle(velocidad)
        pwm_b.ChangeDutyCycle(velocidad)
    if velocidad < 0:
        velocidad = -1*velocidad
        Reversa()
        pwm_a.ChangeDutyCycle(velocidad)
        pwm_b.ChangeDutyCycle(velocidad)

    print(velocidad)
    

def listener():
    rospy.init_node('robot_listener', anonymous=True)
    rospy.Subscriber('/robot_cmdVel', Twist, callback_move)
    rospy.spin()



if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass