#!/usr/bin/env python3
from glob import glob
import rospy
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
import RPi.GPIO as GPIO
import numpy as np

global Vr #Velocidad lineal rueda derecha
global Vl #Velocidad lineal rueda izquierda
global l #Distancia entre las ruedas
global r #Radio de las ruedas
global x  #Posicion en x
global y #Posicion en y
global theta #angulo

x = [0]
y = [0]
theta = [0]

Vr = 0
Vl = 0
l = 10 #cm
r = 2 #cm

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


def getPos(x,y,theta,Vr,Vl):
    dt = 0.1
    tiempo = 0.1

    for i in np.arange(0,tiempo,dt):
        x.append( x[-1] + 0.5* (Vr+Vl) * np.cos(theta[-1]) * dt )
        y.append( y[-1] + 0.5* (Vr+Vl) * np.sin(theta[-1]) * dt )
        theta.append( theta[-1] + (1/l) * (Vr-Vl) * dt ) 
        pos=[x[-1],y[-1],theta[-1]]

    return pos


def callback_move(data):
    global x
    global y
    global theta
    velLin = data.linear.x
    velAng = data.angular.z
    PWM_Lin = velLin*100/33 if velLin < 33 else 100
    PWM_Ang = velAng*100/16 if velAng < 16 else 100
    print(PWM_Lin)
    print(PWM_Ang)
    if velLin < 0:
        PWM_Lin = -1*PWM_Lin
        Giro_Favor_Motor_A()
        Giro_Favor_Motor_B() 
        pwm_a.ChangeDutyCycle(PWM_Lin)
        pwm_b.ChangeDutyCycle(PWM_Lin)
        pos = getPos(x, y, theta, -velLin, -velLin)
        x = pos[0]
        y = pos[1]
        theta = pos[2]
        print(pos)
    elif velLin > 0:
        Giro_Contra_Motor_B()
        Giro_Contra_Motor_A()
        pwm_a.ChangeDutyCycle(PWM_Lin)
        pwm_b.ChangeDutyCycle(PWM_Lin)
        pos = getPos(x, y, theta, velLin, velLin)
        x = pos[0]
        y = pos[1]
        theta = pos[2]
        print(pos)
    
    elif velAng < 0:
        PWM_Ang = -1*PWM_Ang
        Giro_Favor_Motor_B()
        Giro_Contra_Motor_A()
        pwm_a.ChangeDutyCycle(PWM_Ang)
        pwm_b.ChangeDutyCycle(PWM_Ang)
        pos = getPos(x, y, theta, -velAng, velAng)
        x = pos[0]
        y = pos[1]
        theta = pos[2]
        print(pos)

    elif velAng > 0:
        Giro_Contra_Motor_B()
        Giro_Favor_Motor_A()
        pwm_a.ChangeDutyCycle(PWM_Ang)
        pwm_b.ChangeDutyCycle(PWM_Ang)
        pos = getPos(x, y, theta, velAng, -velAng)
        x = pos[0]
        y = pos[1]
        theta = pos[2]
        print(pos)
    else:
        pwm_a.ChangeDutyCycle(0)
        pwm_b.ChangeDutyCycle(0)

def listener():
    rospy.init_node('robot_listener', anonymous=True)
    rospy.Subscriber('/robot_cmdVel', Twist, callback_move)
    pub_postion = rospy.Publisher('/robot_position', Twist, queue_size=10)
    pub_orientation = rospy.Publisher('/robot_orientation', Float32, queue_size=10)
    rospy.spin()
    GPIO.cleanup()

if __name__ == '__main__':
    listener()