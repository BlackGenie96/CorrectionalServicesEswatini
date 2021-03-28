import tkinter as tk
import tkinter.messagebox as mb
import requests
import datetime
import json

from scrollable_frame import *
from health_developmental import *
from constants import *

class EmploymentFrame(tk.Frame):
    def __init__(self,master, flag='new'):
        tk.Frame.__init__(self,master)

        self.frame = ScrollableFrame(master)

        self.buildWidgets(master,flag)
        
        if flag == 'edit':
            self.populateWidgets(master)

        self.frame.pack()


    def buildWidgets(self,master,flag):
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row, text='EMPLOYMENT RECORD',font=label_title_font)
        row.pack(side='top',pady=20)
        lab.pack(side='top')

        #name or address of employer definition
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row, text='NAME/ADDRESS OF EMPLOYER',font=label_font,width=25,relief='ridge')
        self.employer = tk.Entry(row, width=22,relief='sunken',font=entry_font)
        row.pack(side='top',pady=10)
        lab.pack(side='left')
        self.employer.pack(side='right')

        #postion held definition 
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row, text='POSITION', width=25, font=label_font, relief='ridge')
        self.position = tk.Entry(row, width=22, font=entry_font,relief='sunken')
        row.pack(side='top',pady=10)
        lab.pack(side='left')
        self.position.pack(side='right')

        #Date definition
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='DATE(from - to)',width=20, font=label_font, relief='ridge')
        self.date_from = tk.Entry(row,width=15, font=entry_font,relief='sunken')
        dash = tk.Label(row, text='-',width=2,font=hint_font)
        self.date_to = tk.Entry(row,width=15, font=entry_font, relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.date_to.pack(side='right')
        dash.pack(side='right')
        self.date_from.pack(side='right')

        row = tk.Frame(big_row)
        lab = tk.Label(row,text='date format(dd-mm-yyyy)',font=hint_font)
        row.pack(side='top')
        lab.pack(side='top')
        big_row.pack(side='top',pady=10)

        #reason for leaving 
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row, text='REASON FOR LEAVING', width=25, font=label_font,relief='ridge')
        self.leaving_reason = tk.Entry(row,width=22,font=entry_font,relief='sunken')
        row.pack(side='top',pady=10)
        lab.pack(side='left')
        self.leaving_reason.pack(side='right')

        #add button
        row = tk.Frame(self.frame.scrollable_frame)
        but = tk.Button(row,text='Add',width=20,font=button_font,command=lambda: self.addToList())
        row.pack(side='top',pady=15)
        but.pack(side='top')

        #defining listbox
        row = tk.Frame(self.frame.scrollable_frame)
        sbar = tk.Scrollbar(row)
        self.employ_listbox = tk.Listbox(row,relief='sunken',width=80)
        sbar.config(command=self.employ_listbox.yview)
        self.employ_listbox.config(yscrollcommand=sbar.set)
        self.employ_listbox.bind('<Double-1>',self.deleteRecord)
        row.pack(side='top')
        sbar.pack(side='right',fill='y')
        self.employ_listbox.pack(side='left',expand='yes',fill='x')
        self.employ_list_values = []

        #delete hint 
        row = tk.Frame(self.frame.scrollable_frame)
        hint = tk.Label(row, text='hint: Double click on list item to remove from list',font=hint_font)
        row.pack(side='top')
        hint.pack(side='top')

        #save button definition
        row = tk.Frame(self.frame.scrollable_frame)
        but = tk.Button(row,text='Save',width=20, font=button_font,command=lambda: self.postData(master,flag))
        row.pack(side='top',pady=15)
        but.pack(side='top')

        #back button definition
        if flag == 'edit':
            row = tk.Frame(self.frame.scrollable_frame)
            but = tk.Button(row, text='Back', width=20, font=button_font,command=lambda:self.goToMainMenu(master))
            row.pack(side='top',pady=10)
            but.pack(side='top')

    #function to delete record
    def deleteRecord(self,event):
        idx = self.employ_listbox.curselection()[0]
        self.employ_listbox.delete(idx)
        del self.employ_list_values[idx]

    #function to go back to main menu frame
    def goToMainMenu(self,master):
        from main_menu import MainMenuFrame
        self.frame.destroyMe()
        master.switch_frame(MainMenuFrame)
        
    def addToList(self):
        self.counter = 0
        self.employ_listbox.insert(self.counter, f"{self.employer.get()}, {self.position.get()}, {self.date_from.get()} - {self.date_to.get()}, Reason: {self.leaving_reason.get()}")
        self.employ_list_values.append({
            'employer'  : self.employer.get(),
            'position'   : self.position.get(),
            'date_from' : datetime.datetime.strptime(self.date_from.get(),"%d-%m-%Y").isoformat(),
            'date_to'   : datetime.datetime.strptime(self.date_to.get(),"%d-%m-%Y").isoformat(),
            'reason'    : self.leaving_reason.get()
        })

        self.counter += 1
        self.employer.delete(0, 'end')
        self.position.delete(0, 'end')
        self.date_from.delete(0, 'end')
        self.date_to.delete(0, 'end')
        self.leaving_reason.delete(0, 'end')
        self.employer.focus_set()

    #function send employment data to database server
    def postData(self,master,flag):

        offender_id = None
        if isinstance(self.master.current_offender,dict):
            offender_id = self.master.current_offender['offender_id']
        else:
            offender_id = self.master.current_offender

        data = {
            'offender_id' : offender_id,
            'records' : self.employ_list_values
        }

        print(json.dumps(data))
        r = requests.post('http://localhost/CorrectionalServices/API/employment.php',json.dumps(data)).json()
        print('\n Response from server \n')
        print(r)

        if r['success'] == 1:
            print(f"{r['message']}")

            if flag == 'new':
                self.frame.destroyMe()
                master.switch_frame(HealthDevelopmentalFrame)
            else:
                mb.showinfo('Notice', r['message'])
        elif r['success'] == 0:
            print(f"{r['error']}")
            mb.showinfo('Notice', f"{r['message']}")

    #function to populate widgets
    def populateWidgets(self,master):
    
        offender_id = None
        if isinstance(self.master.current_offender,dict):
            offender_id = self.master.current_offender['offender_id']
        else:
            offender_id = self.master.current_offender

        data = {'offender_id' : offender_id}

        r = requests.post('http://localhost/CorrectionalServices/API/getters/get_employment_data.php', json.dumps(data)).json()

        print('\nResponse from server')
        print(r)

        if r['success'] == 1:
            print(r['message'])

            for key, value in enumerate(r['employment_records']):
                value['date_from'] = datetime.datetime.strptime(value['date_from'],"%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y')
                value['date_to'] = datetime.datetime.strptime(value['date_to'],"%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y')
                self.employ_listbox.insert(key,f"{value['employer']}, {value['position']}, {value['date_from']} - {value['date_to']}, Reason: {value['reason']}")
                self.employ_list_values.append(value)
        else:
            mb.showinfo('Notice', r['message'])