import tkinter as tk
import tkinter.messagebox as mb
import requests
import json

from scrollable_frame import *
from constants import *
from quaterly_reviews import *

class HealthDevelopmentalFrame(tk.Frame):
    def __init__(self, master, flag='new'):
        tk.Frame.__init__(self, master)

        self.frame = ScrollableFrame(master)

        self.buildWidgets(master,flag)
        
        if flag == 'edit':
            print('Retrieving offender data from database to display')
            self.populateWidgets(master)


        self.frame.pack()

    def buildWidgets(self,master, flag):
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row,text='HEALTH RECORD',font=label_title_font)
        row.pack(side='top',pady=20)
        lab.pack(side='top')

        row = tk.Frame(self.frame.scrollable_frame)
        self.health = tk.Text(row,bg='white', wrap=tk.WORD,font=entry_font,width=60,height=10)
        self.health.focus_set()
        row.pack(side='top',padx=30)
        self.health.pack(side='top')
        
        #developmental history widget definitions
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row,text='DEVELOPMENTAL HISTORY',font=label_title_font)
        row.pack(side='top',pady=20)
        lab.pack(side='top')

        row = tk.Frame(self.frame.scrollable_frame)
        self.develop = tk.Text(row,bg='white',wrap=tk.WORD,font=entry_font,width=60,height=10)
        row.pack(side='top',padx=30)
        self.develop.pack(side='top')

        #save buttton   
        row = tk.Frame(self.frame.scrollable_frame)
        but = tk.Button(row,text='Save',font=button_font,width=20,command=lambda:self.postData(master,flag))
        row.pack(side='top')
        but.pack(side='top')

        #back button
        if flag == 'edit':
            row = tk.Frame(self.frame.scrollable_frame)
            but = tk.Button(row, text='Back', font=button_font, width=20, command=lambda:self.goToMainMenu(master))
            row.pack(side='top',pady=10)
            but.pack(side='top')

    #function to go back to main menu frame
    def goToMainMenu(self, master):
        from main_menu import MainMenuFrame
        self.frame.destroyMe()
        master.switch_frame(MainMenuFrame)

    #function to send post data to server
    def postData(self,master,flag):

        offender_id = None
        if isinstance(self.master.current_offender,dict):
            offender_id = self.master.current_offender['offender_id']
        else:
            offender_id = self.master.current_offender
        
        data = {
            'offender_id' : offender_id,
            'health'      : self.health.get("1.0",'end'),
            'developmental': self.develop.get("1.0", 'end')
        }

        print(json.dumps(data))

        r = requests.post('http://localhost/CorrectionalServices/API/health_developmental.php',json.dumps(data)).json()

        print('\nResponse from server\n')
        print(r)

        if r['success'] == 1:
            
            if flag == 'new':
                self.frame.destroyMe()
                master.switch_frame(QuaterlyReviewsFrame)
            else:
                mb.showinfo('Notice', r['message'])
        else:
            mb.showinfo('Notice', f"{r['message']}")

    #function to populate widgets for editing and viewing
    def populateWidgets(self, master):

        offender_id = None
        if isinstance(self.master.current_offender,dict):
            offender_id = self.master.current_offender['offender_id']
        else:
            offender_id = self.master.current_offender
        
        data = {'offender_id' : offender_id}

        r = requests.post('http://localhost/CorrectionalServices/API/getters/get_health_devel_data.php',json.dumps(data)).json()

        print('\nResponse from server')
        print(r)

        if r['success'] == 1:
            print(r['message'])

            self.health.insert('1.0', r['health'])
            self.develop.insert('1.0', r['developmental'])
            print('populating complete.')

        else: 
            mb.showinfo('Notice', r['message'])