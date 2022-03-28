#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
import os
#from mi_robot_2 import player
move_msg = Twist()
velLin = 10
velAng = 10

move_msg.linear.x = 0
move_msg.linear.y = 0
move_msg.linear.z = 0
move_msg.angular.x = 0
move_msg.angular.y = 0
move_msg.angular.z = 0

directory = os.path.dirname(__file__)

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

            rate.sleep()
        except:
            pass

if __name__ == '__main__':

    rospy.init_node('robot_player', anonymous=True)
    rate = rospy.Rate(25)
    cmd_vel_pub = rospy.Publisher('/robot_cmdVel', Twist, queue_size=10)
    path = os.path.join(directory, "results", "recorridos")
    file_list = os.listdir(path)
    files = []
    print('Archivos disponibles:')
    for file in file_list:
        if file.endswith('.txt'):
            print(file)
    text = input('Ingrese nombre del archivo (NO INCLUIR .txt): ')
    move(str(text + '.txt'))
