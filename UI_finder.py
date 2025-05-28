import pydirectinput  # Only for games (DirectX, etc)
import pyautogui
import os , sys
from time import sleep
import numpy as np

pyautogui.MINIMUM_DURATION = 0
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = True

def bezier_curve(p0, p1, p2, p3, t):
    return (1-t)**3 * p0 + 3*(1-t)**2 * t * p1 + 3*(1-t) * t**2 * p2 + t**3 * p3

def human_mouse_movement(start, end, duration=1.0, steps=1000):
    p0 = np.array(start)
    p3 = np.array(end)

    distance = np.linalg.norm(p3 - p0)
    variance = distance * 0.3

    p1 = p0 + np.random.uniform(-variance, variance, size=2)
    p2 = p3 + np.random.uniform(-variance, variance, size=2)

    path = [bezier_curve(p0, p1, p2, p3, t) for t in np.linspace(0, 1, steps)]

    interval = duration / steps
    for point in path:
        pyautogui.moveTo(point[0], point[1])
        sleep(interval + np.random.uniform(-interval*0.3, interval*0.3))

def move_mouse_to_image(img, confidence=0.9, duration=1.0):
    try:
        button_to_press = pyautogui.locateOnScreen(img, confidence=confidence)
        button_center = pyautogui.center(button_to_press)
        mouse_pos = pyautogui.position()
        #if not (mouse_pos.x >= button_to_press.left and mouse_pos.x <= button_to_press.left + button_to_press.width and \
        #        mouse_pos.y >=button_to_press.top and mouse_pos.y <= button_to_press.top + button_to_press.height):
        button_end_point = [ coordinate * np.random.uniform(0.91, 1.0) for coordinate in button_center]
        human_mouse_movement(mouse_pos, button_end_point, duration=duration)
    except pyautogui.ImageNotFoundException:
        print("Sem imagem")

def is_image_on_screen(img, confidence=0.9):
    try:
        button_to_press = pyautogui.locateOnScreen(img, confidence=confidence)
        return True
    except pyautogui.ImageNotFoundException:
        return False

def human_click(button='left', trained=False):
    if trained:
        human_reaction_time = (0.190, 0.220)
    else:
        human_reaction_time = (0.210, 0.280)
    reaction_time = np.random.uniform(human_reaction_time[0], human_reaction_time[1])
    sleep(reaction_time)
    pydirectinput.click(button=button)


def main():
    current_path = os.getcwd()
    img_folder = os.path.join(current_path, 'images')
    start_fishing_img = os.path.join(img_folder, 'start_fishing.jpg')
    cast_img = os.path.join(img_folder, 'cast.jpg')
    reel_prontera_img = os.path.join(img_folder, 'reel_prontera.jpg')
    reel_morroc_img = os.path.join(img_folder, 'reel_morroc.jpg')
    reel_morroc2_img = os.path.join(img_folder, 'reel_morroc2.jpg')
    number_of_moves = 0
    is_trained = False
    catch = False
    finish_after = 73

    try:
        move_mouse_to_image(start_fishing_img, confidence=0.95, duration=np.random.uniform(0.6, 1.0))
        human_click()
        sleep(np.random.uniform(0.8, 1.7))
        move_mouse_to_image(cast_img, confidence=0.75, duration=np.random.uniform(0.6, 1.0))
        human_click()
        sleep(np.random.uniform(0.4, 0.5))
        while True:
            if is_image_on_screen(reel_prontera_img, confidence=0.75):
                human_click(trained=is_trained)
                sleep(np.random.uniform(3.0, 5.5))
                if np.random.randint(1, 100) > 80:
                    move_mouse_to_image(cast_img, confidence=0.75, duration=np.random.uniform(0.3, 0.6))
                if number_of_moves >= 3:
                    is_trained = True
                number_of_moves += 1
                if number_of_moves >= finish_after:
                    sys.exit(0)
                else:
                    print(f"missing just {finish_after - number_of_moves} tries")
                catch = True
            elif is_image_on_screen(cast_img, confidence=0.75):
                human_click()
                sleep(0.1)
                if not catch:
                    print("ERRO. NÃO PEGUEI  PEIXE :(")
                catch = False
            
    except KeyboardInterrupt:
        sys.exit(0)


if __name__=="__main__":
    main()