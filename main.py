import threading

from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
#from pynput import keyboard
import PySimpleGUI as sg


global recording, fname
recording = True
keys = []
log = ""

def recordN():
    """""
    with KeyboardListener(on_press=on_press) as keyboard_listener2:

        keyboard_listener2.join()

        print('running_ee')


    with MouseListener(on_click=on_click, on_scroll=on_scroll) as mouse_listener:

        mouse_listener.join()
        t = threading.Thread(target=KeyboardListener)
        m = threading.Thread(target=MouseListener)
        m.start()
        t.start()
        print('threads started')
        if not recording:
            print('not running')
            break
    """""
    keyboard_listener = KeyboardListener(on_press=on_press)
    mouse_listener = MouseListener(on_click=on_click) #, on_scroll=on_scroll
    keyboard_listener.start()
    mouse_listener.start()

    while recording:
        if recording == False:
            mouse_listener = None
            print('recording might not stop')
            return True

    print('listener stopped')

def initilizer():
    global recording
    recording = True
    clwin = False
    """""
    # Setup the listener threads
    keyboard_listener = KeyboardListener(on_press=on_press)
    mouse_listener = MouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    keyboard_listener.start()
    mouse_listener.start()
    keyboard_listener.join()
    mouse_listener.join()
    """""

    esc = '\'esc\''.center(5)

    layout = [
        [sg.Text('Drag Me Out of Your Way\nBefore You Begin Recording\nYou Wont be Able to Move Me\n'
                 'Shift+Click & Scrolling Not Suppored', justification='c')],
        [sg.Text(esc + ' Stops the Recording')],
        [sg.Button('Begin recording', key='-start-')],
        [sg.Button('Cancel', key='-cancel-')]
    ]
    window = sg.Window('no title', layout, grab_anywhere=True, element_justification='c', resizable=False, no_titlebar=True, size=(250, 180))

    while recording:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == '-start-':
            log_file()
            clwin = recordN()
        elif event ==  '-cancel-':
            window.close()

            break
        if clwin == True:
            window.close()

            break


        """"" join must join the keys then when 'popped' restarts the log ????
        with keyboard.Listener(on_press=on_press) as kl:
            
            kl.start()
            print(kl, '...stuff')
            kl.join()
            #if kl.char('b') == 'b':
        """""
    main()
    # Start the threads and join them so the script doesn't end early

def main():
    msg = 'Would you like to \ncreate a new Cursor Bot \nor run a saved bot'
    layout = [
        [sg.Text(msg, justification='c')],
        [sg.Button('New', size=(6, 1), pad=(4, 4)), sg.Button('Saved', size=(6, 1), pad=(4, 4))],
        [sg.Button('Exit', size=(6, 1), pad=(4, 4))]
    ]
    window = sg.Window('Auto Cursor', layout, text_justification='c', element_justification='c', size=(250, 140))

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'New':
            window.close()
            namer()
        elif event == "Run":
            window.close()
        elif event == "Exit":
            window.close()

            print('saved')
    window.close()

def log_file():
    f = open((fname + '.txt'), 'a')
    f.write('(U) [^_^] (U)\n')
    f.close()

def namer():
    global fname
    layout = [
        [sg.Text('Enter new script name: ', size=(17, 1), pad=(0, 0)),
         sg.Input(size=(20, 1), pad=(0, 0), key='-name-'), sg.Text('.txt')],
        [sg.Text('', size=(25, 1), key='-errormsg-')],
        [sg.Button('Next', size=(6, 1), pad=(4, 4)), sg.Button('Back', size=(6, 1), pad=(4, 4))],
    ]
    window = sg.Window('Name Your Script', layout, text_justification='c', element_justification='c', size=(375, 100))

    while True:
        ev, val = window.read()
        if ev == sg.WINDOW_CLOSED:
            break
        elif ev == 'Next':
            fname = val['-name-']
            if fname.isalnum():
                window.close()
                initilizer()
            else:
                window['-name-'].update('')
                window['-errormsg-'].update('Cannot contain special characters')
        elif ev == 'Back':
            window.close()
            main()

def on_press(key):
    global recording, log

    print(log)
    print("Key pressed: {0}".format(key))
    line_count = 0
    try:
        k = key.char #single char key
    except:
        k = str(key)
        if k == 'Key.esc':
            print('Escape was pressed... EXIT')
            recording = False
            return False
    if 'Key' in k:
        if k == 'Key.shift':
            pass
        else:
            s_ender()
            f = open((fname + '.txt'), 'a')
            f.write('[k] {}\n'.format(k))
            f.close()
    else:
        #gets last line in file
        try:
            with open((fname + '.txt'), 'r') as file:
                for last_line in file:
                    pass
        except:
            last_line = ''
            pass

        #if [s] indicating string exists the concat else start new line
        if '[s]' in last_line:
            f = open((fname + '.txt'), 'a')
            f.write('{}'.format(k))
            f.close()
        else:
            f = open((fname + '.txt'), 'a')
            f.write('[s] {}'.format(k))
            f.close()

#def on_move(x, y):
#    print("Mouse moved to ({0}, {1})".format(x, y))
 #   return x, y

def s_ender():
    try:
        with open((fname + '.txt'), 'r') as file:
            for last_line in file:
                pass
    except:
        last_line = ''
        pass
    if '[s]' in last_line:
        f = open((fname + '.txt'), 'a')
        f.write('\n')
        f.close()

def on_click(x, y, button, pressed):
    global x1, y1

    if recording == False:
        return False
    if pressed:
        print('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
        x1 = x
        y1 = y
    else:
        print('Mouse released at ({0}, {1}) with {2}'.format(x, y, button))
        s_ender()

        if x > x1 + 10 or x < x1 - 10 or y > y1 + 10 or y < y1 - 10:
            f = open((fname + '.txt'), 'a')
            f.write('[cd] {} {} {} {} {}\n'.format(str(x1), str(y1), str(x), str(y), str(button)))
            f.close()
            print('mouse dragged')
        else:
            f= open((fname + '.txt'), 'a')
            f.write('[c] {} {} {}\n'.format(str(x), str(y), str(button)))
            f.close()
            print('no drag')

    return x, y, button

"""""
def on_scroll(x, y, dx, dy):
    if recording == False:
        return False
    else:
        print('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))
        return x, y, dx, dy
""""" #for scrolling, currently not supported



if __name__ == '__main__':

    main()

