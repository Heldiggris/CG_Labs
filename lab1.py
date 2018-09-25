# Построение графика функции
# Потенко Максим М8О-307Б
# Функция r = a * (1 - cos(phi))

import cv2
import numpy as np
import math
from tkinter import *
from PIL import ImageTk, Image
import os


# Отбеливание изображения
def white_img(img):
    h, w, d = img.shape
    for i in range(h):
        for j in range(w):
            img[i, j] = 255

# Рисование координатной оси, при максимальном отклонении max_value
def coordinate_axes(img, max_value):
    if(max_value < 1):
        max_value = 1
    h, w, d = img.shape
    font = cv2.FONT_HERSHEY_SIMPLEX

    wb_line = max(w // 130, 1)
    wl_line = max(w // 250, 1)

    w_text = w / 2000 / max(math.log10(max_value) * 0.35 , 1)

# Горизонтальная линия
    cv2.line(img,(int(w * 0.1) ,h // 2),(int(w * 0.9), h // 2),(0,0,0), wb_line)
# Вертикальная линия
    cv2.line(img,(w // 2, int(h * 0.1)),(w // 2, int(h * 0.9)),(0,0,0),wb_line)

# Стрелочка на оси Ox
    cv2.line(img,(int(w * 0.9), h // 2),(int(w * 0.87), int(h / 2.05) ),(0,0,0), wb_line)
    cv2.line(img,(int(w * 0.9), h // 2),(int(w * 0.87), int(h / 1.95) ),(0,0,0), wb_line)

# Стрелочка на оси Oy
    cv2.line(img, (w // 2, int(h * 0.1)),(int(w / 2.05), int(h * 0.13)), (0,0,0), wl_line)
    cv2.line(img, (w // 2, int(h * 0.1)),(int(w / 1.95), int(h * 0.13)), (0,0,0), wl_line)

# Начало координат
    cv2.putText(img,"0",(int(w / 1.97), int(h / 1.92)), font, w_text,(100,100,100),1,cv2.LINE_AA)

# Разметка по горизонтальной оси
    for i in range(10):
        cv2.line(img,(w // 2 - i * w // 25, int(h / 2.03)),(w // 2 - i * w // 25, int(h / 1.97)),(0,0,0), wl_line)
        cv2.line(img,(w // 2 + i * w // 25, int(h / 2.03)),(w // 2 + i * w // 25, int(h / 1.97)),(0,0,0), wl_line)

        if (i != 0):
            if(max_value < 50):
                s1 = str(round(i * max_value / 10, 1))
                s2 = str(round(-i * max_value / 10, 1))
            else:
                s1 = str(int(i * max_value // 10))
                s2 = str(int(-i * max_value // 10))
            cv2.putText(img,s1,(w // 2 + i * w // 25, int(h / 1.92)), font, w_text,(100,100,100),1,cv2.LINE_AA)
            cv2.putText(img,s2,(w // 2 - i * w // 25, int(h / 1.92)), font, w_text,(100,100,100),1,cv2.LINE_AA)

# Разметка по вертикальной оси
    for i in range(10):
        cv2.line(img, (int(w / 2.03), h // 2 - i * h // 25),(int(w / 1.97), h // 2 - i * h // 25),(0,0,0), wl_line)
        cv2.line(img, (int(w / 2.03), h // 2 + i * h // 25),(int(w / 1.97), h // 2 + i * h // 25),(0,0,0), wl_line)

        if (i != 0):
            if(max_value < 50):
                s1 = str(round(i * max_value / 10, 1))
                s2 = str(round(-i * max_value / 10, 1))
            else:
                s1 = str(int(i * max_value // 10))
                s2 = str(int(-i * max_value // 10))
            cv2.putText(img,s1,(int(w / 1.97), h // 2 + i * h // 25), font, w_text,(100,100,100),1,cv2.LINE_AA)
            cv2.putText(img,s2,(int(w / 1.95), h // 2 - i * h // 25), font, w_text,(100,100,100),1,cv2.LINE_AA)

# Реакция на кнопку - построение графика
def button_ev():
    global img
    st = text_box.get()
    if(len(st) > 0):
# Проверяем что введено число
        try:
            a = float(st)
        except:
            return
# Пустое черное изображение
        image = np.zeros((height,width,3), np.uint8)

# Отбеливаем
        white_img(image)

        points = []
        max_val = -math.inf
# Вычисляем все точки и находим максимальное отклонение
        for i in range(-314159, 314159 + 1, 10):
            r = a * (1 - math.cos(i / 100000))
            # print(r)
            y = math.sin(i / 100000) * r
            x = math.cos(i / 100000) * r
            if(abs(x) > max_val):
                max_val = abs(x)
            if(abs(y) > max_val):
                max_val = abs(y)
            points.append((x, y))
# Координатная ось
        coordinate_axes(image, max_val)
# Рисуем точки
        for i in points:
            x = i[0]
            y = i[1]

            if(max_val < 50):
                s = round(max_val / 10, 1)
            else:
                s = max_val // 10

            if(s != 0):
                cv2.circle(image,((width // 2) + int(x / s * (width // 25)), height // 2 + int(y / s * (width // 25))), 5, (0,0,255), -1)
            else:
                cv2.circle(image, ((width // 2), (height // 2)), 5,(0,0,255), -1)
        
# Трансляция изображения из OpenCV в PIL
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        img = Image.fromarray(image)
        img = ImageTk.PhotoImage(img)

# Меняем изображение
        label.configure(image=img)




# Отклик на движение ползунка
def scroll_event(event):
    canvas.configure(scrollregion=canvas.bbox("all"), width=root.winfo_width(),height=root.winfo_height())



if __name__ == "__main__":
# Размер окна
    height = 900
    width  = 900

    img = ""

# Создаем окно и даём имя
    root=Tk()
    root.title("График")

# Даем минимальный и максимальный размер окон, присваеваем стандартный размер
    root.minsize(600,600)
    root.maxsize(1800,1000)
    root.wm_geometry("%dx%d+%d+%d" % (width, height, 0, 0))

# Поле для изображения
    canvas=Canvas(root)
    canvas.place(x=0,y=0)
    frame=Frame(canvas)

# Создаем ползунки
    myscrollbar=Scrollbar(root,orient="vertical",command=canvas.yview)
    myscrollbar2=Scrollbar(root,orient="horizontal",command=canvas.xview)
    canvas.configure(yscrollcommand=myscrollbar.set, xscrollcommand=myscrollbar2.set, width=root.winfo_width(),height=root.winfo_height())
    myscrollbar.pack(side="right",fill="y")
    myscrollbar2.pack(side="bottom",fill="x")
    canvas.create_window((0,0),window=frame,anchor='nw')

# Создаём кнопки
    but = Button(root, text="График", background="#555", foreground="#ccc", padx="20", pady="8", font="16", command=button_ev)
    but.place(x=0,y=0)
    root.update()
    tex = Text(root, state=DISABLED)
# Текстовая подпись
    tex.config(state=NORMAL, font="16", height=3, width=36)
    tex.insert(END, 'График:r = a * (1 - sin(phi))\nВведите параметр a')
    # tex.pack()
    tex.place(x = 0,y= but.winfo_height())
# Поле для ввода текста
    text_box = Entry(root, bd =8,width=20, font="16", background="#555", foreground="#ccc")
    text_box.place(x = but.winfo_width(), y=0)

# Ожидание события
    root.bind("<Configure>",scroll_event)

# Отображаем изображение
    label = Label(frame, width=width, height=height)
    label.pack()
# Запускаем окно
    root.mainloop()
