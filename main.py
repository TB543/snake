import os
import time
import tkinter
from tkinter import *
import random
try:
    from pynput import keyboard
except:
    imports = open("imports.bat", "w")
    imports.write("@echo off\npip install pynput")
    imports.close()
    os.system('imports.bat')
    os.remove('imports.bat')
    from pynput import keyboard


def keypress(key):
    global direction, pause

    str_key = str(key)
    if str_key == "'w'":
        if direction == 3:
            pass
        else:
            direction = 1
    elif str_key == "'a'":
        if direction == 4:
            pass
        else:
            direction = 2
    elif str_key == "'s'":
        if direction == 1:
            pass
        else:
            direction = 3
    elif str_key == "'d'":
        if direction == 2:
            pass
        else:
            direction = 4

    if str_key == "Key.esc":
        if pause == False:
            pause = True
        else:
            pause = False


def start():
    global run, size, direction, pause

    loss.score.pack_forget()
    run = True
    pause = False
    size = 2
    direction = 1
    main()


def loss():
    global run

    loss.score = Button(window, height=2, width=20, bg='green',
                        text=f"You Lost With A Length Of {size + 1}\n(still smaller than Ty's snake)\n Click To Play Again",
                        font=("Times New Roman", 60), command=lambda: start())
    main.canvas.pack_forget()
    loss.score.pack(expand=True, fill='both')
    run = False


def main():
    global direction, size, run

    x = 750
    y = 500
    red_x = 50 * random.randrange(0, game_width)
    red_y = 50 * random.randrange(0, game_height)
    while red_x == x and red_y == y:
        red_x = 50 * random.randrange(0, game_width)
        red_y = 50 * random.randrange(0, game_height)
    old_x = []
    old_y = []

    start_button.pack_forget()
    main.canvas = tkinter.Canvas(window, bg='grey', height=screen_height, width=screen_width)
    main.canvas.pack()
    listener = keyboard.Listener(on_press=keypress)
    listener.start()

    while run:

        main.canvas.create_rectangle(x, y, x + 50, y + 50, fill='green')
        main.canvas.create_rectangle(red_x, red_y, red_x + 50, red_y + 50, fill='red')
        old_x.append(x)
        old_y.append(y)

        while pause:
            try:
                for value in range(size):
                    main.canvas.create_rectangle(old_x[-value - 2], old_y[-value - 2], old_x[-value - 2] + 50,
                                                 old_y[-value - 2] + 50, fill='green')

            except:
                pass
            window.update()

        try:
            old_x.pop(-size - 2)
            old_y.pop(-size - 2)
        except:
            pass

        try:
            for value in range(size):
                main.canvas.create_rectangle(old_x[-value - 2], old_y[-value - 2], old_x[-value - 2] + 50,
                                             old_y[-value - 2] + 50, fill='green')

        except:
            pass

        window.update()
        main.canvas.delete('all')

        if x == red_x and y == red_y:
            red_x = 50 * random.randrange(0, game_width)
            red_y = 50 * random.randrange(0, game_height)
            rand = True
            while rand:
                rand = False
                for number in range(size):
                    while (red_x == old_x[-number - 2] and red_y == old_y[-number - 2]) or (red_x == x and red_y == y):
                        red_x = 50 * random.randrange(0, game_width)
                        red_y = 50 * random.randrange(0, game_height)
                        rand = True
            size += 1

        try:
            if size == len(old_x) - 1:
                for variable in range(size):
                    if x == old_x[-variable - 2] and y == old_y[-variable - 2]:
                        loss()
        except:
            pass

        if direction == 1:
            y -= 50
        elif direction == 2:
            x -= 50
        elif direction == 3:
            y += 50
        elif direction == 4:
            x += 50
        time.sleep(.1)
        if x < 0 or x > screen_width - 50 or y < 0 or y > screen_height - 50:
            loss()


screen_height = 950
screen_width = 1500
game_height = screen_height/50
game_width = screen_width/50
direction = 1
size = 2
run = True
pause = False
window = Tk()
window.title("Snake")
window.geometry("1920x1080")
window.attributes('-fullscreen', True)
window.config(cursor="none")
window.configure(bg='black')
start_button = Button(window, height=2, width=20, bg='green', text="Snake\nClick To Start",
                      font=("Times New Roman", 60), command=lambda: main())
start_button.pack(expand=True, fill='both')
window.mainloop()


# esc glitch and game crashes if food spawns in front of play before fully extended at start
