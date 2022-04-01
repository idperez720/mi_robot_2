#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import os
from std_msgs.msg import Float32
import numpy as np


move_msg = Twist()
velLin = 10
velAng = 10

move_msg.linear.x = 0
move_msg.linear.y = 0
move_msg.linear.z = 0
move_msg.angular.x = 0
move_msg.angular.y = 0
move_msg.angular.z = 0

directory = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


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

def move(text):
    path = os.path.join(directory, "results", "recorridos", text)
    print(path)
    with open(path, 'r') as f:
        lines = f.readlines()

    linesa = []
    for n in lines:
    # print(n)
        linesa.append(n.replace("\n",""))

    #
    ruts = []
    for n in linesa:
        ruts.append(n.split(","))

    lruts = len(ruts)
    for i in range(lruts):
        try:
            move_msg.linear.x = float(ruts[i][0])
            move_msg.linear.y = float(ruts[i][1])
            move_msg.linear.z = float(ruts[i][2])
            move_msg.angular.x = float(ruts[i][3])
            move_msg.angular.y = float(ruts[i][4])
            move_msg.angular.z = float(ruts[i][5])
            cmd_vel_pub.publish(move_msg)
            velLin = move_msg.linear.x
            velAng = move_msg.angular.z
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
            rate.sleep()
        except:
            pass

def player():
    global rate
    global cmd_vel_pub
    global pub_orientation
    global pub_position
    rospy.init_node('robot_player', anonymous=True)
    rate = rospy.Rate(25)
    cmd_vel_pub = rospy.Publisher('/robot_cmdVel', Twist, queue_size=10)
    pub_position = rospy.Publisher('/robot_position', Twist, queue_size=10)
    pub_orientation = rospy.Publisher('/robot_orientation', Float32, queue_size=10)
    path = os.path.join(directory, "results", "recorridos")
    file_list = os.listdir(path)
    print('Archivos disponibles:')
    for file in file_list:
        if file.endswith('.txt'):
            print(file)
    text = input('Ingrese nombre del archivo (NO INCLUIR .txt): ')
    move(str(text + '.txt'))

if __name__ == '__main__':
    try:
        player()
    except rospy.ROSInterruptException:
        pass


