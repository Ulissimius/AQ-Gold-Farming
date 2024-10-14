import pyautogui
import keyboard
import time
import threading

# Things to do:
# Set up picture reading
# Make a one time initialization of focusing visit neighbor text box
# Make a one time initialization of turning on Shield Buff + Overdrive toggle
# Make a conditional to handle dying

running = False
initialRun = True
counter = 0 # recursive tracking
shieldBuff = False
overdrive = False
pcAlive = True

def farming_loop():
    global running, initialRun, shieldBuff, overdrive, pcAlive
    filePath = 'images/'
    filePathMain = filePath + '1 - main loop images/'
    filePathInitial = filePath + '2 - initializing images/'
    filePathDeath = filePath + '3 - death event images/'
    running = True
    print("Starting farming loop...")

    while running:
        # Start - Home screen: click fountain -> click Home button
        print("Home Screen")
        find_and_press(filePathMain + 'fountain.png')
        find_and_press(filePathMain + 'to_house_button.png')
        # time.sleep(1) # loading screen pause

        # My House screen: click visit neighbor -> (IR) click again to focus -> Ctrl + V -> click specific neighbor
        print('My House')
        find_and_press(filePathMain + 'visit_neighbor_button.png')
        pyautogui.click()
        pyautogui.write('45387657', interval=0.01)
        find_and_press(filePathMain + 'travel_to_neighbor_button.png')

        # Battle Screen: (IR) buff and overdrive -> click attack -> click attack/click done -> click done
        print('Battle Screen')
        while is_gog_alive(): # There will need to be a catch here to handle player death
            if not is_pc_alive():
                break
            while initialRun: # Activates important buffs/toggles for the loop
                if not is_pc_alive():
                    break
                if not overdrive:
                    find_and_press(filePathInitial + 'OT_skills_button.png')
                    find_and_press(filePathInitial + 'OT_overdrive_onslaught_toggle.png')
                    find_and_press(filePathInitial + 'OT_overdrive_onslaught_back.png')
                if not shieldBuff:
                    find_and_press(filePathInitial + 'OT_shield.png')
                if shieldBuff and overdrive:
                    initialRun = False
            find_and_press(filePathMain + 'attack_button.png', True)
        if not is_pc_alive():
            find_and_press(filePathDeath + 'next.png')
            time.sleep(2)
            find_and_press(filePathDeath + 'yes.png')
            time.sleep(0.1)
            pyautogui.click()
            time.sleep(0.1)
            pyautogui.click()
        else:
            find_and_press(filePathMain + 'results_done_button.png')
        
            # Neighbor house screen: click return to town button
            print('Neighbor\'s house')
        find_and_press(filePathMain + 'back_to_town_button.png')

def start_farming():
    global running
    if not running:  # To prevent starting multiple threads
        running = True
        thread = threading.Thread(target=farming_loop)
        thread.start()

def stop_farming():
    global running
    running = False
    print("Stopping farming loop...")

def find_and_press(path, countOverride=False):
    global counter, shieldBuff, overdrive

    # Used to shorten attack loop checks to speed up the result screen check.
    if countOverride:
        counter = 8
        print('Counter Shortened!')
    
    try:
        # Locate the image on the screen and return its coordinates
        button_location = pyautogui.locateOnScreen(path, confidence=0.9)
    except pyautogui.ImageNotFoundException:
        counter += 1
        time.sleep(0.5)
        if counter < 10:
            find_and_press(path)
        else:
            counter = 0
            return print('Image not found! Skipping action...')
    else:
        # If found, click the center of the located area
        if button_location:
            pyautogui.click(pyautogui.center(button_location))
        
        # These checks mark player buffs as active for the run.
        if path == 'images/2 - initializing images/OT_overdrive_onslaught_back.png':
            overdrive = True
        if path == 'images/2 - initializing images/OT_shield.png':
            shieldBuff = True

        counter = 0

# Checks to see if the monster is dead.
def is_gog_alive():
    try:
        pyautogui.locateOnScreen('images/1 - main loop images/hp_0.png', confidence=0.99)
    except pyautogui.ImageNotFoundException:
        print('The Shadow Gogg lives!')
        return True
    else:
        print('The Shadow Gogg is dead!')
        return False

# Checks to see if the PC has died.
def is_pc_alive():
        try:
            pyautogui.locateOnScreen('images/3 - death event images/pc_dead.png', confidence=0.99)
        except pyautogui.ImageNotFoundException:
            print('PC is alive.')
            return True
        else:
            print('Oh no, you\'ve died!')
            return False

# Set hotkeys for starting and stopping
keyboard.add_hotkey('F8', start_farming)  # Press F8 to start
keyboard.add_hotkey('F9', stop_farming)   # Press F9 to stop

# Keeps the program running, waiting for hotkey presses
print("Press F8 to start farming, F9 to stop.")
keyboard.wait('esc')  # Press Esc to exit the script completely