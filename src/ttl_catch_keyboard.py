import keyboard  # using module keyboard


def wait_for_ttl_keyboard():
    while True:  # making a loop
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.is_pressed('5'):  # if key 'q' is pressed
                print('You Pressed the Key 5!')
                break  # finishing the loop
            else:
                pass
        except:
            break  # if user pressed a key other than the given key the loop will break
    return None
