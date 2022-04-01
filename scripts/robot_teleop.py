#!/usr/bin/env python3
import rospy
import keyboard
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
import os
import numpy as np

## Variables
global msg
global velLin
global velAng
global VelAngMax
global VelLinMax

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
l = 21 #cm
r = 3.4 #cm

VelAngMax = 16.8 #rad/s
VelLinMax = r*VelAngMax #cmd/s

msg = Twist()
velLin = 0
velAng = 0

msg.linear.x = 0
msg.linear.y = 0
msg.linear.z = 0
msg.angular.x = 0
msg.angular.y = 0
msg.angular.z = 0

directory = os.path.dirname(__file__)


## Funciones
def getPos(x,y,theta,Vr,Vl):
    dt = 0.1
    tiempo = 0.1

    for i in np.arange(0,tiempo,dt):
        x.append( x[-1] + 0.5* (Vr+Vl) * np.cos(theta[-1]) * dt )
        y.append( y[-1] + 0.5* (Vr+Vl) * np.sin(theta[-1]) * dt )
        theta.append( theta[-1] + (1/l) * (Vr-Vl) * dt ) 
        [x[-1],y[-1],theta[-1]]
    return [x[-1],y[-1],theta[-1]]



def key_press(key):
    global msg
    global velLin
    global velAng
    global name
    global x
    global y
    global theta
    global position

    if key.event_type == "down":
        if key.name == "w":
            msg.linear.x = velLin
            getPos(x, y, theta, velLin, velLin)
            move_str = "\n" + str(msg.linear.x) + "," + str(msg.linear.y) + "," + str(msg.linear.z) + "," + str(msg.angular.x) + "," + str(msg.angular.y) + "," + str(msg.angular.z)
            try:
                f.write(move_str)  
            except:
                pass          
        elif key.name == "s":
            msg.linear.x = -1*velLin
            getPos(x, y, theta, velLin, velLin)
            move_str = "\n" + str(msg.linear.x) + "," + str(msg.linear.y) + "," + str(msg.linear.z) + "," + str(msg.angular.x) + "," + str(msg.angular.y) + "," + str(msg.angular.z)
            try:
                f.write(move_str)  
            except:
                pass   
        elif key.name == "a":
            msg.angular.z = velAng
            getPos(x, y, theta, velAng, -velAng)
            move_str = "\n" + str(msg.linear.x) + "," + str(msg.linear.y) + "," + str(msg.linear.z) + "," + str(msg.angular.x) + "," + str(msg.angular.y) + "," + str(msg.angular.z)
            try:
                f.write(move_str)  
            except:
                pass     
        elif key.name == "d":
            msg.angular.z = -1*velAng
            getPos(x, y, theta, -velAng, velAng)
            move_str = "\n" + str(msg.linear.x) + "," + str(msg.linear.y) + "," + str(msg.linear.z) + "," + str(msg.angular.x) + "," + str(msg.angular.y) + "," + str(msg.angular.z)
            try:
                f.write(move_str)  
            except:
                pass   
        elif key.name == "h":
            try:
                f.close()
                print('Recorrido guardado como: ' + name + '.txt')
            except:
                pass
            
            


    elif key.event_type == "up":
        if key.name == "w":
            msg.linear.x = 0
            move_str = "\n" + str(msg.linear.x) + "," + str(msg.linear.y) + "," + str(msg.linear.z) + "," + str(msg.angular.x) + "," + str(msg.angular.y) + "," + str(msg.angular.z)
            try:
                f.write(move_str)  
            except:
                pass  
        elif key.name == "s":
            msg.linear.x = 0
            move_str = "\n" + str(msg.linear.x) + "," + str(msg.linear.y) + "," + str(msg.linear.z) + "," + str(msg.angular.x) + "," + str(msg.angular.y) + "," + str(msg.angular.z)
            try:
                f.write(move_str)  
            except:
                pass  
        elif key.name == "a":
            msg.angular.z = 0
            move_str = "\n" + str(msg.linear.x) + "," + str(msg.linear.y) + "," + str(msg.linear.z) + "," + str(msg.angular.x) + "," + str(msg.angular.y) + "," + str(msg.angular.z)
            try:
                f.write(move_str)  
            except:
                pass  
        elif key.name == "d":
            msg.angular.z = 0
            move_str = "\n" + str(msg.linear.x) + "," + str(msg.linear.y) + "," + str(msg.linear.z) + "," + str(msg.angular.x) + "," + str(msg.angular.y) + "," + str(msg.angular.z)
            try:
                f.write(move_str)  
            except:
                pass    


def talker():
    global velLin
    global velAng
    global f
    global pub_orientation
    global pub_position
    velLin = int(input('Ingrese la velociadad lineal deseada: '+"[0-"+str(int(VelLinMax))+"](cm/s):"))
    velAng = int(input('Ingrese la velociadad angular deseada: '+"[0-"+str(int(VelAngMax))+"](rads/s):"))
    

    ## Guardar recorido
    con=input('Desea guardar el recorrido? y/n \n')
    if(con=="y"):
        name = input('Ingrese nombre del archivo \n')
        path = os.path.join(directory, "results", "recorridos", name)
        f = open(path + ".txt","a")
        #recorridos.append(name1 + '.txt')
        print('Presione h para guardar el recorrido ')



    rospy.init_node('robot_teleop', anonymous=True)
    pub = rospy.Publisher('/robot_cmdVel', Twist, queue_size=10)
    pub_position = rospy.Publisher('/robot_position', Twist, queue_size=10)
    pub_orientation = rospy.Publisher('/robot_orientation', Float32, queue_size=10)
    rate = rospy.Rate(10) #10Hz
    keyboard.hook(key_press)
    while not rospy.is_shutdown():
        pub.publish(msg)
        orientation = theta[-1]
        position.linear.x = x[-1]
        position.linear.y = y[-1]
        pub_orientation.publish(orientation)
        pub_position.publish(position)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass