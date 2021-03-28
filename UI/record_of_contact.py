import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb
import datetime
import json
import requests

from constants import *
from scrollable_frame import *
from discharge_interview import *

class RecordOfContactFrame(tk.Frame):

    def __init__(self,master, flag='new'):
        tk.Frame.__init__(self,master)

        self.frame = ScrollableFrame(master)

        self.buildWidgets(master,flag)
        
        if flag == 'edit':
            print('Retrieving offender data from database to display')
            self.populateWidgets(master, flag)

        self.frame.pack(pady=50)

    def buildWidgets(self, master, flag):
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row, text='RECORD OF CONTACT',font=label_title_font)
        row.pack(side='top')
        lab.pack(side='top')

        #date definition
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='DATE',font=label_font,width=22,relief='ridge')
        self.date = tk.Entry(row,width=35,font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.date.pack(side='right')

        row = tk.Frame(big_row)
        hint = tk.Label(row,text='date format(dd-mm-yyyy)',font=hint_font)
        row.pack(side='top')
        hint.pack(side='top')
        big_row.pack(side='top',padx=15)

        #nature of contact/ interview definition
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row, text='NATURE OF INTERVIEW',font=label_font,width=22,relief='ridge')
        self.nature = tk.Entry(row,width=35, font=entry_font,relief='sunken')
        row.pack(side='top',pady=20)
        lab.pack(side='left')
        self.nature.pack(side='right')

        #problems identified definition
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row, text='PROBLEMS IDENTIFIED',font=label_font,width=22,relief='ridge')
        self.problems = tk.Entry(row,width=35, font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.problems.pack(side='right')

        row = tk.Frame(big_row)
        hint = tk.Label(row,text='if more than one, separate using semi-colon(;)',font=hint_font)
        row.pack(side='top')
        hint.pack(side='top')
        big_row.pack(side='top')

        #tentative action
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row, text='TENTATIVE ACTION',font=label_font,width=22,relief='ridge')
        self.tentative = tk.Entry(row,width=35, font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.tentative.pack(side='right')

        #final action
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row,text='FINAL ACTION',font=label_font,width=22,relief='ridge')
        self.final_action = tk.Entry(row,width=35, font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.final_action.pack(side='right')

        #save button
        row = tk.Frame(self.frame.scrollable_frame)
        but = tk.Button(row,text='Save',width=20,font=button_font,command=lambda:self.postData(master, flag))
        row.pack(side='top')
        but.pack(side='top')

        #clear button
        row = tk.Frame(self.frame.scrollable_frame)
        but = tk.Button(row, text='Clear', width=20, font=button_font,command=lambda:self.clearData(master))
        row.pack(side='top',pady=15)
        but.pack(side='top')

        if flag == 'edit':

            row = tk.Frame(self.frame.scrollable_frame)
            but = tk.Button(row, text='Back',font=button_font, width=20, command=lambda:self.goToMainMenu(master))
            row.pack(side='top',pady=15)
            but.pack(side='top')

            #self.treeview definition for record of contact
            row = tk.Frame(self.frame.scrollable_frame)
            self.treev = ttk.Treeview(row,selectmode='browse')
            self.treev.pack(side='left')
            verscrlbar = ttk.Scrollbar(row,orient='vertical',command=self.treev.yview)
            row.pack(side='top')
            verscrlbar.pack(side='right',fill='y')
            self.treev.configure(yscrollcommand=verscrlbar.set)

            self.treev['columns'] = ['1','2','3','4','5']
            self.treev['show'] = 'headings'

            self.treev.column('1',width=120,anchor='c')
            self.treev.column('2',width=120,anchor='se')
            self.treev.column('3',width=120, anchor='se')
            self.treev.column('4',width=120,anchor='se')
            self.treev.column('5',width=120,anchor='se')

            self.treev.heading('1', text='Date')
            self.treev.heading('2', text='Nature')
            self.treev.heading('3', text='Problem')
            self.treev.heading('4', text='Tentative')
            self.treev.heading('5', text='Final Action')
            self.tree_list = []
            self.treev.bind('<Button-1>',self.leftClick)
            #self.treev.bind('<ButtonRelease>',self.leftClick)

    def clearData(self, master):
        self.date.delete(0,'end')
        self.nature.delete(0,'end')
        self.problems.delete(0,'end')
        self.tentative.delete(0,'end')
        self.final_action.delete(0,'end')

    #function to handle left click
    def leftClick(self, event):
        item = self.treev.identify_row(event.y)
        info = self.treev.item(item,'values')

        #populate input widgets
        print(info)
        self.date.insert(0,info[0])
        self.nature.insert(0, info[1])
        self.problems.insert(0, info[2])
        self.tentative.insert(0,info[3])
        self.final_action.insert(0, info[4])

    def postData(self, master,flag):

        offender_id = None
        if isinstance(self.master.current_offender,dict):
            offender_id = self.master.current_offender['offender_id']
        else:
            offender_id = self.master.current_offender

        data = {
            "offender_id": offender_id,
            "date" : datetime.datetime.strptime(self.date.get(), "%d-%m-%Y").isoformat(),
            "nature" : self.nature.get(),
            "problem" : self.problems.get(),
            "tentative": self.tentative.get(),
            "final_action": self.final_action.get()
        }

        print(json.dumps(data))
        
        r = requests.post('http://localhost/CorrectionalServices/API/record_of_contact.php',json.dumps(data)).json()

        print("\nResponse from server:")
        print(r)

        if r['success'] == 1:

            if flag == "new":
                self.frame.destroyMe()
                master.switch_frame(DischargeInterviewFrame)
            else:
                mb.showinfo("Notice",f"{r['message']}") 
        else:
            mb.showinfo("Notice",f"{r['message']}")

    #function to populate widgets
    def populateWidgets(self,master,flag):

        offender_id = None
        if isinstance(self.master.current_offender,dict):
            offender_id = self.master.current_offender['offender_id']
        else:
            offender_id = self.master.current_offender

        data = {'offender_id': offender_id}

        r = requests.post('http://localhost/CorrectionalServices/API/getters/get_record_of_contact_data.php',json.dumps(data)).json()
        print("\nResponse from server:")
        print(r)

        if r['success'] == 1:
            
            for key, value in enumerate(r['records']):
                value['date'] = datetime.datetime.strptime(value['date'],"%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y')
                self.treev.insert("", 'end',values=(value['date'],value['nature'],value['problem'],value['tentative'],value['final']))
                self.tree_list.append(value)

            print('population complete.')
        
        else: 
            mb.showinfo('Notice', r['message'])

    #handles going back to main menu frame
    def goToMainMenu(self, master):
        from main_menu import MainMenuFrame
        self.frame.destroyMe()
        master.switch_frame(MainMenuFrame)