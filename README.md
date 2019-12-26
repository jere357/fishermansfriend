### World of Warcraft: A Fisherman's friend
=========

This is a World of Warcraft fishing bot written in python. Im going to be blunt right in the beginning, you will probably spend a lot of time configuring this bot unless you're a programmer. The main problem with creating wow fishbots is the detection of the fishing bobber and determining the moment it goes into the water - that is the moment when you want to right click. Other python fishbots on github use openCV and awkward setup (setting low resolution, changing water quality, removing interface using alt-z). This bot "only" requires you to have darknet-yolov3 installed, and CUDA enabled which means you need to have a decent graphics card to run this bot. My GTX 1070 Ti manages to take a screenshot and run it through the darknet at ~7 fps. The OpenCV versions are unreliable in detecting the bobber - achieving ~80% accuracy even with the perfect setup. The provided darknet weights have been trained on ~150 bobber screenshots from wailing caverns which i have annotated, it detects the bobber almost perfectly. The second problem - determining the moment in which the bobber goes into the water. In the beginning my bot was also written using openCV and it worked like this. First it would locate the bobber at a certain confidence let's say 75%, then it spams screenshot all the time and when the confidence falls below  0.8*(the average confidence of last 6 frames) it would deduce that the bobber is now in the water and it would right click. The "problem" with the darknet implementation was that it would always detect the bobber with >0.99 confidence and thus the previous method stopped working. The way it works now is that it tracks the bobbers location from frame to frame and when the pixel-distance between bobbers in 2 frames is larger than distance_sensitivity * (average distance between frames up until now) it right clicks at that moment.

Requirements:
--------------
* 1. You also need CUDA to be installed and configured correctly, this can prove quite challenging, i recommend running this script (this is for ubuntu, not windows) https://www.tensorflow.org/install/gpu#install_cuda_with_apt 
* 2. You need to install darknet on your computer. I recommend you install this version: https://github.com/AlexeyAB/darknet - it supposedly has better performance than the original one, and it has the ability to train custom classes. It also comes with a handy c++ application you can use for annotating images (i used it while annotating my custom dataset)
* 3. You need to provide the path to the libdarknet.so in darknet.py at line 122, or place the project in the darknet installation folder (the one that contains the original darknet.py)
* 4. Install pyautogui, skimage (sklearn), and numpy
* 5. Download the darknet weights from https://drive.google.com/file/d/1qtDV3-uC38BrkGL5lnacmWp96RqHKhft/view?usp=sharing and place them into this folder or change the weight path at line 36 in fishermansfriend.py

Notice: 
-----------------
Sadly the bot no longer works on retail wow. It should still work on private server if you dabble in such activities. It is my theory that blizzard developed a method to detect synthetic keyboard and mouse usage. When it detects synthetic mouse and KB usage it makes the game spawn a useless bobber. This bobber never enter the water (no fish ever get caught), and it doesn't disappear after your fishing spell ends channeling (?). I currently have no solution for this

Instructions: 
-----------------
* Turn on autoloot in wow
* Run "fishermansfriend.py"
* Switch to your world of warcraft window
* Equip a fishing rod and bind fishing to T - line 48 in fishermansfriend.py.
* Face your character towards the water
* Go into first person view (scroll all the way to your face)

Variables you maybe want to adjust:
---------------
* distance_sensitivity - this determines how much do you expect the bobber to move when it goes into the water, the default value will probably work fine but if you notice that sometimes the bobber goes into the water without right click being pressed the issues is probably with this value you can uncomment line 73 and monitor the output to see how much your distance_sensitivity should be. 
* fish_goal - how many times you expect to cast the fishing spell before the bot logs out, dependent on how much space you have in your bags 
* The libdarknet.so path in darknet.py at line 122

Ban Safety:
-----------
* The nice thing about python fishbots is that they are undetectable by Warden or any other anti-hack tools used in wow. This is because they run outside of the world of warcraft client. All they do is move your cursor, take screen shots, press a few keyboard keys, and right click. They don't interact with the game in the way that detectable bots do.

Features in-mind for the future:
--------------------------------
* Monitor only the y axis, no need to calculate distance
* Don't save pictures to the drive but keep then in memory instead (~7% detection time)
* Make it a console runnable application with argument parsing from the command line

Contact:
--------
jeronim96@gmail.com or here