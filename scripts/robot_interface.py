#!/usr/bin/env python3
import rospy
import numpy as np
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl
import math
import matplotlib.patches as patches
import tkinter as Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

trackX = [] 
trackY = []
trackZ = []
angle = []

def callback_pose(data):

    turtle_pos_x = np.round(data.linear.x, 3)
    turtle_pos_y = np.round(data.linear.y, 3)
    turtle_pos_z = np.round(data.angular.z, 3)

    trackX.append(turtle_pos_x)
    trackY.append(turtle_pos_y)
    trackZ.append(turtle_pos_z)
    pos_array = [turtle_pos_x, turtle_pos_y, turtle_pos_z]
    #print('angulo: ', pos_array)

def callback_orientation(data):
    angle.append(np.round(float(data.data), 2))
    #print(angle)

def save_plot():
    title = title_input.get()
    fig.suptitle(title)
    plt.savefig(title + '.png')
    fig.suptitle('')


def animate(i, trackX, trackY):
    # Draw x and y lists
    ax.clear()
    rect = patches.Rectangle((2.3, -2.3), -4.6, 4.6, linewidth=1)
    ax.add_patch(rect)
    ax.scatter([-2.3, -2.3, 2.3, 2.3],[2.3, -2.3, -2.3, 2.3])
    ax.plot(trackX[-1], trackY[-1], color='w', marker='*')
    ax.plot(trackX, trackY, color='w')

if __name__ == '__main__':
    # crea el nodo
    rospy.init_node('robot_interface', anonymous=True)
    rospy.Subscriber('/robot_position', Twist, callback_pose)
    rospy.Subscriber('/robot_orientation', Float32, callback_orientation)
    rospy.Rate(60)
    
    fig = plt.figure(figsize=(5,5))
    root = Tk.Tk()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(column=0,row=1)
    
    ax = fig.add_subplot(1, 1, 1)
    # Format plot
    ax.set_xlim([-2.3, 2.3])
    ax.set_ylim([-2.3, 2.3])

    title_input = Tk.Entry(master=root,
                            width=30,
                            font='Arial 20')
    title_input.place(x=150,y=50)
    save_btn = Tk.Button(master = root,
                        height=2,
                        width=10,
                        command=save_plot,
                        text='Save')
    save_btn.place(x=650, y=50)
    
    # Set up plot to call animate() function periodically
    ani = animation.FuncAnimation(fig, animate, fargs=(trackX, trackY), interval=0)

    Tk.mainloop()
    
