
import keyboard
import inputs
import threading
from time import sleep

learned_x_min = -1.0
learned_x_max = 1.0
learned_y_min = -1.0
learned_y_max = 1.0

last_x = 0.0
last_y = 0.0

running = True

SEND_FRAME_MS = 100
SEND_FRAME_SEC = SEND_FRAME_MS / 1000.0

DEADZONE = 0.1

def aggregate_inputs(event):
    global learned_x_min, learned_x_max, learned_y_min, learned_y_max, last_x, last_y
    match event.code:
        case "ABS_RX" if event.state < 0.0:
            learned_x_min = event.state if event.state < learned_x_min else learned_x_min
            last_x = -event.state / learned_x_min
        case "ABS_RX" if event.state >= 0.0:
            learned_x_max = event.state if event.state > learned_x_max else learned_x_max
            last_x = event.state / learned_x_max
        case "ABS_RY" if event.state < 0.0:
            learned_y_min = event.state if event.state < learned_y_min else learned_y_min
            last_y = -event.state / learned_y_min
        case "ABS_RY" if event.state >= 0.0:
            learned_y_max = event.state if event.state > learned_y_max else learned_y_max
            last_y = event.state / learned_y_max

def read_controller():
    while running:
        events = inputs.get_gamepad()
        for event in events:
            aggregate_inputs(event)
            # print(event.ev_type, event.code, event.state)

def send_frame_keypresses():

    budget = SEND_FRAME_SEC
    consumed = 0.0

    xy_sum = abs(last_x) + abs(last_y)
    xr = 0.0
    yr = 0.0
    if xy_sum > DEADZONE:
        xr = last_x / xy_sum
        yr = last_y / xy_sum

    # print("({:.2f}, {:.2f})".format(xr, yr))

    if xr > DEADZONE:
        keyboard.press("right")
        sleep(abs(xr) * SEND_FRAME_SEC)
        consumed += abs(xr) * SEND_FRAME_SEC
        # print("right for {:0.2f}".format(abs(xr) * SEND_RATE_SEC))
        keyboard.release("right")
    elif xr < -DEADZONE:
        keyboard.press("left")
        sleep(abs(xr) * SEND_FRAME_SEC)
        consumed += abs(xr) * SEND_FRAME_SEC
        # print("left for {:0.2f}".format(abs(xr) * SEND_RATE_SEC))
        keyboard.release("left")
    
    if yr > DEADZONE:
        keyboard.press("up")
        sleep(abs(yr) * SEND_FRAME_SEC)
        consumed += abs(yr) * SEND_FRAME_SEC
        # print("up for {:0.2f}".format(abs(yr) * SEND_RATE_SEC))
        keyboard.release("up")
    elif yr < -DEADZONE:
        keyboard.press("down")
        sleep(abs(yr) * SEND_FRAME_SEC)
        consumed += abs(yr) * SEND_FRAME_SEC
        # print("down for {:0.2f}".format(abs(yr) * SEND_RATE_SEC))
        keyboard.release("down")

    budget -= consumed
    sleep(max(budget, 0.0))
    # print("-----------")
    
def write_keyboard():
    while running:
        # sleep(SEND_RATE_MS / 1000.0)
        # print("({:.2f}, {:.2f})".format(last_x, last_y))
        send_frame_keypresses()

if __name__ == "__main__":
    threading.Thread(target=write_keyboard, name="kbd_writer").start()
    try:
        read_controller()
    except KeyboardInterrupt:
        running = False
