import tkinter as tk
import tkinter.messagebox as mb
import requests
import json

from constants import *
from main_menu import *

class RetrieveOffenderFrame(tk.Frame):

    def __init__(self, master, flag='new'):
        tk.Frame.__init__(self, master)
        
        self.buildWidgets(master)

    
    def buildWidgets(self, master):
        row = tk.Frame(self)
        lab = tk.Label(row, text='FILL ONE OR BOTH OF THE FIELDS\nTO SEARCH FOR OFFENDER',font=label_title_font)
        row.pack(side='top',padx='30',pady=25)
        lab.pack(side='top')

        #gaol number definition
        row = tk.Frame(self)
        lab = tk.Label(row, text='GAOL NUMBER',font=label_font, width=20,relief='ridge')
        self.gaol_number = tk.Entry(row,width=20,font=entry_font,relief='sunken')
        row.pack(side='top', pady=10)
        lab.pack(side='left')
        self.gaol_number.pack(side='right')
        self.gaol_number.focus_set()

        #id number definition
        row = tk.Frame(self)
        lab = tk.Label(row, text='ID NUMBER',font=label_font, width=20, relief='ridge')
        self.id_number = tk.Entry(row, width=20,font=entry_font, relief='sunken')
        row.pack(side='top',pady=10)
        lab.pack(side='left')
        self.id_number.pack(side='right')

        #search button definition
        row = tk.Frame(self)
        but = tk.Button(row, text='Search', font=button_font, width=20, command=lambda:self.searchForOffender(master))
        row.pack(side='top',pady=20)
        but.pack(side='top')

    def searchForOffender(self, master):
        data = {}
        
        if self.id_number.get() != None or self.id_number.get() != '':
            data['id_number'] = self.id_number.get()

        if self.gaol_number.get() != None or self.gaol_number.get() != '':
            data['gaol_number'] = self.gaol_number.get()

        print(json.dumps(data))

        r = requests.post('http://localhost/CorrectionalServices/API/retrieve_offender.php', json.dumps(data)).json()   

        print('\nResponse from server:\n')
        print(r)
        
        if r['success'] == 1:
            #save offender data
            master.current_offender = {
                'name'             : r['name'],
                'surname'          : r['surname'],
                'id_number'        : r['id_number'],
                'gaol_number'      : r['gaol_number'],
                'offender_id'      : r['offender_id']
            }

            master.switch_frame(MainMenuFrame)
        elif r['success'] == 0:
            mb.showinfo('Notice',f"{r['message']}")
