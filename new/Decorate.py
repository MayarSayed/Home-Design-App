from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.image import Image
from kivy.uix.behaviors import CoverBehavior
from kivy.graphics import Color, Rectangle
from os.path import join, dirname
import numpy as np
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.colorpicker import ColorPicker
from kivy.properties import ObjectProperty
from operator import mul
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
import cv2
import time
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.core.window import Window

#from android.storage import app_storage_path
#settings_path = app_storage_path()
#from android.permissions import request_permissions, Permission
#request_permissions([Permission.WRITE_EXTERNAL_STORAGE,Permission.READ_EXTERNAL_STORAGE])
#from android.storage import primary_external_storage_path
x_clk=0
y_clk=0
def Detect_Objects(img):
    # Yolo algorithm for Detection
    net = cv2.dnn.readNet("yolov3.weights",
                          "yolov3.cfg")
    classes = []
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    # print(classes)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    height, width, channels = img.shape

    # detect Furniture Image
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # showing info on screen
    class_ids = []
    confidences = []
    boxes = []

    Furniture_list = ["chair", "sofa", "bed", "bench", "diningtable", "refrigerator",
                      "oven", "microwave", "clock"]

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if ((confidence > 0.5)):
                # object detected Dimensions
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                width_obj = int(detection[2] * width)
                height_obj = int(detection[3] * height)

                # rectangle coordinates
                x_rect = int(center_x - width_obj / 2)
                y_rect = int(center_y - height_obj / 2)

                boxes.append([x_rect, y_rect, width_obj, height_obj])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    objs = []  # store cropped objects for one image

    for i in range(len(boxes)):
        if ((i in indexes)):
            for z in Furniture_list:
                if classes[class_ids[i]] == z:
                    x_box, y_box, w_box, h_box = boxes[i]
                    objs.append(img[y_box: y_box + h_box, x_box: x_box + w_box])

    return (objs)
SD_CARD = "D:"
mcolor=(255,255,0,1)
i=0
mimage='boy.png'
captured="obj1.jpg"
selected="obj2.jpg"
After="room1.jpg"
class CameraClick(Screen):
    camera=ObjectProperty(None)
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png(SD_CARD+"/IMG.png")
        global  captured
        captured=SD_CARD+"/IMG.png"
        sm.current="check"
        print("Captured")

