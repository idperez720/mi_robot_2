#!/usr/bin/env python3
import rospy
import keyboard
from std_msgs.msg import String

global msg
global velLin
global velAng
msg = "0"
velLin = 0
velAng = 0

def key_press(key):
    global msg
    global velLin
    global velAng

    if key.event_type == "down":
        if key.name == "w":
            msg = str(velLin)
        elif key.name == "s":
            msg = str(-1*velLin)
        elif key.name == "a":
            msg = str(velAng)
        elif key.name == "d":
            msg = str(-1*velAng)

    elif key.event_type == "up":
        if key.name == "w":
            msg = "0"
        elif key.name == "s":
            msg = "0"
        elif key.name == "a":
            msg = "0"
        elif key.name == "d":
            msg = "0"

def talker():
    global velLin
    global velAng
    velLin = int(input('Ingrese la velociadad lineal deseada: '))
    velAng = int(input('Ingrese la velociadad angular deseada: '))
    pub = rospy.Publisher('/robot_cmdVel', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) #10Hz
    keyboard.hook(key_press)
    while not rospy.is_shutdown():
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass