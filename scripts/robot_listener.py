#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import RPi.GPIO as GPIO


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
GPIO.setup(ena, GPIO.OUT)
GPIO.setup(enb, GPIO.OUT)
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

#funciones de los motores
def Adelante():
    GPIO.output(in2,True)
    GPIO.output(in1,False)
    GPIO.output(in3,True)
    GPIO.output(in4,False)

def Reversa():
    GPIO.output(in2,False)
    GPIO.output(in1,True)
    GPIO.output(in3,False)
    GPIO.output(in4,True)

def Giro_Favor_Motor_A():
    GPIO.output(in1,True)
    GPIO.output(in2,False)


def Giro_Contra_Motor_A():
    GPIO.output(in1,False)
    GPIO.output(in2,True)


def Giro_Favor_Motor_B():
    GPIO.output(in3,False)
    GPIO.output(in4,True)


def Giro_Contra_Motor_B():
    GPIO.output(in3,True)
    GPIO.output(in4,False)


def callback_move(data):
    velLin = data.linear.x
    velAng = data.angular.z

    PWM_Lin = velLin*100/56 if velLin < 33 else 100
    PWM_Ang = velAng*100/16 if velAng < 16 else 100

    if velLin < 0:
        PWM_Lin = -1*PWM_Lin
        Giro_Favor_Motor_A()
        Giro_Favor_Motor_B() 
        pwm_a.ChangeDutyCycle(PWM_Lin)
        pwm_b.ChangeDutyCycle(PWM_Lin)

    elif velLin > 0:
        Giro_Contra_Motor_B()
        Giro_Contra_Motor_A()
        pwm_a.ChangeDutyCycle(PWM_Lin)
        pwm_b.ChangeDutyCycle(PWM_Lin)

    
    elif velAng < 0:
        PWM_Ang = -1*PWM_Ang
        Giro_Favor_Motor_B()
        Giro_Contra_Motor_A()
        pwm_a.ChangeDutyCycle(PWM_Ang)
        pwm_b.ChangeDutyCycle(PWM_Ang)


    elif velAng > 0:
        Giro_Contra_Motor_B()
        Giro_Favor_Motor_A()
        pwm_a.ChangeDutyCycle(PWM_Ang)
        pwm_b.ChangeDutyCycle(PWM_Ang)

    else:
        pwm_a.ChangeDutyCycle(0)
        pwm_b.ChangeDutyCycle(0)


def listener():
    global pub_orientation
    global pub_position
    rospy.init_node('robot_listener', anonymous=True)
    rospy.Subscriber('/robot_cmdVel', Twist, callback_move)
    rospy.spin()
    GPIO.cleanup()

if __name__ == '__main__':
    listener()