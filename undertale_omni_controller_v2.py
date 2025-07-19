
import keyboard
import inputs
import threading
from time import sleep

SEND_FRAME_MS = 100
SEND_FRAME_SEC = SEND_FRAME_MS / 1000.0

DEADZONE = 0.1

learned_x_min = -0.1
learned_x_max = 0.1
learned_y_min = -0.1
learned_y_max = 0.1

last_x = 0.0
last_y = 0.0

ratio_x = 0.0
ratio_y = 0.0

right_held = False
left_held = False
up_held = False
down_held = False

running = True

def aggregate_inputs(event):
    global learned_x_min, learned_x_max, learned_y_min, learned_y_max, last_x, \
           last_y, ratio_x, ratio_y

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
    
    xy_sum = abs(last_x) + abs(last_y)
    ratio_x = 0.0
    ratio_y = 0.0
    if xy_sum > DEADZONE:
        ratio_x = last_x / xy_sum
        ratio_y = last_y / xy_sum

def read_controller():
    while running:
        events = inputs.get_gamepad()
        for event in events:
            aggregate_inputs(event)
            # print(event.ev_type, event.code, event.state)

def send_frame_x():
    global right_held, left_held

    budget = SEND_FRAME_SEC
    consumed = 0.0

    if abs(ratio_x) > DEADZONE:
        # start holding the direction and we'll release as needed if the ratio is low enough
        if ratio_x > DEADZONE and not right_held:
            keyboard.press("right")
            right_held = True
        elif ratio_x < -DEADZONE and not left_held:
            keyboard.press("left")
            left_held = True

        # heuristic for releasing the keys
        if 0.0 <= ratio_x < 0.5 and right_held:
            keyboard.release("right")
            to_sleep = max((0.5 - abs(ratio_x)) * 2 * SEND_FRAME_SEC, 0.0)
            sleep(to_sleep)
            consumed += to_sleep
            # print(f"{to_sleep:0.2f} release right")
            keyboard.press("right")
        elif -0.5 < ratio_x < 0.0 and left_held:
            keyboard.release("left")
            to_sleep = max((0.5 - abs(ratio_x)) * 2 * SEND_FRAME_SEC, 0.0)
            sleep(to_sleep)
            consumed += to_sleep
            # print(f"{to_sleep:0.2f} release left")
            keyboard.press("left")

    else:
        if right_held:
            keyboard.release("right")
            right_held = False
        if left_held:
            keyboard.release("left")
            left_held = False

    if right_held and ratio_x < 0.0:
            keyboard.release("right")
            right_held = False

    if left_held and ratio_x > 0.0:
            keyboard.release("left")
            left_held = False


    budget -= consumed
    sleep(max(budget, 0.0))


def send_frame_y():
    global up_held, down_held

    budget = SEND_FRAME_SEC
    consumed = 0.0

    if abs(ratio_y) > DEADZONE:
        # start holding the direction and we'll release as needed if the ratio is low enough
        if ratio_y > DEADZONE and not up_held:
            keyboard.press("up")
            up_held = True
        elif ratio_y < -DEADZONE and not down_held:
            keyboard.press("down")
            down_held = True

        # heuristic for releasing the keys
        if 0.0 <= ratio_y < 0.5 and up_held:
            keyboard.release("up")
            to_sleep = max((0.5 - abs(ratio_y)) * 2 * SEND_FRAME_SEC, 0.0)
            sleep(to_sleep)
            consumed += to_sleep
            # print(f"{to_sleep:0.2f} release up")
            keyboard.press("up")
        elif -0.5 < ratio_y < 0.0 and down_held:
            keyboard.release("down")
            to_sleep = max((0.5 - abs(ratio_y)) * 2 * SEND_FRAME_SEC, 0.0)
            sleep(to_sleep)
            consumed += to_sleep
            # print(f"{to_sleep:0.2f} release down")
            keyboard.press("down")

    else:
        if up_held:
            keyboard.release("up")
            up_held = False
        if down_held:
            keyboard.release("down")
            down_held = False

    if up_held and ratio_y < 0.0:
            keyboard.release("up")
            up_held = False

    if down_held and ratio_y > 0.0:
            keyboard.release("down")
            down_held = False

    budget -= consumed
    sleep(max(budget, 0.0))


def write_keyboard_x():
    while running:
        send_frame_x()

def write_keyboard_y():
    while running:
        send_frame_y()

if __name__ == "__main__":
    threading.Thread(target=write_keyboard_x, name="kbd_writer_x").start()
    threading.Thread(target=write_keyboard_y, name="kbd_writer_y").start()
    try:
        read_controller()
    except KeyboardInterrupt:
        running = False
