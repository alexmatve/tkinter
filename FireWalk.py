from tkinter import *
import math
import random
import time


# функция для преобразования цвета
def get_rgb(rgb):
    rgb = tuple(rgb)
    return "#%02x%02x%02x" % rgb


# функция, оканчивающая работу без ошибок
def end():
    global running
    running = False


MX = MY = 250
scale = 5

root = Tk()
c = Canvas(root, width=MX * scale, height=MY * scale, bg="black")  # создание холста 1000x600
root.protocol("WM_DELETE_WINDOW", end)
c.pack()

running = True

numParticle = 25  # Общее количество частиц

gravity = 0.08  # Коэффициент гравитации

# Для простоты ориентации в списке частиц, сделаем отдельные переменные для номеров ячеек отдельной частицы:
_x = 0  # номер координаты X
_y = 1  # номер координаты Y
_dirx = 2  # номер направления по X
_diry = 3  # номер направления по Y

pal = []  # Палитра для графического эффекта
# Палитра почти как для пламени, но немного больше.
for i in range(0, 64):
    pal.append([i * 4, 0, 0])
for i in range(64, 128):
    pal.append([255, i * 4 - 255, 0])
for i in range(128, 255):
    pal.append([255, 255, round((i * 4 - 128) / 4)])


# Генерация нового взрыва в указанных координатах.
# -------------------------------------------------------------------------------------------------------


class FireWork():
    def __init__(self):
        self.t = 0  # количество пройденных анимаций
        self.ovals = []  # количество пикселей, оставленных частицей, хранилице
        self.rad = 3  # размер круглых частиц
        self.col_fire = [random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)]  # выбор цвета
        self.scr = []  # Промежуточный список для хранения экрана

        # атрибуты для создания линии
        self.hor = random.randint(100, 400)
        self.x = random.randint(1, MX * scale)
        self.line = c.create_line(self.x, MY * scale, self.x, MY * scale - 40, fill='white', width=3)

        # Создаем список списков из нулей длиной MY, в итоге получится квадратная таблица из нулей MX.
        for y in range(0, MY):
            self.scr.append([0] * MX)

        self.particles = []  # Список с частицами
        for i in range(0, numParticle):  # Инициализируем список пустыми значениями
            self.particles.append([0, 0, 0, 0])

    def ready_to_boom(self):
        if self.line is not None:
            if c.coords(self.line)[1] > self.hor:
                return False
            else:
                line_coords = c.coords(self.line)
                c.delete(self.line)
                self.line = None
                self.boom(line_coords[0], line_coords[1])
        return True

    # удалять ли взрыв
    def is_existed(self):
        for i in self.ovals:
            c.delete(i)

    # анимация
    def act(self):
        if self.ready_to_boom():
            for i in range(0, numParticle):  # Перебираем все частицы
                x = round(self.particles[i][_x])
                y = round(self.particles[i][_y])

                # Изменяем координаты частицы в зависимости от скорости
                self.particles[i][_x] += self.particles[i][_dirx]
                self.particles[i][_y] += self.particles[i][_diry]

                self.particles[i][_diry] += gravity  # Применяем к скорости частицы - гравитацию

            # меняем радиус и цвет удаляющихся частиц
            self.rad += 0.01
            for i in range(len(self.col_fire)):
                self.col_fire[i] += 7 * (self.col_fire[i] <= 248)

            # генерируем круги
            for dot in self.particles:
                x = dot[_x]
                y = dot[_y]
                o = c.create_oval(x, y, x + self.rad, y + self.rad, fill=get_rgb(self.col_fire))
                self.ovals.append(o)

            # счётчик анимаций
            self.t += 1
        else:
            # передвижение снаряда вверх
            c.move(self.line, 0, -10)

    # метод нужен для расчёта новых координат для частицы
    def boom(self, x, y):
        for i in range(0, numParticle):
            self.particles[i][_x] = x  # Задаем точку, откуда взорвется салют
            self.particles[i][_y] = y
            # Генерируем случайные скорости разлета частицы в диапазоне от -3.0 до 3.0
            self.particles[i][_dirx] = random.randint(-30, 30) / 10.0
            self.particles[i][_diry] = random.randint(-30, 30) / 10.0


fireworks = [FireWork()]
start_time = time.time()


def action():
    # каждый фейерверк вылетает за определённое время
    global start_time
    if (time.time() - start_time) > 1.6:
        fireworks.append(FireWork())
        start_time = time.time()

    # проход по каждому из фейерверков
    for f in fireworks:
        f.act()
        if f.t > 30:
            fireworks.remove(f)
            f.is_existed()


def run():
    action()
    root.after(20, run)


run()

root.mainloop()
