# -*- coding: utf-8 -*-
"""
Created on Wed May  6 03:31:13 2020

@author: Sara
"""
import cv2
import numpy as np

def Detect_Objects(img):
    #Yolo algorithm for Detection
    net = cv2.dnn.readNet("C:/Users/Sara/Downloads/yolo/yolov3.weights",
                      "C:/Users/Sara/Downloads/yolo/yolov3.cfg")
    classes = []
    with open("C:/Users/Sara/Downloads/yolo/coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    #print(classes)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]    
    height , width , channels = img.shape
    
    #detect Furniture Image
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    
    #showing info on screen
    class_ids = []
    confidences = []
    boxes = []

    Furniture_list = ["chair" , "sofa" , "bed", "bench" , "diningtable" , "refrigerator" ,
                  "oven" , "microwave" , "clock"]  
    
    for out in outs:
        for detection in out : 
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if ((confidence > 0.5)) :
                #object detected Dimensions
                center_x = int(detection[0] * width )
                center_y = int(detection[1] * height )
                width_obj = int (detection[2] * width )
                height_obj = int (detection[3]* height )
                
                #rectangle coordinates 
                x_rect = int(center_x - width_obj / 2)
                y_rect = int(center_y - height_obj / 2)
                
                boxes.append([x_rect, y_rect , width_obj, height_obj])
                confidences.append(float(confidence))
                class_ids.append(class_id)
            
            
            
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    objs = []#store cropped objects for one image

    for i in range (len(boxes)) :
        if ((i in indexes)) :
            for z in Furniture_list:
                if classes[class_ids[i]] == z:
                    x_box , y_box , w_box , h_box = boxes[i]
                    objs.append ( img[ y_box : y_box+h_box , x_box: x_box+w_box ] )

    return(objs)
    
    ##############################################################################
img = cv2.imread('C:/Users/Sara/Desktop/image/living_room.jpg' )
objects = []
objects = Detect_Objects(img)   

print(len(objects))

for q in range (len(objects)):
    cv2.imshow(str(q), objects[q])

cv2.waitKey(0)
cv2.destroyAllWindows()

                 
                    
                    