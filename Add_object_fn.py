# -*- coding: utf-8 -*-
"""
Created on Mon May 11 23:13:19 2020

@author: Mayar
"""
import numpy as np
import cv2
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def add_obj(room,obj,X,Y):
    
    obj_height,obj_width,obj_channels = obj.shape
    Start_height = math.floor(Y - (obj_height/2))
    Start_width = math.floor(X -(obj_width/2))
    room_height,room_width,room_channels = room.shape
    if(obj_width > 0.5*room_width):
       obj = cv2.resize(obj,(math.floor(room_width*0.4),math.floor(obj_height )))
       obj_height,obj_width,obj_channels = obj.shape

    if(obj_height > 0.5*room_height):
       obj = cv2.resize(obj,(math.floor(obj_width),math.floor(room_height*0.4 )))
       obj_height,obj_width,obj_channels = obj.shape
       
    if(room_height > obj_height and room_width > obj_width):
        #Case 1
        if(Start_width < 0):
            if(Start_height < 0):
                room[0:obj_height,0:obj_width] = obj[0:obj_height,0:obj_width]
                
            elif(Start_height + obj_height > room_height ):
                room[room_height-obj_height:room_height+obj_height,0:obj_width] = obj[0:obj_height,0:obj_width]
                

            else:
                room[Start_height:Start_height+obj_height,0:obj_width] = obj[0:obj_height,0:obj_width]
              

        #Case 2
        elif(Start_width +obj_width > room_width):
            if(Start_height < 0):
                room[0:obj_height,room_width-obj_width:room_width+obj_width] = obj[0:obj_height,0:obj_width]
                
            elif(Start_height + obj_height > room_height ):
                room[room_height-obj_height:room_height+obj_height,room_width-obj_width:room_width+obj_width] = obj[0:obj_height,0:obj_width]
               
            else:
                room[Start_height:Start_height+obj_height,room_width-obj_width:room_width+obj_width] = obj[0:obj_height,0:obj_width]
                
        #Case 3
        elif(Start_height < 0):
            room[0:obj_height,Start_width:Start_width+obj_width] = obj[0:obj_height,0:obj_width]
           
        
        elif(Start_height + obj_height > room_height ):
            room[room_height-obj_height:room_height+obj_height,Start_width:Start_width+obj_width] = obj[0:obj_height,0:obj_width]
            
        
        else:  
            room[Start_height:Start_height+obj_height,Start_width:Start_width+obj_width] = obj[0:obj_height,0:obj_width]
            
    
    return(room)

obj = cv2.imread('C:/Users/Sara/Documents/GitHub2/Home-Design-App/new/obj1.jpeg')
 
obj_height,obj_width,obj_channels = obj.shape

room = cv2.imread('C:/Users/Sara/Documents/GitHub2/Home-Design-App/new/room1.jpg')
room_height,room_width,room_channels = room.shape

room_after = add_obj(room,obj,600,630)
plt.imshow(room_after)
plt.show()
#print(obj_height,obj_width,obj_channels)
#print(room_height,room_width,room_channels)