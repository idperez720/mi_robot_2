#!/usr/bin/env python3
import rospy
import keyboard
from geometry_msgs.msg import Twist
import os


## Variables
global msg
global velLin
global velAng
global VelAngMax
global VelLinMax

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
def key_press(key):
    global msg
    global velLin
    global velAng
    global name

    if key.event_type == "down":
        if key.name == "w":
            msg.linear.x = velLin
            move_str = "\n" + str(msg.linear.x) + "," + str(msg.linear.y) + "," + str(msg.linear.z) + "," + str(msg.angular.x) + "," + str(msg.angular.y) + "," + str(msg.angular.z)
            try:
                f.write(move_str)  
            except:
                pass          
        elif key.name == "s":
            msg.linear.x = -1*velLin
            move_str = "\n" + str(msg.linear.x) + "," + str(msg.linear.y) + "," + str(msg.linear.z) + "," + str(msg.angular.x) + "," + str(msg.angular.y) + "," + str(msg.angular.z)
            try:
                f.write(move_str)  
            except:
                pass   
        elif key.name == "a":
            msg.angular.z = velAng
            move_str = "\n" + str(msg.linear.x) + "," + str(msg.linear.y) + "," + str(msg.linear.z) + "," + str(msg.angular.x) + "," + str(msg.angular.y) + "," + str(msg.angular.z)
            try:
                f.write(move_str)  
            except:
                pass     
        elif key.name == "d":
            msg.angular.z = -1*velAng
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