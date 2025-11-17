# ------------------------------------
# libraries required for bot running
# --------------------------------------

import csv
from os import error, path
import re
import time
import pyautogui
from pyautogui import *
import pandas as pd
import random
import json
import pyperclip


def press_left_keys(times):

    for _ in range(0,times):
        pyautogui.press('left')

# ----------------------------------
def FindImagesOnScreen(ListOfImages):

    """
    This function is used to find the multiple images on the screen, when any of the image was find it contains
    it returns the (x,y) cordinates where image was found.
    """
    cordinates = None

    for image in ListOfImages:

        if LocateImageOnScreen(image) == True:
            cordinates = Locate_PNGImageOnScreen(image)
            break 
    
    return cordinates



def redirect_url(link):

    """
    This function is used to redirect the group link...
    """


    # Press Ctrl + L to selsect the address bar
    pyautogui.hotkey('ctrl', 'l')

    # Wait for the address bar to become active
    time.sleep(2)

    # print("link to write is ",link)
    
    # Type the URL and press Enter
    # pyautogui.typewrite(link,interval=0.05)
    pyautogui.write(link)
    time.sleep(1)
    pyautogui.press('space')
    pyautogui.press('enter')
    time.sleep(2)

def ClickImageOnScreen(image_png,total_clicks):
    # this function is used to search the image on screen and returns the co-ordinates

    try:

        cordinates = pyautogui.locateCenterOnScreen(image_png, grayscale=True, confidence=0.8)
        pyautogui.click(cordinates[0],cordinates[1],clicks=total_clicks)
    
    except pyautogui.ImageNotFoundException: 
        # print("No Image found to Click")
        pass

def ClickImageOnScreen_withoutGrayScale(image_png,total_clicks):
    # this function is used to search the image on screen and returns the co-ordinates

    try:

        cordinates = pyautogui.locateCenterOnScreen(image_png, confidence=0.8)
        pyautogui.click(cordinates[0],cordinates[1],clicks=total_clicks)
    
    except pyautogui.ImageNotFoundException: 
        # print("No Image found to Click")
        pass

def find_image_on_screen(image_png): 

    """
    This function is used to find image on screen, 
    If it was find return True otherwise False
    """
    if len(Locate_PNGImageOnScreen(image_png)) > 0: 
        return True  

    else: 
        return False


def find_specific_image(image_png):

    """
    This function is used to find the specific image on the screen by pressing the Number of tabs on the screen 
    when the image was found then it simply break the function 
    """

    while(True):

        if LocateImageOnScreen(image_png) == True:         
            break 
        time.sleep(0.5)
        pyautogui.press('tab')


def LocateAllImagesOnScreen(image_path):
    """
    Locates all occurrences of a specified image on the screen.

    Parameters:
    - image_path (str): The path to the image file.
    - grayscale (bool): Whether to use grayscale mode for image matching (default: True).
    - confidence (float): The minimum confidence level for matching (default: 0.8).

    Returns:
    - list of tuples: A list of (x, y) positions where the image is located on the screen.
    """
    positions = []
    
    try:
        # Locate all occurrences of the image on the screen
        locations = pyautogui.locateAllOnScreen(image_path, grayscale=True, confidence=0.8)
        for loc in locations:
            # Get the center of each located instance of the image
            x, y = pyautogui.center(loc)
            positions.append((x, y))

    except Exception as e:
        print(f"Error locating images on screen: {e}")
    
    return positions

def Locate_PNGImageOnScreen(image_png):

    # this function is used to search the imsage on screen and returns the co-ordinates
    # time.sleep(4)

    try:

        if pyautogui.locateCenterOnScreen(image_png, grayscale=True, confidence=0.8) != None:
            cordinates = pyautogui.locateCenterOnScreen(image_png,grayscale=True, confidence=0.8)
            position = []
            position.append(cordinates[0])
            position.append(cordinates[1])
            return position
        else:
            return [] 
    
    except pyautogui.ImageNotFoundException: 
        return []


def move_cursor(): 
    """
    This function is used to move the cursor to left side of screen where Twitter Icon was place
    """ 

    pyautogui.moveTo(100,100)

    # cordinates = Locate_PNGImageOnScreen('.//Images/ICON.png') 
    # pyautogui.click(cordinates[0]+120,cordinates[1])
    # time.sleep(1)

