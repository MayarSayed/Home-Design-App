# # Wall Paint Functions

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2 
import numpy as np

def Simple_Wall(image_src = 'wallimages/wall4_2.jpg' , color = (5, 94, 76,0.2) ):
    # Read in the image
    image = mpimg.imread(image_src)
    
    # change image color to gray scale
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)
    
    # edges = cv.Canny(gray_image,100,200)
    cnts, hierarchy = cv2.findContours(blackAndWhiteImage ,cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # Find the index of the largest contour
    areas = [cv2.contourArea(c) for c in cnts]
    max_index = np.argmax(areas)

    #Fill in the Wall with the Specific Color
    cv2.drawContours(image, cnts, max_index, color , -1)
    return image
    

def Simple_3Walls(image_src = 'wallimages/wall9.jpg' , color = (5, 94, 76,0.2) ):
    # Read in the image
    image = mpimg.imread(image_src)
    
    # change image color to gray scale
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(gray_image, 195, 255, cv2.THRESH_BINARY)
    
    # edges = cv.Canny(gray_image,100,200)
    cnts, hierarchy = cv2.findContours(blackAndWhiteImage ,cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # Find the index of the largest contour
    areas = [cv2.contourArea(c) for c in cnts]
    max_index = np.argmax(areas)
    
    #Fill in the Wall with the Specific Color
    cv2.drawContours(image, cnts, max_index, color , -1)
    return image


def Simple_Chair(image_src = 'wallimages/wall8.jpg' , color = (5, 94, 76,0.2) ):
    # Read in the image
    image = mpimg.imread(image_src)
    
    # change image color to gray scale
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(gray_image, 168, 255, cv2.THRESH_BINARY)
    
    # edges = cv.Canny(gray_image,100,200)
    cnts, hierarchy = cv2.findContours(blackAndWhiteImage ,cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # Find the index of the largest contour (wall)
    areas = [cv2.contourArea(c) for c in cnts]
    max_index = np.argmax(areas)

    #Fill in the Wall with the Specific Color
    cv2.drawContours(image, cnts, max_index, color , -1)
    return image


def Long_Chair(image_src = 'wallimages/wall55.jpe' , color = (5, 94, 76,0.2) ):
    # Read in the image
    image = mpimg.imread(image_src)
    
    # change image color to gray scale
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(gray_image, 142, 255, cv2.THRESH_BINARY)
    
    # edges = cv.Canny(gray_image,100,200)
    cnts, hierarchy = cv2.findContours(blackAndWhiteImage ,cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # Find the index of the largest contour (wall)
    areas = [cv2.contourArea(c) for c in cnts]
    max_index = np.argmax(areas)

    #Fill in the Wall with the Specific Color
    cv2.drawContours(image, cnts, max_index, color , -1)
    return image




