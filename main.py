from multiprocessing import Process, Pipe, freeze_support
import pyautogui
import keyboard
import easygui
import random
import os

def pause_button(conn2):
    while True:
        pyautogui.sleep(0.5)
        # Stop Shortcut
        if keyboard.read_key() == "s":
            conn2.send("close")
            break

        # Pause Shortcut
        elif keyboard.read_key() == "p":
            conn2.send("pause")
            pyautogui.alert("Autoclicker Paused,Click 'p' Again to resume")

            while True:
                pyautogui.sleep(0.5)
                if keyboard.read_key() == "p":
                    conn2.send("resume")
                    pyautogui.alert("Autoclicker Resumed")
                    break
def pause_checker():
    if conn1.poll(0):
        text = conn1.recv()

        if text == "pause":
            while True:
                pyautogui.sleep(0.25)

                if conn1.poll(0):
                    text = conn1.recv()

                    if text == "resume":
                        break

        elif text == "close":
            return 1
def click(_x, _y, _action, _timer):



    # Move the mouse at location if it isnt nothing
    if _x.islower() != "none" and _y.islower() != "none":

        if "img(" in _x.lower():

            _x = _x.replace("img('", "")
            _x = _x.replace("')", "")
            _x.lower()
            _x.strip()

            try:
                _x, _y = pyautogui.locateCenterOnScreen(_x, confidence=0.9)
            except:pass

        elif "imgwait(" in _x.lower():

            _x = _x.replace("imgwait('", "")
            _x = _x.replace("')", "")
            _x.lower()
            _x.strip()

            while True:
                pyautogui.sleep(0.3)
                try:
                    _x, _y = pyautogui.locateCenterOnScreen(_x, confidence=0.9)
                except:pass
                if _x is not None and _y is not None:
                    break



        else:
            #If 'x' need to be randomised
            if "r(" in _x:
                _x = _x.replace("r(", "")
                _x = _x.replace(")", "")
                _x1, _x2 = _x.split("-")
                _x = random.randint(int(_x1), int(_x2))

            # If 'y' need to be randomised
            if "r(" in _y:
                _y = _y.replace("r(", "")
                _y = _y.replace(")", "")
                _y1, _y2 = _y.split("-")
                _y = random.randint(int(_y1), int(_y2))

        pyautogui.moveTo(int(_x), int(_y))

    #If the action isnt nothing
    if _action.islower() != "none":

        #we format the infos
        _action = _action.strip()
        _action = _action.lower()

        #If the action is left click
        if _action == "lclick":
            pyautogui.click()

        # If the action is right click
        elif _action == "rclick":
            pyautogui.click(button='right')



    #If the timer isnt nothing
    if _timer.islower() != "none":

        # If 'timer' need to be randomised
        if "r(" in _timer:
            _timer = _timer.replace("r(", "")
            _timer = _timer.replace(")", "")
            _timer1, _timer2 = _timer.split("-")
            _timer = random.uniform(float(_timer1), float(_timer2))

        pyautogui.sleep(float(_timer))
if __name__ == '__main__':
    freeze_support()
    pyautogui.FailSafeException = False


    #System loop
    while True:

        #Generate the first textbox
        input1 = int(easygui.enterbox("How many Clicks??   (Only type numbers)", "Rel_Auto_Clicker", "2"))

        #If input1 is true, we start the GUI
        if input1:

            # Starting Multi-Threading
            conn1, conn2 = Pipe()
            c = Process(target=pause_button, args=(conn2,))
            c.start()

            list = []
            _list = []

            # Generate textbox
            for i in range(input1):
                list += ["#" + str(i+1)]

            #Reload last save
            if os.path.isfile("config.txt"):
                with open("config.txt", "r") as file:
                    for lines in file.readlines():
                        _list.append(lines)


            #Generate the multibox
            input2 = easygui.multenterbox("Type your mouse locations & behavior for each step\n\nFormula is:    Left_position, Right_position, Behavior, Pause(second)\n\nexample:        x, y, lclick, 0.5\nexample:        200, 400, rclick, 2\nexample:        200, 400, None, 10\nexample:        r(200-210), r(400-450), lclick, r(5-10)\nexample:        img('config.png'), None, lclick, r(5-10)\nexample:        img('c:\img\picture.png'), None, lclick, r(5-10)\nexample:        imglock('c:\img\picture.png'), None, lclick, r(5-10)", "Rel_Auto_Clicker", list, _list)
            if input2:


                #Autosave 'config.txt'
                _list = []

                # Read
                for i in range(input1):
                    # Save before loop
                    with open("config.txt", "w+") as file:
                        for line in input2:
                            file.write(line + "\n")

                pyautogui.alert("Click 's' to stop\nClick 'p' to pause")
                #Pre-start pause
                pyautogui.sleep(3)

            #The click loop
                while pause_checker() != 1:

                    for x in input2:

                        _x, _y, _action, _timer = x.split(",")

                        # _x = left position
                        # _y = right position
                        # _action = behavior
                        # _timer = pause after click

                        #Sending infos for each step to click function
                        click(_x, _y, _action, _timer)

                    #If key stop is pressed:
            else: break
        else: break
