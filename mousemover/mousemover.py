import random
import time
import threading
import mouse
import tkinter as tk
import keyboard
from mouse._mouse_event import ButtonEvent

first_movement = True
end_pos = None
autoclick_active = False
label1 = None
keyboard_event = False
activity_detected_event = threading.Event()
clicked = False
user_afk = False

######################################################################################################################################################
#TODO: CAPIRE COME FIXARE l'evento on click. C'è un bug nella libreria mouse. Forse andrebbe downgradata la versione, o controllato il github.       #
#TODO: capire come aggiungere le scritte "user afk" e "user not afk" sulla schermata. Probabilmente c'è un limite logistico al sistema implementato. #
######################################################################################################################################################

def on_click_event(e):
    global clicked
    # if isinstance(e, ButtonEvent) and e.event_type=="down":
    clicked = True

def on_release_click_event(e):
    global clicked
    if isinstance(e, ButtonEvent) and e.event_type=="up":
        clicked = False    

def handle_release(e):
    global keyboard_event
    # global pressed
    # if e.name not in keyboard._pressed_events:
    keyboard_event = False

def on_keyboard_event(event):
    global keyboard_event
    keyboard_event = True

def perform_random_actions():
    global first_movement
    global end_pos
    global start_pos  
    global user_afk
    user_afk=True
    try:
        if first_movement:   
            x_offset = random.randint(-10, 10)
            y_offset = random.randint(-10, 10)
            mouse.move(x_offset, y_offset, absolute=False, duration=0.2)
            first_movement = False
            end_pos = mouse.get_position()
        else:
            if mouse.get_position() == end_pos:
                wheretomove = start_pos
            else:
                wheretomove = end_pos

            mouse.move(wheretomove[0], wheretomove[1], duration=0.2)

        for _ in range(2):
            mouse.click('right')

        # Indicate that autoclicking is active in the mouse mover window
        #update_label_text(mouse_mover_root,label1,"User is AFK")

    except Exception as e:
        update_label_text(mouse_mover_root,label1,"Error: " + str(e) + ", please restart the program")


def check_activity(inactivity_time):
    global user_afk
    previous_mouse_position = mouse.get_position()
    previous_activity_time = time.time()
    keyboard.on_press(on_keyboard_event)
    keyboard.on_release(handle_release)
    mouse.on_click(on_click_event)
    mouse.on_right_click(on_click_event)
    mouse.hook(on_release_click_event)
    
    
    while True:
        current_mouse_position = mouse.get_position()
        mouse_moved = current_mouse_position != previous_mouse_position
        # Check if the mouse position has changed compared to the previous position
        #print(clicked)
        if mouse_moved or keyboard_event or clicked:
            if current_mouse_position != previous_mouse_position: 
                previous_mouse_position = current_mouse_position
            #if keyboard_event or clicked: update_label_text(mouse_mover_root,label1,"User is not AFK")
            previous_activity_time = time.time()

        # Check if there was any mouse activity (click or movement) by the user in the last 5 seconds
        current_time = time.time()
        elapsed_time = current_time - previous_activity_time

        if elapsed_time >= inactivity_time:
            perform_random_actions()
            # previous_mouse_position=current_mouse_position
            # current_mouse_position = mouse.get_position()
            previous_activity_time=current_time
        #elif elapsed_time < inactivity_time:
            # Indicate that the user is not AFK and no autoclicking will be performed
            #print(elapsed_time,end="\r",)
            #update_label_text(mouse_mover_root,label1,"User is not AFK")
            # Create a label for displaying status/error messages

        time.sleep(0.1)  # Add a short delay to avoid high CPU usage


# Function to update the GUI label text
def update_label_text(root,label,text):
    label.config(text=text)
    root.update()


# Function to start the mouse mover tool
def start_mouse_mover():
    global start_pos
    global mouse_mover_root
    global label1
    try:
        # Get the user input for the desired inactivity time (in seconds)
        inactivity_time = float(entry.get())

        # Hide the input window
        root.withdraw()
        start_pos=mouse.get_position()

        # Create a new window for the mouse mover tool
        mouse_mover_root = tk.Toplevel()
        mouse_mover_root.title("Mouse Mover")
        mouse_mover_root.geometry("300x100")

        # Set the window position to the bottom right corner of the screen
        screen_width = mouse_mover_root.winfo_screenwidth()
        screen_height = mouse_mover_root.winfo_screenheight()
        window_width = 200
        window_height = 50
        mouse_mover_root.geometry(f"{window_width}x{window_height}+" + str(screen_width - window_width) + "+" + str(screen_height - int(window_height*2.2)))
        mouse_mover_root.attributes("-topmost", True)
        mouse_mover_root.lift()
        # Create a label for displaying status/error messages
        #label1 = tk.Label(mouse_mover_root, text="User is not AFK")
        label1 = tk.Label(mouse_mover_root, text="tool is running!")
        label1.pack()

        # Start the thread to check for activity
        activity_thread = threading.Thread(target=check_activity, args=(inactivity_time,))
        activity_thread.start()

        # Start the main loop for the GUI event handling
        mouse_mover_root.mainloop()

    except ValueError:
        update_label_text(root,label2,"Invalid input. Please enter a valid number.")

# Create the input GUI window
root = tk.Tk()
root.title("Mouse Mover")
root.geometry("300x100")

# Add a label for instructions
instruction_label = tk.Label(root, text="Enter the desired inactivity time (in seconds):")
instruction_label.pack(pady=10)

# Add an entry widget for user input
entry = tk.Entry(root)
entry.pack()

# Add a button to start the mouse mover tool
start_button = tk.Button(root, text="Start", command=start_mouse_mover)
start_button.pack(pady=10)

# Create a label for displaying status/error messages
label2 = tk.Label(root, text="Enter the desired inactivity time and click Start.")
label2.pack()

# Start the main loop for the input GUI event handling
root.mainloop()