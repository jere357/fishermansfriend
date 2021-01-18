# Stupid python path shit.
# Instead just add darknet.py to somewhere in your python path
# OK actually that might not be a great idea, idk, work in progress
# Use at your own risk. or don't, i don't care
import sys, os
sys.path.append(os.path.join(os.getcwd(),'python/'))
import numpy as np
import pdb
import time
import pyautogui
import cv2 as cv
from matplotlib import pyplot as plt

def detect_screenshot(template):
    t1= time.time()
    tempstring = 'temppic.jpg'
    pyautogui.screenshot(tempstring)
    w, h = template.shape[::-1]
    img = cv.imread(tempstring, 0)
    res = cv.matchTemplate(img, template, cv.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    top_left = min_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    """
    cv.rectangle(img,top_left, bottom_right, 255, 2)
    plt.subplot(121),plt.imshow(res,cmap = 'gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(img,cmap = 'gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.show()
    """
    bobber_loc = ((top_left[0] + bottom_right[0])/2, (top_left[1] + bottom_right[1])/2)
    pyautogui.moveTo(bobber_loc[0], bobber_loc[1])
    t2= time.time()
    #print(res)
    #print("harddisk loading/saving time : {}s".format(round(t2-t1, 4)))
    return bobber_loc

def calculate_distance(p1,p2):
    #distance is not rooted  because the pixel count is very low idk which one should be used this one works fine so i didnt bother
    #maybe if u play at a lower resolution you should consider changing it idk
    #return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    return (abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]))

if( __name__ == '__main__'):
    fish_goal = 400
    distance_sensitivity = 3 #variable for detection moment -- this depends on your resolution
    #wait just a lil bit
    time.sleep(4)
    #if youre afk for some time your character sits down and he/she cant cast fishing
    pyautogui.press("w")
    fish_counter = 0
    template = cv.imread("wcbobber.png", 0)
    while(fish_counter < fish_goal):
        time_begin = time.time()
        #begin fishing - T keybind
        print("stiscen T")
        pyautogui.press("t")
        #wait until bobber appears on screen
        time.sleep(1.4)
        r = detect_screenshot(template)
        if(len(r) == 0):
            #some mistake occured - recast fishing
            continue
        last_point = (r[0],r[1])
        #if a bobber is even found:
        if(len(r) > 0):
            #confidence = r[0][1]
            last_point = (r[0],r[1])
            #move cursor to bobber
            pyautogui.moveTo(r[0] ,r[1])
            while(True):
                distance_array = [3]
                time_current = time.time()
                current_point = (r[0],r[1])
                distance = calculate_distance(current_point, last_point)
                r = detect_screenshot(template)
                if(time_current - time_begin > 20):
                    #taking way too long, recast fishing
                    break
                if(len(r)==0):
                    break
                #print("confidence: {} kooridnate: {},{}  distance = {}".format(confidence, round(r[0][2][0],2) ,round(r[0][2][1],2), round(distance,3)))
                #bobber went into the water
                if(distance > distance_sensitivity*(sum(distance_array) / len(distance_array)) and len(distance_array) > 0):
                    #time.sleep(abs(np.random.normal(0.7,0.15)))
                    print("distance: {}, treshold: {}".format(distance, distance_sensitivity*(sum(distance_array) / len(distance_array))))
                    distance_array.append(distance)
                    time.sleep(0.3)
                    pyautogui.click(button= "right")
                    print("fish caught")
                    break
                pyautogui.moveTo(current_point)
            #it would sometime hold the right click pressed and move to at the same time (i think) and it would drag teh camera somewhere uninmportant
            #this sleep waits for the previous bobber to disappear
            time.sleep(3.2)
    #log out once youre done
    pyautogui.press("enter")
    pyautogui.hotkey("shift", "7")
    pyautogui.typewrite("/camp")
    pyautogui.press("enter")