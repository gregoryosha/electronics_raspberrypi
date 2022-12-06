import time

import controls

controls.pin_setup()

time.sleep(1)

controls.move_forward(1168, 6)

time.sleep(1)

controls.rotate_right()

time.sleep(1)

controls.move_forward(300)

time.sleep(1)

controls.cleanup()
