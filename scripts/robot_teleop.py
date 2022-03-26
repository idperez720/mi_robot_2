#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from pynput import keyboard as kb
import os

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

def on_press(key):
    #print(move)
    try:
        if key.char == 'w':

            move_msg.linear.x = velLin
            move_str = "\n" + str(move_msg.linear.x) + "," + str(move_msg.linear.y) + "," + str(move_msg.linear.z) + "," + str(move_msg.angular.x) + "," + str(move_msg.angular.y) + "," + str(move_msg.angular.z)
            f.write(move_str)
        elif key.char == 's':
            move_msg.linear.x = -velLin
            move_str = "\n" + str(move_msg.linear.x) + "," + str(move_msg.linear.y) + "," + str(move_msg.linear.z) + "," + str(move_msg.angular.x) + "," + str(move_msg.angular.y) + "," + str(move_msg.angular.z)
            f.write(move_str)
        elif key.char == 'a':
            move_msg.angular.z = velAng
            move_str = "\n" + str(move_msg.linear.x) + "," + str(move_msg.linear.y) + "," + str(move_msg.linear.z) + "," + str(move_msg.angular.x) + "," + str(move_msg.angular.y) + "," + str(move_msg.angular.z)
            f.write(move_str)
        elif key.char == 'd':
            move_msg.angular.z = -velAng
            move_str = "\n" + str(move_msg.linear.x) + "," + str(move_msg.linear.y) + "," + str(move_msg.linear.z) + "," + str(move_msg.angular.x) + "," + str(move_msg.angular.y) + "," + str(move_msg.angular.z)
            f.write(move_str)
        else:
            move_msg.linear.x = 0
            move_msg.angular.z = 0
            move_str = "\n" + str(move_msg.linear.x) + "," + str(move_msg.linear.y) + "," + str(move_msg.linear.z) + "," + str(move_msg.angular.x) + "," + str(move_msg.angular.y) + "," + str(move_msg.angular.z)
            f.write(move_str)
        if key.char == 'h':
            f.close()
            print('Recorrido guardado como: ' + name + '.txt')
            #listener.stop()

    except:
        pass

def on_release(key):
    try:
        if key.char == 'w' or key.char == 's':
            move_msg.linear.x = 0
            move_str = "\n" + str(move_msg.linear.x) + "," + str(move_msg.linear.y) + "," + str(move_msg.linear.z) + "," + str(move_msg.angular.x) + "," + str(move_msg.angular.y) + "," + str(move_msg.angular.z)
            f.write(move_str)
        elif key.char == 'a' or key.char == 'd':
            move_msg.angular.z = 0
            move_str = "\n" + str(move_msg.linear.x) + "," + str(move_msg.linear.y) + "," + str(move_msg.linear.z) + "," + str(move_msg.angular.x) + "," + str(move_msg.angular.y) + "," + str(move_msg.angular.z)
            f.write(move_str)

    except:
        pass
listener = kb.Listener(
            on_press=on_press,
            on_release=on_release)

def move():
    cmd_vel_pub = rospy.Publisher('/robot_cmdVel', Twist, queue_size=10)
    rospy.Rate(10)

    while not rospy.is_shutdown():
        cmd_vel_pub.publish(move_msg)



if __name__ == '__main__':

    rospy.init_node('robot_teleop', anonymous=True)
    recorridos = []
    velLin = float(input('Ingrese la velociadad lineal deseada: '))
    velAng = float(input('Ingrese la velociadad angular deseada: '))

    con=input('Desea guardar el recorrido? y/n \n')


    if(con=="y"):
        name = input('Ingrese nombre del archivo \n')
        path = os.path.join(directory, name)
        f = open(path + ".txt","a")
        #recorridos.append(name1 + '.txt')
        print('Presione h para guardar el recorrido ')
    listener.start()
    move()
