from pynput.mouse import Listener as MouseListener
#from pynput.keyboard import Listener as KeyboardListener
from pynput import keyboard
import PySimpleGUI as sg


global recording
recording = False
keys = []

def recordN():

    return
def initilizer():
    """""
    # Setup the listener threads
    keyboard_listener = KeyboardListener(on_press=on_press)
    mouse_listener = MouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    keyboard_listener.start()
    mouse_listener.start()
    keyboard_listener.join()
    mouse_listener.join()
    """""
    exitCase = 0
    til = '`'
    til = til.center(5)
    s = 's'.center(5)

    layout = [
        [sg.Text(til + ' (tilda) Start/Stop Recording')],
        [sg.Text(s + ' Enter text')],
        [sg.Button('Begin recording', key='-start-')]
    ]
    window = sg.Window('no title', layout, grab_anywhere=True, resizable=False, no_titlebar=True, size=(250, 200))

    # Collect all event until released

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == '-start-':
            print('start')
            with keyboard.Listener(on_press=on_press) as kl:
                #kl.start()
                kl.join()
                #if kl.char('b') == 'b':
                print(kl, '...stuff')

    print('out of while')
    # Start the threads and join them so the script doesn't end early

    if exitCase == 5:
        window.close()
    print('out')

def main():
    msg = 'Would you like to \ncreate a new Cursor Bot \nor run a saved bot'
    layout = [
        [sg.Text(msg, justification='c')],
        [sg.Button('New', size=(6, 1), pad=(4, 4)), sg.Button('Saved', size=(6, 1), pad=(4, 4))]
    ]
    window = sg.Window('Auto Cursor', layout, text_justification='c', element_justification='c', size=(250, 110))

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'New':
            window.close()
            namer()
        elif event == "Saved":
            window.close()

            print('saved')
    window.close()

def namer():
    badchar = ('\'\";:.,/?><\|{}()`~!@#$%^&*=');

    layout = [
        [sg.Text('Enter new script name: ', size=(17, 1), pad=(0, 0)),
         sg.Input(size=(20, 1), pad=(0, 0), key='-name-')],
        [sg.Text('', size=(25, 1), key='-errormsg-')],
        [sg.Button('Next')],
    ]
    window = sg.Window('Name Your Script', layout, text_justification='c', element_justification='c', size=(375, 90))

    while True:
        ev, val = window.read()
        if ev == sg.WINDOW_CLOSED:
            break
        if ev == 'Next':
            fname = val['-name-']
            if fname.isalnum():
                window.close()
                initilizer()
            else:
                window['-name-'].update('')
                window['-errormsg-'].update('Cannot contain special characters')


            fname = val['-name-']
            print(fname)

def on_press(key):
    global recording
    print("Key pressed: {0}".format(key))
    if key == keyboard.Key.esc:
        print('Escape was pressed... EXIT')
        return False
    try:
        k = key.char #single char key
    except:
        k = key.name #other keys
    if k == '`':
        recording = True
        print('Record starting')
    if recording == True:
        keys.append(key)
        wfile(keys)

def wfile(keys, name): #file writter
    with open((name + '.txt'), 'w') as f:
        print('placeholder')
def on_move(x, y):
    print("Mouse moved to ({0}, {1})".format(x, y))
    return x, y

def on_click(x, y, button, pressed):
    if pressed:
        print('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
    else:
        print('Mouse released at ({0}, {1}) with {2}'.format(x, y, button))
    return x, y, button

def on_scroll(x, y, dx, dy):
    print('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))
    return x, y, dx, dy




if __name__ == '__main__':
    main()