def Simple_Wall(image_src='wallimages/wall4_2.jpg', color=(5, 94, 76, 0.2)):
    # Read in the image
    image = cv2.imread(image_src)

    # change image color to gray scale
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)

    # edges = cv.Canny(gray_image,100,200)
    cnts, hierarchy = cv2.findContours(blackAndWhiteImage, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # Find the index of the largest contour
    areas = [cv2.contourArea(c) for c in cnts]
    max_index = np.argmax(areas)

    # Fill in the Wall with the Specific Color
    cv2.drawContours(image, cnts, max_index, color, -1)
    return image


def Simple_3Walls(image_src='wallimages/wall9_3.jpg', color=(5, 94, 76, 0.2)):
    # Read in the image
    image = cv2.imread(image_src)

    # change image color to gray scale
    image1 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray_image = cv2.cvtColor(image1, cv2.COLOR_RGB2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(gray_image, 120, 255, cv2.THRESH_BINARY)

    lower_white = np.array([229, 229, 229])
    upper_white = np.array([255, 255, 255])
    # Define the masked area
    mask = cv2.inRange(image, lower_white, upper_white)

    newimage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    masked_image = np.copy(newimage)
    masked_image[mask == 0] = [0, 0, 0]

    # edges = cv2.Canny(gray_image,100,200)
    cnts, hierarchy = cv2.findContours(blackAndWhiteImage, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # Find the index of the largest contour
    areas = [cv2.contourArea(c) for c in cnts]
    max_index = np.argmax(areas)

    cv2.drawContours(image, cnts, max_index, color, -1)

    # Load in a background image, and convert it to RGB
    background_image = image
    resized = cv2.resize(background_image, (4000, 3000), interpolation=cv2.INTER_AREA)

    new_mask = cv2.bitwise_not(mask)
    masked_image_bg = cv2.bitwise_and(resized, resized, mask=new_mask)

    complete_image = masked_image_bg + masked_image

    return complete_image


def Simple_Chair(image_src='wallimages/wall8.jpg', color=(5, 94, 76, 0.2)):
    # Read in the image
    image = cv2.imread(image_src)

    # change image color to gray scale
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(gray_image, 168, 255, cv2.THRESH_BINARY)

    # edges = cv.Canny(gray_image,100,200)
    cnts, hierarchy = cv2.findContours(blackAndWhiteImage, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # Find the index of the largest contour (wall)
    areas = [cv2.contourArea(c) for c in cnts]
    max_index = np.argmax(areas)

    # Fill in the Wall with the Specific Color
    cv2.drawContours(image, cnts, max_index, color, -1)
    return image


def Long_Chair(image_src='wallimages/wall55.jpe', color=(5, 94, 76, 0.2)):
    # Read in the image
    image = cv2.imread(image_src)

    # change image color to gray scale
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(gray_image, 142, 255, cv2.THRESH_BINARY)

    # edges = cv.Canny(gray_image,100,200)
    cnts, hierarchy = cv2.findContours(blackAndWhiteImage, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # Find the index of the largest contour (wall)
    areas = [cv2.contourArea(c) for c in cnts]
    max_index = np.argmax(areas)

    # Fill in the Wall with the Specific Color
    cv2.drawContours(image, cnts, max_index, color, -1)
    return image
def send(captured):
    objects = []
    img = cv2.imread('sara.jpeg')
    objects = Detect_Objects(img)
    return objects
class ConfirmPopup(Popup):
    text = StringProperty('Do you want to save the photo?')

    ok_text = StringProperty('Save')
    cancel_text = StringProperty('Cancel')

    __events__ = ('on_ok', 'on_cancel')

    def ok(self):
        self.dispatch('on_ok')
        self.dismiss()


    def cancel(self):
        self.dispatch('on_cancel')
        self.dismiss()


    def on_ok(self):
        y=cv2.imread(After)
        cv2.imwrite(SD_CARD+"/myph.jpg", y)
        sm.current = "main"


    def on_cancel(self):
        sm.current = "main"
class P(FloatLayout):
    pass
def show_popup():
    show = P() # Create a new instance of the P class
    clr_picker = ColorPicker()
    clr_picker.pos_hint={"x":0.05, "top":0.99}
    show.add_widget(clr_picker)
    def on_color(instance, value):
        print("RGBA = ", str(value))  # or instance.color
        global mcolor
        res=tuple(value)
        mcolor= list(map(mul, res, (255,255,255,255)))
        temp=0
        temp=mcolor[0]
        mcolor[0]=mcolor[2]
        mcolor[2]=temp
        mcolor=tuple(mcolor)


        print(mcolor)

    clr_picker.bind(color=on_color)
    popupWindow = Popup(title="Popup Window", content=show, size_hint=(None, None), size=(600, 600))
    # Create the popup window

    popupWindow.open()  # show the popup
def popup2():
    h=ConfirmPopup()
    h.open()
class CheckImg(Screen):
    objs = ObjectProperty(None)
    yarb = ObjectProperty(None)
    text = StringProperty("Select your object")

    def on_enter(self):
        img = send(captured)
        self.text="kkkkkkkkkkkkkkkkkkkkkkk"
        for i in img:
            cv2.imwrite('tt.jpg',i)
            submit = Button(background_normal='tt.jpg')
            submit.bind(on_press=self.pressed)
            self.objs.add_widget(submit)
    def pressed(self,i):
        selected=i.background_normal
        print("pressed")
        self.manager.get_screen("wall").select.opacity = 1
        sm.current="wall"
        print(selected)

class MainWindow(Screen):

    def travel(self,new_image):
        #self.ids.mwall.color.opacity = 0
        global mimage,After
        mimage = new_image
        After=mimage
        sm.current="wall"

class WallWindow(Screen):
    test = ObjectProperty(None)
    color = ObjectProperty(None)
    paint = ObjectProperty(None)
    addobj=ObjectProperty(None)
    select=ObjectProperty(None)
    def on_enter (self):
        global mimage
        global After
        #After = mimage
        self.test.source = After
        self.test.reload()
    def mayarsara(self):
        global y_clk,x_clk
        print("x_clk: "+str(x_clk))
    def on_touch_down(self,touch):
        global y_clk,x_clk
        x_clk=touch.pos[0]
        y_clk = touch.pos[1]
        return super(WallWindow, self).on_touch_down(touch)
    def colors(self):
        show_popup()
    def change(self):
        global mimage,After
        print("yyyyyyyyyyyy"+mimage)
        global mcolor
        if(mimage=='room1.jpg'):
            img=Simple_Wall(mimage,mcolor)
        elif (mimage=='room2.jpg'):
            img=Simple_Chair(mimage,mcolor)
        elif (mimage=='room3.jpg'):
            img=Simple_3Walls(mimage,mcolor)
        elif(mimage=='room4.jpg'):
            img=Long_Chair(mimage,mcolor)
        print("Entered")
        After="test2.jpg"
        cv2.imwrite("test2.jpg", img)
        #Image("test2.jpg").save("D:/AVR/test2.jpg")
        self.test.source="test2.jpg"
        self.test.reload()
class ObjWindow(Screen):
    mc1 = StringProperty("obj1.jpg")
    mc2 = StringProperty("obj2.jpg")
    mc3 = StringProperty("obj3.jpg")
    mc4 = StringProperty("obj4.jpg")

    obj1=ObjectProperty(None)
    obj2 = ObjectProperty(None)
    obj3 = ObjectProperty(None)
    obj4 = ObjectProperty(None)

    def Apply(self):
        global i
        print("image"+captured)
        if(i==0):
            self.mc1=captured
            self.obj1.background_normal=self.mc1
            print("111")
        elif(i==1):
            self.mc2 = captured
            self.obj2.background_normal = self.mc2
            print("222")
        elif (i == 2):
            self.mc3 = captured
            self.obj3.background_normal = mc3
        elif (i >=4):
            self.mc4 = captured
            self.obj4.background_normal = mc4
            i==0
        i+=1

    def choose(self,mimg):
        print(mimage)
        global selected,After
        selected=mimg
        self.manager.get_screen("wall").select.opacity=1

        sm.current = "wall"
class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("mymain.kv")
sm = WindowManager()
screens = [MainWindow(name="main"), WallWindow(name="wall"),ObjWindow(name="obj"),CameraClick(name="mcamera"),CheckImg(name="check")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "main"



class MyMainApp(App):
    def build(self):
        Window.bind(on_keyboard=self.key_input)
        return sm

    def key_input(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            if(sm.current=="wall" ):
                popup2()
            elif(sm.current=="obj"):
                sm.current = "wall"
            elif(sm.current=="mcamera"):
                sm.current = "obj"
            elif(sm.current=="check"):
                sm.current = "mcamera"
            else:
                App.get_running_app().stop()
            return True  # override the default behaviour
        else:  # the key now does nothing
            return False

    def on_pause(self):
        return True

if __name__ == "__main__":
    MyMainApp().run()

########################################################################HADEEL


