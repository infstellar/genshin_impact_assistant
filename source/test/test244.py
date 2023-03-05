from pynput.keyboard import Listener, KeyCode

def show(key):
    if key == KeyCode.from_char('s'):
        print('You pressed s')
    else:
        print('You pressed something else')

with Listener(on_press=show) as listener:
    listener.join()