import uinput
from pynput.mouse import Listener, Controller as MouseController

# Create the virtual joystick device with ABS_X and its value range (0 to 255)
events = [
    uinput.ABS_X + (0, 255, 0, 0),
]
joystick = uinput.Device(events, name="Virtual Joystick")  # Add the "name" parameter to set the device name

# Calibration variables
calibrated_min = None
calibrated_max = None
joystick_min = 0  # Minimum value of the virtual joystick's X-axis
joystick_max = 255  # Maximum value of the virtual joystick's X-axis

def calibrate_mouse(x):
    # Apply mouse calibration to the virtual joystick's X-axis range
    return int((x - calibrated_min) / (calibrated_max - calibrated_min) * (joystick_max - joystick_min) + joystick_min)

def on_move(x, y):
    # Get the mouse movement value on the X-axis
    normalized_x = calibrate_mouse(x)
    # Emit the movement on the joystick's ABS_X
    joystick.emit(uinput.ABS_X, normalized_x)

def calibrate():
    global calibrated_min, calibrated_max

    # Initialize the mouse controller
    mouse = MouseController()

    # Move the mouse to the minimum position
    print("Move the mouse to the minimum position...")
    input("Press Enter when ready.")
    calibrated_min = mouse.position[0]

    # Move the mouse to the maximum position
    print("Move the mouse to the maximum position...")
    input("Press Enter when ready.")
    calibrated_max = mouse.position[0]

    print(f"Calibration completed:\nCalibrated_min: {calibrated_min}\nCalibrated_max: {calibrated_max}")

# Perform calibration before starting the mouse listener
calibrate()

# Start the listener to read mouse movement
with Listener(on_move=on_move) as listener:
    listener.join()
