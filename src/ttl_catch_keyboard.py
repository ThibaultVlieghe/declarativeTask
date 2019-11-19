import keyboard  # using module keyboard


def wait_for_ttl_keyboard():
    while True:
        try:
            if keyboard.is_pressed('5'):
                print('You Pressed the Key 5!')
                break  # finishing the loop
            else:
                pass
        except:
            break
    return None
