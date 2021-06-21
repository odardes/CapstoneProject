from tkinter import *
import pygame, config
from Car.car import *
import tkinter.messagebox as tkms
import time
import re


# Create the main window and the car
instructions_list = []
pygame_clock = pygame.time.Clock()
screen = pygame.display.set_mode(config.RESOLUTION)
car = Car(screen, 0, 0, float("inf"), 0, 0)


# Change from cm to px
def cm_to_px(cm):
    one_cm = (config.DISPLAY_WIDTH // config.ROWS) / 10
    return cm * one_cm


# Converted to how many pixels go per second instead of how many cm go per second
def cmps_to_pxps(cmps):
    one_cmps = ((config.DISPLAY_WIDTH // config.ROWS) / 10)
    if pygame_clock.get_fps() == 0:
        one_cmps *= 1 / 30
    else:
        one_cmps *= 1 / (pygame_clock.get_fps())
    return cmps * one_cmps


instructions = '''1.  You can use move(distance,time,direction) function to control the vehicle’s movements. Please give degree values to direction (ex 45,135,270 etc.).   
\n2.  You can press the reset button to restore to defaults and  start over.
\n3.  You can use repeat() function to create a while loop(Ex: repeat (3)move(20,2,135)).
'''


def reset_btn_function():
    print("Reset Button Pressed")
    set_output_text("Reset Button is Pressed")
    car.reset()


def instructions_btn_function():
    print("Instructions Button Pressed")
    tkms.showinfo(
        'Instructions', f'{instructions}',  icon='info')


def give_warning(string):
    tkms.showinfo(
        'Warning', f'{string}',  icon='error')


def execute_btn_function():
    global speed, direction, distance
    print("Execute Button Pressed")
    strings = input_box.get(1.0, "end-1c")
    print('Data: ', strings)
    loop_count = 0
    print(strings.split("\n"))
    for string in strings.split("\n"):
        if string.find('repeat')!=-1: # this will give you number of loops on i
            temp = re.findall('\\((.*?)\\)', string)
            loop_count = int(temp[0])
            print(f'Loop Value: {loop_count}')
            string = string.replace(f"repeat({loop_count})", "")
            print(string)
        else:
            loop_count = 1

        if string.find('if')!=-1 and string.find('obs_dist')!=-1 and string.find('<')!=-1:
            temp = re.findall(r'\d+', string)
            out= ''
            for i in temp:
                out+=i
            num = int(out)
            print (f"Number:{num}")
            return
        if string.find('if')!=-1 and string.find('speed')!=-1 :
            temp = re.findall(r'\d+', string)
            out= ''
            for i in temp:
                out+=i
            speed = int(out)
            print (f"Speed:{speed}")
            if string.find('<')!=-1:
                if speed < 0:
                    give_warning('Enter A valid Speed Value')

                    pass
            if string.find('>')!=-1:
                if speed > 100:
                    give_warning('Enter A valid Speed Value')
                    pass
        if string.find('move') != -1:
            data = string[string.find('('):]
            data = data.replace('(', '')
            data = data.replace(')', '')
            parameters = data.split(',')
            distance = int(parameters[0])
            speed = int(parameters[1])
            direction = int(parameters[2])
            print(f'Distance:{distance},Time:{speed},Direction:{direction}')
            with open('codesender.txt', 'r+') as f:
                f.write("(" + str(distance) + ',' + str(speed) + ',' + str(direction) + ")")
                # prints every item on a txt

        for i in range(loop_count):
            instructions_list.append([cmps_to_pxps(speed), math.radians(direction), cm_to_px(distance)])


def clock():
    hour = time.strftime("%H")
    min = time.strftime("%M")
    sec = time.strftime("%S")
    clock_label.config(text=hour+':'+min+':'+sec)
    clock_label.after(1000, clock)


t_sec = 0
t_min = 0
t_hour = 0
running = False


def reset_timer():
    global t_hour, t_min, t_sec
    t_sec = 0
    t_min = 0
    t_hour = 0


def display_timer():
    def count():
        if running:
            global t_hour, t_min, t_sec
            timer_label.config(text=str(t_hour)+':'+str(t_min)+':'+str(t_sec))
            t_sec += 1
            if t_sec == 60:
                t_sec = 0
                t_min += 1
            if t_min == 60:
                t_min = 0
                t_hour += 1
            timer_label.after(1000, count)
    count()


running = False


def stop_timer():
    global running
    running = False


def start_timer():
    global running
    running = True
    display_timer()


def set_output_text(string):
    output.configure(text=string)


######################### GUI ######################
gui = Tk()
gui.geometry('500x500')
gui.resizable(0, 0)  # cant be maximizes (fixed size)
gui.title("Toy Car")

# title
Label(gui, text='TOY CAR', font=(
    "Comic Sans MS", 24)).place(x=175, y=10)
# buttons
# #  reset btn
reset_btn = Button(gui, text='Reset', width=12,
                   command=lambda: reset_btn_function())
reset_btn.place(x=380, y=40)
# #  instructions btn
instructions_btn = Button(gui, text='Instructions',
                          width=12, command=lambda: instructions_btn_function())
instructions_btn.place(x=10, y=40)
# execute btn
execute_btn = Button(gui, text='Execute', width=12,
                     command=lambda: execute_btn_function())
execute_btn.place(x=380, y=445)
# clock
clock_label = Label(gui, text="00:00:00", font=(48))
clock_label.place(x=20, y=10)
# timer
timer_label = Label(gui, text="0:0:0", font=(48))
timer_label.place(x=400, y=10)
# text box
Label(gui, text='Enter Input Command : ', font=(
    "Helvetica", 12)).place(x=10, y=350)
# input box (scrolle able box)
input_box = Text(
    gui, font=(
        "Helvetica", 11), undo=True, height=4, width=38)
input_box.place(x=175, y=356)

# output
output = Label(gui, text='Here is you text output  message', font=(16))
# output.configure(anchor="center")
output.pack(pady=200, anchor="center")
# output.place(y = 245)


# __________________main__________
clock()  # start clock


'''
Functions You will Use:

>>  To print text in the output screen:
        set_output_text("The Car moved.") # take any string 

>>  start_timer ()   # start the timer
>>  stop_timer()    # stop the timer
>>  reset_timer()   # reset timer  to 0:0:0

>> reset_btn_function()
    use this button to reset your data that your want when reset button is pressed

>> give_warning(string)
    you can use this funtion to show warning on the screen 
'''
