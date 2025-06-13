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
        button_to_press = pyautogui.locateCenterOnScreen(img, confidence=confidence)
        mouse_pos = pyautogui.position()
        button_end_point = (np.random.uniform(button_to_press[0]-10, button_to_press[0]+10), np.random.uniform(button_to_press[1]-10, button_to_press[1]+10))
        human_mouse_movement(mouse_pos, button_end_point, duration=duration)
    except pyautogui.ImageNotFoundException:
        print("Sem imagem")

def is_image_on_screen(img, confidence=0.9, grayscale=False):
    try:
        button_to_press = pyautogui.locateOnScreen(img, confidence=confidence, grayscale=grayscale)
        return True
    except pyautogui.ImageNotFoundException:
        return False

def human_click(button='left', trained=False):
    if trained:
        human_reaction_time = (0.190, 0.210)
    else:
        human_reaction_time = (0.210, 0.230)
    reaction_time = np.random.uniform(human_reaction_time[0], human_reaction_time[1])
    sleep(reaction_time)
    pydirectinput.click(button=button)


def main():
    current_path = os.getcwd()
    img_folder = os.path.join(current_path, 'images')
    cast_img = os.path.join(img_folder, f'cast.jpg')
    fish_level = "5"
    reel_img = os.path.join(img_folder, f'reel_{fish_level}.png')
    fishing_times = 0
    error = 0
    is_trained = True
    catch = False
    finish_after = 71

    try:
        move_mouse_to_image(cast_img, confidence=0.75, duration=np.random.uniform(0.6, 1.0))
        while True:
            if is_image_on_screen(cast_img, confidence=0.70):
                if not catch and fishing_times != 0:
                    print("ERRO. NÃO PEGUEI  PEIXE :(")
                    error += 1
                if fishing_times >= finish_after or error >= 3:
                    sys.exit(0)
                else:
                    print(f"doing more {finish_after - fishing_times} tries")                
                fishing_times += 1
                catch = False
                human_click()
                sleep(np.random.uniform(0.1, 0.3))

                while True:
                    if is_image_on_screen(reel_img, confidence=0.75, grayscale=True):
                        human_click(trained=is_trained)
                        while not is_image_on_screen(cast_img, confidence=0.70) and is_image_on_screen(reel_img, confidence=0.60, grayscale=True):
                            human_click(trained=is_trained)
                            sleep(np.random.uniform(0.07, 0.1))
                        catch = True
                        break
            
    except KeyboardInterrupt:
        sys.exit(0)


if __name__=="__main__":
    main()