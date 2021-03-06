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
import math
#from android.storage import app_storage_path
#settings_path = app_storage_path()
#from android.permissions import request_permissions, Permission
#request_permissions([Permission.WRITE_EXTERNAL_STORAGE,Permission.READ_EXTERNAL_STORAGE])
#from android.storage import primary_external_storage_path
x_clk=0
y_clk=0


def add_obj(room, obj, X, Y):
    Y = 660 - Y
    X = X + 160
    # starting positions

    room_height, room_width, room_channels = room.shape
    obj_height, obj_width, obj_channels = obj.shape
    print(X, Y)

    if (obj_width > 0.5 * room_width):
        print("change width")
        obj = cv2.resize(obj, (math.floor(room_width * 0.5), math.floor(obj_height)))
        obj_height, obj_width, obj_channels = obj.shape

    if (obj_height > 0.5 * room_height):
        print("change height")
        obj = cv2.resize(obj, (math.floor(obj_width), math.floor(room_height * 0.5)))
        obj_height, obj_width, obj_channels = obj.shape

    Start_height = math.floor(Y - (obj_height / 2))
    Start_width = math.floor(X - (obj_width / 2))

    if (room_height > obj_height and room_width > obj_width):
        # Case 1
        if (Start_width < 0):
            if (Start_height < 0):
                print("case1_if")
                #######################done
                room[0:obj_height, 0:obj_width] = obj[0:obj_height, 0:obj_width]

            elif (Start_height + obj_height > room_height):
                print("case1_elif")
                ##############################
                room[room_height - obj_height:room_height, 0:obj_width] = obj[0:obj_height, 0:obj_width]


            else:
                print("case1_else")
                #######S########
                room[Start_height:Start_height + obj_height, 0:obj_width] = obj[0:obj_height, 0:obj_width]


        # Case 2
        elif (Start_width + obj_width > room_width):
            if (Start_height < 0):
                print("case2_if")
                room[0:obj_height, room_width - obj_width:room_width + obj_width] = obj[0:obj_height, 0:obj_width]

            elif (Start_height + obj_height > room_height):
                print("case2_elif")
                room[room_height - obj_height:room_height + obj_height,
                room_width - obj_width:room_width + obj_width] = obj[0:obj_height, 0:obj_width]

            else:
                print("case2_else")
                room[Start_height:Start_height + obj_height, room_width - obj_width:room_width + obj_width] = obj[
                                                                                                              0:obj_height,
                                                                                                              0:obj_width]

        # Case 3
        elif (Start_height < 0):
            print("case3")
            ################
            room[0:obj_height, Start_width:Start_width + obj_width] = obj[0:obj_height, 0:obj_width]


        elif (Start_height + obj_height > room_height):
            print("case_elif")
            room[room_height - obj_height:room_height + obj_height, Start_width:Start_width + obj_width] = obj[
                                                                                                           0:obj_height,
                                                                                                           0:obj_width]


        else:
            print("case_else")
            print(X, Y)
            room[Start_height:Start_height + obj_height, Start_width:Start_width + obj_width] = obj[0:obj_height,
                                                                                                0:obj_width]

    return (room)



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
        #captured=SD_CARD+"/IMG.png"
        captured='sara.jpeg'
        sm.current='obj'
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
    image = cv2.resize(image, (1280, 750), interpolation=cv2.INTER_AREA)

    return image


def Simple_3Walls(image_src='room3.jpg', color=(5, 94, 76, 0.2)):
    # Read in the image
    image = cv2.imread(image_src)
    # print('Image dimensions:', image.shape)    # change image color to gray scale
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
    #masked_image = cv2.resize(masked_image, (4000, 3000), interpolation=cv2.INTER_AREA)


    # edges = cv2.Canny(gray_image,100,200)
    cnts, hierarchy = cv2.findContours(blackAndWhiteImage, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # Find the index of the largest contour
    areas = [cv2.contourArea(c) for c in cnts]
    max_index = np.argmax(areas)

    cv2.drawContours(image, cnts, max_index, color, -1)

    # Load in a background image, and convert it to RGB
    background_image = image
    background_image = cv2.resize(background_image, (1280, 750), interpolation=cv2.INTER_AREA)
    resized = cv2.resize(background_image, (1280, 750), interpolation=cv2.INTER_AREA)
    mask=mask.astype(np.uint8)
    mask = cv2.resize(mask, (1280, 750), interpolation=cv2.INTER_AREA)
    new_mask = cv2.bitwise_not(mask)

    new_mask = cv2.resize(new_mask, (1280, 750), interpolation=cv2.INTER_AREA)
    masked_image_bg = cv2.bitwise_and(resized, resized, mask=new_mask)
   # masked_image_bg = cv2.resize(masked_image_bg, (1280, 960), interpolation=cv2.INTER_AREA)

    complete_image = masked_image_bg + masked_image
    #complete_image = cv2.resize(complete_image, (1280, 750), interpolation=cv2.INTER_AREA)

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
    image = cv2.resize(image, (1280, 750), interpolation=cv2.INTER_AREA)

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
    image = cv2.resize(image, (1280, 750), interpolation=cv2.INTER_AREA)

    return image

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

    def popup2(self):
        h = ConfirmPopup()
        h.open()
    def on_enter (self):
        global mimage
        global After
        #After = mimage
        self.test.source = After
        self.test.reload()
        if(self.select.opacity==1):
            Clock.schedule_once(lambda dt: self.mayarsara(), 2)
    def mayarsara(self):
        global y_clk,x_clk,After,selected
        print("mayaaaaaaaaaar")
        print("x_clk: "+str(x_clk))
        print("y_clk: " + str(y_clk))
        img1=cv2.imread(After)
        img2=cv2.imread(selected)
        img=add_obj(img1,img2,x_clk,y_clk)
        #cv2.imwrite("test2.jpg", img)
        cv2.imwrite('test2.jpg',img)
        After='test2.jpg'

        self.test.source = After
        self.test.reload()
        self.select.opacity=0
    def on_touch_down(self,touch):

        global y_clk,x_clk
        print("x_clk: " + str(x_clk))
        print("y_clk: " + str(y_clk))
        x_clk=touch.pos[0]
        y_clk = touch.pos[1]
        return super(WallWindow, self).on_touch_down(touch)
    def colors(self):
        print("bebo")
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
    mc1 = StringProperty("")
    mc2 = StringProperty("")
    mc3 = StringProperty("")
    mc4 = StringProperty("")

    obj1=ObjectProperty(None)
    obj2 = ObjectProperty(None)
    obj3 = ObjectProperty(None)
    obj4 = ObjectProperty(None)
    add= ObjectProperty(None)

    def Apply(self):
        global captured
        global i
        print("image" + captured)
        if (i == 0):
            self.mc1 = captured
            self.obj1.background_normal = self.mc1
            print("111")
        elif (i == 1):
            self.mc2 = captured
            self.obj2.background_normal = self.mc2
            print("222")
        elif (i == 2):
            self.mc3 = captured
            self.obj3.background_normal =self.mc3
        elif (i >= 4):
            self.mc4 = captured
            self.obj4.background_normal = self.mc4
            i == 0
        i += 1

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


