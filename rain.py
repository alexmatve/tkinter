from tkinter import *
import math
from random import randint


# Функция, отвечающая за создание капли в виде линии
def create_drop():
    x = randint(1, 1000)
    y = 0
    k = randint(0, 2)
    line = c.create_line(x, y, x, y + 30, fill=colors[k], width=thickness[k])
    drops.append((line, speed[k]))


# функция, реализующая движение линий
def rain():
    for i in range(len(drops)):
        line, pace = drops[i]
        c.move(line, 0, pace)  # передвижение капель по вертикали с определённой скоростью
        if c.coords(line)[1] >= 600:  # пока верхняя координата не достигнет координаты 600 - длины Canvas
            c.delete(line)  # удаление линии
            drops.pop(i)
            create_drop()  # создание новой: таким образом цикл будет выполняться бесконечно


def update_rain():
    rain()
    root.after(50, update_rain)


root = Tk()
c = Canvas(root, width=1000, height=600, bg="MediumPurple1")  # создание холста 1000x600
c.pack()

thickness = [3, 6, 9]  # толщина капель, зависит от дальности
colors = ["SteelBlue1", "DodgerBlue3", "DodgerBlue4"]  # цвета капель, зависит от дальности
speed = [19, 23, 28]  # всевозможные скорости падения капель, зависит от дальности

drops = []  # список, содержащий капли (объекты типа c.create_line)

# создаём первые 100 капель
for _ in range(300):
    create_drop()

# запуск основной программы
update_rain()

root.mainloop()
