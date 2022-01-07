from multiprocessing import Process, Pipe, freeze_support
import pyautogui
import keyboard
import easygui
import sys

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
            c.terminate()
            pyautogui.alert("Autoclicker Exit")
            sys.exit(0)
def click(_x, _y, _action, _timer):

    # Move the mouse at location if it isnt nothing
    if _x.islower() != "none" and _y.islower() != "none":
        pyautogui.moveTo(int(_x), int(_y))

    #If the action isnt nothing
    if _action.islower() != "none":

        #we format the infos
        _action = _action.strip()
        _action = _action.lower()

        #If the action is left click
        if _action == "lclick":
            print("left click)")
            pyautogui.click()

        # If the action is right click
        elif _action == "rclick":
            print("right click")
            pyautogui.click(button='right')

    pause_checker() # we check for pause before the sleep
    #If the timer isnt nothing
    if _timer.islower() != "none":
        pyautogui.sleep(int(_timer))
    pause_checker() # we check for pause after the sleep

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    freeze_support()
    pyautogui.FailSafeException = False

    # Starting Multi-Threading
    conn1, conn2 = Pipe()
    c = Process(target=pause_button, args=(conn2,))
    c.start()

    #System loop
    while True:

        #Generate the first textbox
        input1 = int(easygui.enterbox("How many times?   (Numbers only)", "Rel_Auto_Clicker", "2"))

        #If input1 is true, we start the GUI
        if input1:

            #Make new textbox for the amount entered
            list = []
            for i in range(input1):
                list += ["Step " + str(i+1)]

            #Generate the multibox
            input2 = easygui.multenterbox("Type your mouse locations & behavior for each step\n\nFormula is:    [Left_position, Right_position, Behavior, Pause(second)]\n\nexample:        [x, y, lclick, 0.5]\nexample:        [200, 400, rclick, 2]\nexample:        [200, 400, None, 10]", "Rel_Auto_Clicker", list)
            if input2:

                pyautogui.alert("Click 's' to stop\nClick 'p' to pause")
                #Pre-start pause
                pyautogui.sleep(3)

            #The click loop
                while True:
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
