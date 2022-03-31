#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
import numpy as np

global Vr #Velocidad lineal rueda derecha
global Vl #Velocidad lineal rueda izquierda
global l #Distancia entre las ruedas
global r #Radio de las ruedas
global x  #Posicion en x
global y #Posicion en y
global theta #angulo
global position

position = Twist()

position.linear.x = 0
position.linear.y = 0

x = [0]
y = [0]
theta = [0]

Vr = 0
Vl = 0
l = 10 #cm
r = 2 #cm


def getPos(x,y,theta,Vr,Vl):
    dt = 0.1
    tiempo = 0.1

    for i in np.arange(0,tiempo,dt):
        x.append( x[-1] + 0.5* (Vr+Vl) * np.cos(theta[-1]) * dt )
        y.append( y[-1] + 0.5* (Vr+Vl) * np.sin(theta[-1]) * dt )
        theta.append( theta[-1] + (1/l) * (Vr-Vl) * dt ) 
        [x[-1],y[-1],theta[-1]]
    return [x[-1],y[-1],theta[-1]]


def callback_move(data):
    global x
    global y
    global theta
    global position

    velLin = data.linear.x
    velAng = data.angular.z
    if velLin < 0:
        getPos(x, y, theta, -velLin, -velLin)
        orientation = theta[-1]
        position.linear.x = x[-1]
        position.linear.y = y[-1]
        pub_orientation.publish(orientation)
        pub_position.publish(position)

    elif velLin > 0:
        getPos(x, y, theta, velLin, velLin)
        orientation = theta[-1]
        position.linear.x = x[-1]
        position.linear.y = y[-1]
        pub_orientation.publish(orientation)
        pub_position.publish(position)
    
    elif velAng < 0:
        getPos(x, y, theta, -velAng, velAng)
        orientation = theta[-1]
        position.linear.x = x[-1]
        position.linear.y = y[-1]
        pub_orientation.publish(orientation)
        pub_position.publish(position)

    elif velAng > 0:
        getPos(x, y, theta, -velAng, velAng)
        orientation = theta[-1]
        position.linear.x = x[-1]
        position.linear.y = y[-1]
        pub_orientation.publish(orientation)
        pub_position.publish(position)

def listener():
    global pub_orientation
    global pub_position
    rospy.init_node('robot_listener', anonymous=True)
    rospy.Subscriber('/robot_cmdVel', Twist, callback_move)
    pub_position = rospy.Publisher('/robot_position', Twist, queue_size=10)
    pub_orientation = rospy.Publisher('/robot_orientation', Float32, queue_size=10)
    rospy.spin()

if __name__ == '__main__':
    listener()