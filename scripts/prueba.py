#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from pynput import keyboard as kb

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

move_msg = Twist()
velLin = 0
velAng = 0

move_msg.linear.x = 0
move_msg.linear.y = 0
move_msg.linear.z = 0
move_msg.angular.x = 0
move_msg.angular.y = 0
move_msg.angular.z = 0

directory = os.path.dirname(__file__)

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

def on_press(key):
    #print(move)
    try:
        if key.char == 'w':
            Adelante()
            pwm_a.ChangeDutyCycle(velLin)
            pwm_b.ChangeDutyCycle(velLin)
        elif key.char == 's':
            Reversa()
            pwm_a.ChangeDutyCycle(velLin)
            pwm_b.ChangeDutyCycle(velLin)
        # elif key.char == 'a':
        #     move_msg.angular.z = velAng
        # elif key.char == 'd':
        #     move_msg.angular.z = -velAng
        else:
            pwm_a.ChangeDutyCycle(0)
            pwm_b.ChangeDutyCycle(0)

    except:
        pass

def on_release(key):
    try:
        if key.char == 'w' or key.char == 's':
            move_msg.linear.x = 0
        elif key.char == 'a' or key.char == 'd':
            move_msg.angular.z = 0

    except:
        pass
listener = kb.Listener(
            on_press=on_press,
            on_release=on_release)






def move():
    cmd_vel_pub = rospy.Publisher('/robot_cmdVel', Twist, queue_size=10)
    rospy.Rate(100)

    while not rospy.is_shutdown():
        cmd_vel_pub.publish(move_msg)



if __name__ == '__main__':

    #rospy.init_node('robot_teleop', anonymous=True)
    #recorridos = []
    velLin = float(input('Ingrese la velociadad lineal deseada: '))
    velAng = float(input('Ingrese la velociadad angular deseada: '))

    listener.start()
    move()
