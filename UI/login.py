import tkinter as tk
import tkinter.messagebox as mb
import requests
from firstMenu import *
from constants import *

class LoginFrame(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)

        #definition of widgets
        tk.Label(self,text="Enter Your ID below:",font=label_title_font,width="50").pack(side=tk.TOP,pady=15)
        self.officer_id = tk.Entry(self,width="35",font=entry_font)
        self.officer_id.pack(side=tk.TOP,expand=1,ipady=5,pady=10)
        self.officer_id.focus_set()

        tk.Button(self, text="LOG IN",font=button_font,command=lambda:self.loginService(master)).pack(side=tk.TOP,ipady=5,ipadx=5,pady=10)

    def loginService(self,master):
        r = requests.post('http://localhost/CorrectionalServices/API/login.php',{'officer_no': self.officer_id.get()}).json()

        if r['success'] == 1:
            print(f"{r['message']}")
            master.officer_info = {
                'name'      : f"{r['name']}",
                'surname'   : f"{r['surname']}",
                'officer_id': f"{r['officer_id']}"
            }

            master.switch_frame(FirstMenu)
        else:
            print(f"{r['message']}")
            mb.showinfo('Notice',f'{r["message"]}')
