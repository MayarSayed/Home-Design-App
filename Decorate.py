from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.core.image import Image
from kivy.uix.behaviors import CoverBehavior
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.colorpicker import ColorPicker
from kivy.properties import ObjectProperty
from operator import mul
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
import cv2
from kivy.core.window import Window
#from android.storage import app_storage_path
#settings_path = app_storage_path()
mcolor=(0,0,0,0)
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
    popupWindow = Popup(title="Popup Window", content=show, size_hint=(None,None),size=(600,600))
    # Create the popup window

    popupWindow.open() # show the popup
class MainWindow(Screen):
    pass
class WallWindow(Screen):
    test = ObjectProperty(None)
   # img_src = StringProperty('boy.png')

    def in_touch_down(self, touch):
        print("Mouse Down", touch)
        self.test.source = "boy.bng"
    def colors(self):
        show_popup()
        #self.add_widget(self.clr_picker)
    def change(self):
        print("Entered")
        img=cv2.imread("test.jpg")
        global mcolor
        img=cv2.rectangle(img,(100,100),(200,200),mcolor,-1)
        print(mcolor)
        #cv2.imwrite(str(settings_path)+"/mimage.jpg",img)
        cv2.imwrite("test2.jpg", img)
        self.test.source="test2.jpg"
        self.test.reload()
        #self.img_src='boy.png
class ObjWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("mymain.kv")
sm = WindowManager()
screens = [MainWindow(name="main"), WallWindow(name="wall"),ObjWindow(name="obj")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "main"



class MyMainApp(App):
    def build(self):
        Window.bind(on_keyboard=self.key_input)
        return sm

    def key_input(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            if(sm.current=="wall" or sm.current=="obj" ):
                sm.current="main"
            else:
                App.get_running_app().stop()
            return True  # override the default behaviour
        else:  # the key now does nothing
            return False

    def on_pause(self):
        return True

if __name__ == "__main__":
    MyMainApp().run()