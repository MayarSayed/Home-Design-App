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
SD_CARD = "D:"
mcolor=(0,0,0,0)
i=0
mimage='boy.png'
captured="obj1.jpg"
selected="obj2.jpg"
After="room1.jpg"

    #text = StringProperty('Do you want to save the photo?')

    #ok_text = StringProperty('Save')
    #cancel_text = StringProperty('Cancel')
def Mayars(room,obj):
    print(room)
    print(obj)
    cv2.imread("room1.jpg")
    return "room3.jpg"

class CameraClick(Screen):
    camera=ObjectProperty(None)
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        #camera = self.ids['camera']
        #timestr = time.strftime("%Y%m%d_%H%M%S")
        #camera.export_to_png("IMG.png".format(timestr))
        global  captured
        captured="boy.png"
        sm.current="obj"
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
def Simple_3Walls(image_src='wallimages/wall9.jpg', color=(5, 94, 76, 0.2)):
    # Read in the image
    image = cv2.imread(image_src)

    # change image color to gray scale
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(gray_image, 195, 255, cv2.THRESH_BINARY)

    # edges = cv.Canny(gray_image,100,200)
    cnts, hierarchy = cv2.findContours(blackAndWhiteImage, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # Find the index of the largest contour
    areas = [cv2.contourArea(c) for c in cnts]
    max_index = np.argmax(areas)

    # Fill in the Wall with the Specific Color
    cv2.drawContours(image, cnts, max_index, color, -1)
    return image


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

class ConfirmPopup(Popup):
    text = StringProperty('Do you want to save the photo?')

    ok_text = StringProperty('Save')
    cancel_text = StringProperty('Cancel')

    __events__ = ('on_ok', 'on_cancel')

    def ok(self):
        self.dispatch('on_ok')
        self.dismiss()
        sm.current = "main"

    def cancel(self):
        self.dispatch('on_cancel')
        self.dismiss()


    def on_ok(self):
        cv2.imwrite(SD_CARD+"/test2.jpg", mimage)
        sm.current = "main"


    def on_cancel(self):
        sm.current = "main"
class MyPaintWidget(Widget):

    def on_touch_down(self, touch):
        print("hhhhhhhhhhhhh")
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

class MainWindow(Screen):

    def travel(self,new_image):
        #self.ids.mwall.color.opacity = 0
        global mimage
        mimage = new_image
        sm.current="wall"

class WallWindow(Screen):
    test = ObjectProperty(None)
    put = ObjectProperty(None)

    color = ObjectProperty(None)
    start = ObjectProperty(None)
    paint = ObjectProperty(None)
    addobj=ObjectProperty(None)
    select=ObjectProperty(None)




    def back(self):
        #TODO confirmation
        popup2()
        self.start.opacity = 1
        self.test.opacity = 0
        self.color.opacity = 0
        self.paint.opacity = 0
        self.put.opacity = 0
        self.addobj.opacity = 0


    def manage(self):
        global mimage
        global After
        After=mimage
        self.test.source = mimage
        self.test.reload()
        self.start.opacity = 0
        self.test.opacity = 1
        self.color.opacity = 1
        self.paint.opacity = 1
        self.put.opacity = 1
        self.addobj.opacity = 1
   # img_src = StringProperty('boy.png')
    def colors(self):
        show_popup()
        #self.add_widget(self.clr_picker)
    def Mayarsara(self):
        #After
        #selected
        self.select.opacity=1
        #############################MAYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAR
        #Window.bind(mouse_pos=lambda w, p: print((p)))
    def change(self):
        global mimage
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
        After=img
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
            self.obj1.background_normal=captured

            print("111")
        elif(i==1):
            self.mc2 = captured
            self.obj2.background_normal = mc2
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
        global selected
        selected=mimg
        sm.current = "wall"

        #new=Mayars("test2.jpg",mimg)


class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("mymain.kv")
sm = WindowManager()
screens = [MainWindow(name="main"), WallWindow(name="wall"),ObjWindow(name="obj"),CameraClick(name="mcamera")]
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
                wall=WallWindow()
                wall.back()

            elif(sm.current=="obj"):
                sm.current = "wall"
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