def Click_PNGImageOnScreen(image_png,_x,_y,total_clicks):
    # this function is used to search the image on screen and returns the co-ordinates

    if len(Locate_PNGImageOnScreen(image_png)) > 0:

        cordinates = pyautogui.locateOnScreen(image_png, grayscale=True, confidence=0.8)
        pyautogui.click(cordinates[0]+_x,cordinates[1]+_y,clicks=total_clicks) # (x,y) 

    else:
        pass

def LocateImageOnScreen(image_png):

    # this function is used to search the image on screen and returns the co-ordinates
    # time.sleep(4)

    try:
        # print("block a")


        if pyautogui.locateCenterOnScreen(image_png, grayscale=True, confidence=0.8) != None:
            return True
        else:
            return False
        

    except pyautogui.ImageNotFoundException as e:
        # print("block b")

        # print("exception block") 
        return False


def locate_when_appear(png_image):
    """
    This function is used to find image when it appears...
    It prevents the unwanted time sleeps
    """
    counter = 0
    while(True):
        
        try:

            if LocateImageOnScreen(png_image) == True: 
                break
            else: 
                time.sleep(1)

            counter += 1
            if counter == 7:
                break
        
        except pyautogui.ImageNotFoundException:
            pass


def click_when_appear(png_image):
    """
    This function is used to click on image when it appears...
    It prevents the unwanted time sleeps
    """

    while(True): 
        if LocateImageOnScreen(png_image) == True: 
            ClickImageOnScreen(png_image,1)
            break
        else: 
            time.sleep(0.5)

def press_up_key(n_times):
    """
    Press UP key on keyboard
    """
    for i in range(0,n_times):
        pyautogui.press('up')

def press_arrow_keys(arrow_,times):

    for i in range(0,times):
        pyautogui.hotkey(arrow_)

def press_down_keys(n_times):

    for i in range(0,n_times):
        pyautogui.press('down')

def press_up_key(n_times):

    for i in range(0,n_times):
        pyautogui.press('up')

def press_tab_key(times):

    for i in range(0,times):
        pyautogui.press('tab')


def please_wait(png_image):

    """
    Wait until appear... 
    """

    while(True):

        try:

            if LocateImageOnScreen(png_image) == True: 
                break  

            time.sleep(1)

        
        except pyautogui.ImageNotFoundException: 
            pass

def wait_and_click(png_image):

    """
    This function is used to wait for a image , and then click on the image ... 
    """
    while(True):

        try:

            if LocateImageOnScreen(png_image) == True: 
                
                time.sleep(1)
                ClickImageOnScreen(png_image,1)
                break  

            time.sleep(1)
        
        except pyautogui.ImageNotFoundException: 
            pass

def wait_and_click_after_time(png_image):

    """
    This function is used to wait for a image , and then click on the image ... 
    """
    flag = True #by - default we assume this condition that image was found on a screen ...

    counter = 0
    while(True):

        try:

            if LocateImageOnScreen(png_image) == True: 
                
                time.sleep(1)
                ClickImageOnScreen(png_image,1)
                break  

            time.sleep(1)
            
        except pyautogui.ImageNotFoundException: 
            pass

        counter += 1 
        if counter == 5: 
            flag = False
            break

    return flag

def please_wait_for_n_seconds(png_image,n):

    """
    this function waits for N number seconds on the monitor screen till the image appears, 
    if no image found returns the False value , 
    if image was found it returns the True value statement 
    """
    counter = 0

    while(True):

        try:

            if LocateImageOnScreen(png_image) == True: 
                break 

            else:
                # print(f"Time seconds {counter}")
                time.sleep(1)
        except pyautogui.ImageNotFoundException:
            pass

        counter += 1 

        if counter == n: 
            break 

    if counter == n: 
        # print(counter)
        return False

    else:
        return True

def please_wait_for_sometime(png_image):

    """
    This function is used to wait for sometime if image wasn't appear then it simply break the function , this is very useful in case of dynamic images, especially in such cases when due to slow internet connection or slow computer speed due to lack of good hardware... 
    """
    counter = 0

    while(True):

        try:

            if LocateImageOnScreen(png_image) == True: 
                break 

            else:
                time.sleep(1)
                counter += 1 
        
            if counter > 5:
                break
        
        except pyautogui.ImageNotFoundException:
            pass
    
    if counter < 5: 
        return True
    
    else:
        return False

