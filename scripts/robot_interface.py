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
import tkinter.font as TkFont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

trackX = [] 
trackY = []
angle = []

def callback_pose(data):

    turtle_pos_x = np.round(data.linear.x, 3)
    turtle_pos_y = np.round(data.linear.y, 3)

    trackX.append(turtle_pos_x)
    trackY.append(turtle_pos_y)
    pos_array = [turtle_pos_x, turtle_pos_y]

def callback_orientation(data):
    angle.append(np.round(float(data.data), 2))

def save_plot():
    title = title_input.get()
    fig.suptitle(title)
    plt.savefig(title + '.png')
    fig.suptitle('')


def animate(i, trackX, trackY):
    # Draw x and y lists
    ax.clear()
    if trackX: 
        ax.plot(trackX[-1], trackY[-1], color='r', marker='*')
    ax.plot(trackX, trackY, color='b')

if __name__ == '__main__':
    # crea el nodo
    rospy.init_node('robot_interface', anonymous=True)
    rospy.Subscriber('/robot_position', Twist, callback_pose)
    rospy.Subscriber('/robot_orientation', Float32, callback_orientation)
    rospy.Rate(60)
    
    fig = plt.figure(figsize=(5,5))
    root = Tk.Tk()
    root.geometry("500x700")
    root.configure(background='white')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().place(x=0, rely=0.1)

    ax = fig.add_subplot(1, 1, 1)
    # Format plot
    fontFamily = TkFont.Font(family="Arial", size=14, weight="bold", slant="italic")

    label = Tk.Label(master=root, text="Ingrese el titulo para guardar \n la grafica", foreground='black', background='white', font=fontFamily)
    label.place(x=75, y=25)


    title_input = Tk.Entry(master=root,
                            width=30,
                            font=fontFamily)
    title_input.place(x=75,rely=0.1)
    save_btn = Tk.Button(master = root,
                        height=2,
                        width=50,
                        command=save_plot,
                        text='Save')
    save_btn.place(relx=0.1, y=600)
    
    # Set up plot to call animate() function periodically
    ani = animation.FuncAnimation(fig, animate, fargs=(trackX, trackY), interval=0)

    Tk.mainloop()
    
