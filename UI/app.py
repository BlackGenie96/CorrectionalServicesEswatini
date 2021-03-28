import tkinter as tk
from login import *

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()


        self._frame = None
        self.officer_info = None
        self.current_offender = None
        self.switch_frame(LoginFrame)

    def makeFullScreen(self):
        self.geometry("%dx%d" % (self.width,self.height))
        

    def switch_frame(self, frame_class):
        try:
            new_frame = frame_class(self)

            #destroy the current frame if exists
            if self._frame is not None:
                print("Destroyed : %s" % (self._frame.winfo_class))
                self._frame.destroy()

            #assing new frame to the class frame variable
            self._frame = new_frame
            self._frame.pack()
        except TypeError:
            print('THis error')