def click_if_any_image_appears(list_of_images): 

    """
    This function takes a list of images , if any of them appears on web screen then simply click on that image ... , we need this method if a web template was changed dynamically after some time ...
    """

    boolean = False

    for image in list_of_images: 

        if LocateImageOnScreen(image) == True: 
            ClickImageOnScreen(image, 1)  
            boolean = True
            break 
        
        else:
            time.sleep(1) 
    
    return boolean

def click_on_inspect_element_scrollbar():

    axes = Locate_PNGImageOnScreen('./Images/settings.png')

    for i in range(0,7):
        pyautogui.click(axes[0]+75,axes[1]+25)


def find_head_tag():

    axes = Locate_PNGImageOnScreen('./Images/settings.png')


    while(True):

        if find_image_on_screen('./Images/body.png') == True:
            break

        else:
            pyautogui.click(axes[0]+75,axes[1]+245)


        time.sleep(1)

def press_backspace(number):

    for i in range(0,number):
        pyautogui.press("backspace")


def redirect_file_path(filename,folder_path):
    
    axes = pyautogui.locateOnScreen('.//Images/up.png') 
    pyautogui.click(axes[0]+700,axes[1],clicks=1)

    time.sleep(1)
    pyautogui.press('backspace')
    time.sleep(1)

    pyautogui.typewrite(folder_path,interval=0.05)
    pyautogui.press('enter')
    time.sleep(1)

    # click on filename...
    axes = pyautogui.locateOnScreen('.//Images/filename.png')
    pyautogui.click(axes[0]+300,axes[1],clicks=1)
    time.sleep(1)

    pyautogui.typewrite(filename,interval=0.05)
    pyautogui.press('enter')

    # auto-check condition to terminate the 
    time.sleep(7)

    if find_image_on_screen('.//Images/post.png') == False:

        # print("Post image not found...")

        pyautogui.press('enter')
        pyautogui.press('tab')
        pyautogui.press('tab') 
        pyautogui.press('tab') 
        time.sleep(1)

        pyautogui.press('enter')

def if_this_image_appear_on_screen(png_image):

    """
    This function wait for 3 secs to check the certain image was appear on screen or not...
    """

    flag = False
    counter = 0

    while(True):
        if find_image_on_screen(png_image) == True:
            flag = True
            pyautogui.press('enter')
            time.sleep(1)
            break 

        counter += 1 
        time.sleep(1)

        if counter == 3:
            break    
    
    return flag

def scroll_down_until_image_found(png_image): 

    """
    This function will scroll down the monitor screen till the specific image was appear on a screen ...
    """

    while(True): 

        if LocateImageOnScreen(png_image) == True: 
            break 

        else: 
            press_down_keys(5)
        
        time.sleep(1)

def maximimize_chrome():

    ClickImageOnScreen('./Images/maximum.png',1)


def copy_url():
    # Bring the Chrome window to the front
    # pyautogui.hotkey('alt', 'tab')

    # Give the window a moment to come to the front
    time.sleep(1)

    # Select the address bar
    pyautogui.hotkey('ctrl', 'l')

    # Copy the URL
    pyautogui.hotkey('ctrl', 'c')

    # Give the clipboard a moment to update
    time.sleep(1)

    # Get the URL from the clipboard
    url = pyperclip.paste()

    # ClickImageOnScreen

    return url

def copy_text():

    # Bring the Chrome window to the front
    # pyautogui.hotkey('alt', 'tab')
    # Give the window a moment to come to the front
    time.sleep(1)

    # Select the address bar
    pyautogui.hotkey('ctrl', 'a')

    # Copy the URL
    pyautogui.hotkey('ctrl', 'c')

    # Give the clipboard a moment to update
    time.sleep(1)

    # Get the URL from the clipboard
    text = pyperclip.paste()
    # pyautogui.press('left')

    # axes = pyautogui.position()

    # ClickImageOnScreen

    return text

# print("start /_")
# time.sleep(4)
# scroll_down_until_image_found("./Screenshots/LinkedIn/comment.png")
# text = copy_text()
# print(text) 

# ClickImageOnScreen("./Screenshots/LinkedIn/comment.png",1)

# click_on_inspect_element_scrollbar()
# axes = Locate_PNGImageOnScreen('./Images/all_filters.png')
# scrolling_function(axes,1)
# find_head_tag()

# print("starts /_")
# time.sleep(5)
# flag = please_wait_for_sometime('./Screenshots/posts.png')
# print(flag)

# URL = copy_url()
# print(URL)

# time.sleep