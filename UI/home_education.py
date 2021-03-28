import tkinter as tk
import tkinter.messagebox as mb
import requests
import datetime
import json

from scrollable_frame import *
from employment import *
from constants import *
from main_menu import *

class HomeEducationFrame(tk.Frame):
    
    def __init__(self,master, flag='new'):
        tk.Frame.__init__(self,master)
        self.frame = ScrollableFrame(master)

        if flag == 'new':
            self.buildWidgets(master,flag)
        elif flag == 'edit':
            self.buildWidgets(master,flag)
            self.populateWidgets(master)

        self.frame.pack()
    
    def buildWidgets(self,master, flag):
        #defining Home environment widgets
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row,text='HOME ENVIRONMENT',font=label_title_font)
        row.pack(side='top',pady=20)
        lab.pack(side='top')

        #home conditions definition
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='HOME CONDITIONS',font=label_font)
        row.pack(side='top',pady=15)
        lab.pack(side='top')

        row = tk.Frame(big_row)
        self.home_conditions = tk.Text(row, bg='white', wrap=tk.WORD,font=entry_font,width=60, height=5)
        row.pack(side='top')
        self.home_conditions.pack(side='top')

        big_row.pack() 

        #community standing definition
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row, text='COMMUNITY STANDING',font=label_font)
        row.pack(side='top',pady=15)
        lab.pack(side='top')

        row = tk.Frame(big_row)
        self.community_standing = tk.Text(row,bg='white',wrap=tk.WORD,font=entry_font,width=60,height=5)
        row.pack(side='top')
        self.community_standing.pack(side='top')
        big_row.pack()

        #Education record widget definitions
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row, text='EDUCATIONAL RECORD',font=label_title_font)
        row.pack(side='top', pady=25)
        lab.pack(side='top')

        #name of school definition
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row, text='NAME OF SCHOOL',font=label_font,width=20,relief='ridge')
        self.school_name = tk.Entry(row, width=30,font=entry_font,relief='sunken')
        row.pack(side='top',padx=30)
        lab.pack(side='left')
        self.school_name.pack(side='right')

        #dates definitions
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='DATES(yyyy - yyyy)',font=label_font,relief='ridge',width=20)
        self.date_from = tk.Entry(row,width=12,font=entry_font,relief='sunken')
        dash = tk.Label(row,text='-',font=('Bold',17),width=3)
        self.date_to = tk.Entry(row,width=12,font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.date_to.pack(side='right')
        dash.pack(side='right')
        self.date_from.pack(side='right')
        
        #qualification/grade/form definition
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='QUALIFICATION',font=label_font,width=20,relief='ridge')
        self.qualification = tk.Entry(row,width=30, font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.qualification.pack(side='right')

        big_row.pack(side='top')
        #add button
        tk.Button(self.frame.scrollable_frame,text='Add',font=button_font,command=lambda: self.addToList()).pack(side='top',pady=20)

        row = tk.Frame(self.frame.scrollable_frame)
        self.edu_list = tk.Listbox(row,relief='sunken',width=80)
        self.sbar = tk.Scrollbar(row)
        self.sbar.config(command=self.edu_list.yview)
        self.edu_list.config(yscrollcommand=self.sbar.set)
        self.edu_list.bind("<Double-1>",self.deleteSchool)
        row.pack(side='top')
        self.sbar.pack(side='right',fill='y')
        self.edu_list.pack(side='left',expand='yes',fill='x')
        self.edu_list_values = []

        #delete hint 
        row = tk.Frame(self.frame.scrollable_frame)
        hint = tk.Label(row, text='hint: Double click on list item to remove from list',font=hint_font)
        row.pack(side='top')
        hint.pack(side='top')

        #save button definition
        row = tk.Frame(self.frame.scrollable_frame)
        but = tk.Button(row, text='Save',font=button_font,width=20,command=lambda: self.sendPostData(master,flag))
        row.pack(side='top',pady=5)
        but.pack(side='top')

        #back button
        if flag == 'edit':
            row = tk.Frame(self.frame.scrollable_frame)
            but = tk.Button(row, text='Back', font=button_font, width=20, command=lambda:self.goToMainMenu(master))
            row.pack(side='top',pady=15)
            but.pack(side='top')

    #function to handle going back to main menu frame
    def goToMainMenu(self,master):
        self.frame.destroyMe()
        master.switch_frame(MainMenuFrame)

    #function to handle deleting items from list
    def deleteSchool(self, event):
        idx = self.edu_list.curselection()[0]
        self.edu_list.delete(idx)
        del self.edu_list_values[idx]

    #function to send home education data to database server
    def sendPostData(self,master,flag):
       
        offender_id = None
        if isinstance(self.master.current_offender,dict):
            offender_id = self.master.current_offender['offender_id']
        else:
            offender_id = self.master.current_offender

        
        data = {
            'home' : self.home_conditions.get('1.0','end'),
            'community': self.community_standing.get('1.0','end'),
            'education_record' : self.edu_list_values,
            'offender_id' : offender_id
        }

        print(json.dumps(data))

        r = requests.post('http://localhost/CorrectionalServices/API/home_education.php',json.dumps(data)).json()

        print("\nResponse from server: \n")
        print(r)

        if r['success'] == 1:
            #go to employment record frame
            print(f"{r['message']}")

            if flag != 'edit':
                self.frame.destroyMe()
                master.switch_frame(EmploymentFrame)
            else:
                mb.showinfo('Notice',r['message'])
        elif r['success'] == 0:
            mb.showinfo('Notice', f"{r['message']}")

    #function to populate widgets
    def populateWidgets(self, master):
        offender_id = None
        if isinstance(self.master.current_offender,dict):
            offender_id = self.master.current_offender['offender_id']
        else:
            offender_id = self.master.current_offender

        data = {'offender_id' : offender_id}

        r = requests.post('http://localhost/CorrectionalServices/API/getters/get_home_education_data.php', json.dumps(data)).json()

        print("\nResponse from server")
        print(r)

        if r['success'] == 1:
            self.home_conditions.insert('1.0',r['home'])
            self.community_standing.insert('1.0', r['community'])
            
            for (key, value) in enumerate(r['edu_list']):
                value['date_from'] = datetime.datetime.strptime(value['date_from'],"%Y-%m-%d %H:%M:%S").strftime('%Y')
                value['date_to'] = datetime.datetime.strptime(value['date_to'],"%Y-%m-%d %H:%M:%S").strftime('%Y')
                self.edu_list_values.append(value)
                self.edu_list.insert(key, f"{value['school_name']} ==> {value['date_from']} - {value['date_to']} ==> {value['qualification']}")
            
            print("Widgets populated")
        else: 
            mb.showinfo('Notice', r['message'])
    

    #function to add record to list
    def addToList(self):
        self.counter = 0
        self.edu_list.insert(self.counter,f"{self.school_name.get()} ==> {self.date_from.get()} - {self.date_to.get()} ==> {self.qualification.get()}")
        self.edu_list_values.append({
            'school_name' :self.school_name.get(),
            'date_from' : datetime.datetime.strptime(f"01-01-{self.date_from.get()}", "%d-%m-%Y").isoformat(),
            'date_to' : datetime.datetime.strptime(f"31-12-{self.date_to.get()}", "%d-%m-%Y").isoformat(),
            'qualification' : self.qualification.get()
        })

        self.counter += 1
        self.school_name.delete(0, 'end')
        self.date_from.delete(0, 'end')
        self.date_to.delete(0, 'end')
        self.qualification.delete(0, 'end')
        self.school_name.focus_set()
