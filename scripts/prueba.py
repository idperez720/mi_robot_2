#!/usr/bin/env python3
from glob import glob
import rospy
import keyboard
from std_msgs.msg import String
from geometry_msgs.msg import Twist

# global msg
# global velLin
# global velAng
# msg = "0"
# velLin = 0
# velAng = 0

global msg
global velLin
global velAng

msg = Twist()
velLin = 0
velAng = 0

msg.linear.x = 0
msg.linear.y = 0
msg.linear.z = 0
msg.angular.x = 0
msg.angular.y = 0
msg.angular.z = 0

def key_press(key):
    global msg
    global velLin
    global velAng

    if key.event_type == "down":
        if key.name == "w":
            msg.linear.x = velLin
        elif key.name == "s":
            msg.linear.x = -1*velLin
        elif key.name == "a":
            msg.angular.z = velAng
        elif key.name == "d":
            msg.angular.z = -1*velAng

    elif key.event_type == "up":
        if key.name == "w":
            msg.linear.x = 0
        elif key.name == "s":
            msg.linear.x = 0
        elif key.name == "a":
            msg.angular.z = 0
        elif key.name == "d":
            msg.angular.z = 0

def talker():
    global velLin
    global velAng
    velLin = int(input('Ingrese la velociadad lineal deseada: '))
    velAng = int(input('Ingrese la velociadad angular deseada: '))
    pub = rospy.Publisher('/robot_cmdVel', Twist, queue_size=10)
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