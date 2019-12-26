# Stupid python path shit.
# Instead just add darknet.py to somewhere in your python path
# OK actually that might not be a great idea, idk, work in progress
# Use at your own risk. or don't, i don't care
import sys, os
sys.path.append(os.path.join(os.getcwd(),'python/'))
import darknet as dn
import numpy as np
import pdb
import time
import pyautogui


def detect_screenshot(counter = 0):
    t1= time.time()
    tempstring = "temppic.jpg"
    pyautogui.screenshot(tempstring)
    t2= time.time()
    framepath = tempstring.encode(encoding= "UTF-8")
    r = dn.detect(net, meta, framepath, thresh= 0.3)
    t3 = time.time()
    print("harddisk loading/saving time : {}s".format(round(t2-t1, 4)))
    print("detection time: {}s".format(round(t3-t1, 4)))
    return r
def calculate_distance(p1,p2):
    #distance is not rooted  because the pixel count is very low idk which one should be used this one works fine so i didnt bother
    #maybe if u play at a lower resolution you should consider changing it idk
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

if( __name__ == '__main__'):
    fish_goal = 400
    distance_sensitivity = 3 #variable for detection moment -- this depends on your resolution
    #darknet setup
    dn.set_gpu(0)
    #it wont properly load unless you the paths are in binary :))
    net = dn.load_net(b"yolov3-bobber.cfg", b"yolov3-bobber_final.weights", 0)
    meta = dn.load_meta(b"obj.data")
    #wait just a lil bit
    time.sleep(4)
    #if youre afk for some time your character sits down and he/she cant cast fishing
    pyautogui.press("w")
    fish_counter = 0
    while(fish_counter < fish_goal):
        time_begin = time.time()
        #begin fishing - T keybind
        pyautogui.press("t")
        #wait until bobber appears on screen
        time.sleep(3)
        r = detect_screenshot()
        if(len(r) == 0):
            #some mistake occured - recast fishing
            continue
        last_point = (r[0][2][0],r[0][2][1])
        distance_array = []
        if(len(r) > 0):
            confidence = r[0][1]
            last_point = (r[0][2][0],r[0][2][1])
            #move cursor to bobber
            pyautogui.moveTo(r[0][2][0] ,r[0][2][1])
            while(True):
                time_current = time.time()
                current_point = (r[0][2][0],r[0][2][1])
                distance = calculate_distance(current_point, last_point)
                r = detect_screenshot()
                #no bobber detected - recast fishing
                if(time_current - time_begin > 40):
                    #taking way too long, recast fishing
                    break
                if(len(r)==0):
                    break
                #print("confidence: {} kooridnate: {},{}  distance = {}".format(confidence, round(r[0][2][0],2) ,round(r[0][2][1],2), round(distance,3)))
                distance_array.append(distance)
                #bobber went into the water
                if(distance > distance_sensitivity*(sum(distance_array) / len(distance_array))):
                    #time.sleep(abs(np.random.normal(0.7,0.15)))
                    time.sleep(0.5)
                    pyautogui.click(button= "right")
                    print("fish caught")
                    break
                pyautogui.moveTo(current_point)
            #it would sometime hold the right click pressed and move to at the same time (i think) and it would drag teh camera somewhere uninmportant
            time.sleep(1)
    #log out once youre done
    pyautogui.press("enter")
    pyautogui.hotkey("shift", "7")
    pyautogui.typewrite("camp")
    pyautogui.press("enter")