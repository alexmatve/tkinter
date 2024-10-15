from tkinter import *
import math

root = Tk()
c = Canvas(root, width=600, height=600, bg="white")
c.pack()

x_center = 300
y_center = 300
ball_rad = 200
dot_rad = 10
speed = 2
direction = 1

ball = c.create_oval(200, 200, 400, 400, fill='blue')

point = c.create_oval(-dot_rad, -dot_rad, +dot_rad, +dot_rad, fill="green")


def update_point_position(angle=0):
    x = x_center + ball_rad * math.cos(math.radians(angle)) // 2
    y = x_center + ball_rad * math.sin(math.radians(angle)) // 2
    c.coords(point, x - dot_rad, y - dot_rad, x + dot_rad, y + dot_rad)
    angle += speed * direction
    if angle >= 360:
        angle = 0
    root.after(50, update_point_position, angle)


def plus_speed():
    global speed
    speed += 1


def minus_speed():
    global speed
    speed -= 1


def change_direction():
    global direction
    direction *= -1


def update_speed(value):
    global speed
    speed = float(value)


speed_slider = Scale(root, length=300, from_=-10, to=10, orient="horizontal", label="Задать скорость", resolution=1, command=update_speed)
speed_slider.pack()


speed_increase_button = Button(root, text="Быстрее", command=plus_speed)
speed_increase_button.pack()
speed_decrease_button = Button(root, text="Медленнее", command=minus_speed)
speed_decrease_button.pack()


direction_button = Button(root, text="Изменить направление", command=change_direction)
direction_button.pack()


update_point_position()

root.mainloop()
