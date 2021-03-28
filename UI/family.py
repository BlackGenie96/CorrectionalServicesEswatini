import tkinter as tk
import tkinter.messagebox as mb
import requests
import json
from scrollable_frame import *
from home_education import *
from constants import *

class FamilyFrame(tk.Frame):

    def __init__(self,master, flag='new'):
        tk.Frame.__init__(self,master)

        self.frame = ScrollableFrame(master)

        if flag == 'new':
            self.buildWidgets(master)
        elif flag == 'edit':
            self.buildWidgets(master)
            self.populateWidgets(master)
            print('Retrieving offender data from database to display')

        self.master = master

        #defining save button to send data to database
        row = tk.Frame(self.frame.scrollable_frame)
        but = tk.Button(row,text='Save',font=button_font,width=20,command=lambda:self.sendPostData(flag))
        row.pack(side='top', pady=20)
        but.pack(side='top')

        #defining back button to go back to main menu
        if flag == 'edit':
            row = tk.Frame(self.frame.scrollable_frame)
            but = tk.Button(row, text='Back', font=button_font, width=20,command=lambda:self.goBackToMainMenu(master))
            row.pack(side='top',pady=10)
            but.pack(side='top')

        self.frame.pack()

    #function to go back to main menu
    def goBackToMainMenu(self,master):
        from main_menu import MainMenuFrame
        self.frame.destroyMe()
        master.switch_frame(MainMenuFrame)

    #function to handle sending data to database server
    def sendPostData(self,flag):
 
        offender_id = None
        if isinstance(self.master.current_offender,dict):
            offender_id = self.master.current_offender['offender_id']
        else:
            offender_id = self.master.current_offender

        family_data = {
            'religion' : self.religion.get(),
            'marital_status' : self.marital_status.get(),
            'family' : self.family_list_values,
            'offender_id' : offender_id
        }

        if self.marital_status.get() != "Single" or self.marital_status.get() != "SINGLE" or self.marital_status.get() != "single" or self.marital_status.get() != None:
            family_data['marriage_type'] = self.marriage_variable.get()

        print(family_data)

        try:
            r = requests.post('http://localhost/CorrectionalServices/API/fam_religion.php',json.dumps(family_data)).json()
        except json.decoder.JSONDecodeError:
            print("Something wrong here")

        print("\nResponse from server\n")
        print(json.dumps(r))

        if r['success'] == 1:
            print(r['message'])
            
            if flag == 'new':
                self.frame.destroyMe()
                self.master.switch_frame(HomeEducationFrame)
            elif flag == 'edit':
                mb.showinfo('Notice',r['message'])
        else:
            print(r['message'])

            mb.showinfo('Notice',r['message'])

    #function to delete family member in family listbox
    def deleteMember(self,event):
        idx = self.family_list.curselection()[0]
        self.family_list.delete(idx)
        del self.family_list_values[idx]
    
    #function to build widgets
    def buildWidgets(self,master):
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row,text='CLIENT PROFILE CONTINUED',font=label_title_font)
        row.pack(side='top', pady=20)
        lab.pack(side='top')

        #religion definition
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row,text='RELIGION',font=label_font, width=20,relief='ridge')
        self.religion = tk.Entry(row,width=35, font=entry_font,relief='sunken')
        row.pack(side='top',pady=10)
        lab.pack(side='left')
        self.religion.pack(side='right')

        #marital status definition
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row, text='MARITAL STATUS',font=label_font, width=20, relief='ridge')
        self.marital_status = tk.Entry(row, width=35, font=entry_font, relief='sunken')
        row.pack(side='top',pady=10)
        lab.pack(side='left')
        self.marital_status.pack(side='right')

        #marrige type radio buttons
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row, text='MARRIAGE TYPE',font=label_font,width=20,relief='ridge')
        self.marriage_values = {
            'Traditional' : 'Traditional Marriage',
            'Civil Marriage'       : 'Civil Marriage'
        }
        self.marriage_variable = tk.StringVar()
        row.pack(side='top',pady=10)
        lab.pack(side='left')
        for (text,value) in self.marriage_values.items():
            tk.Radiobutton(row,text=text,variable=self.marriage_variable,value=value,indicator=0,width=21,relief='sunken').pack(side='right',padx=3)

        #family definition
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row, text='FAMILY',font=label_title_font)
        row.pack(side='top',pady=15)
        lab.pack(side='top')

        #member name definition
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row,text='NAME',font=label_font,width=20,relief='ridge')
        self.member_name = tk.Entry(row,width=35, font=entry_font,relief='sunken')
        row.pack(side='top', pady=10)
        lab.pack(side='left')
        self.member_name.pack(side='right')

        #age definition
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row,text='AGE',font=label_font,width=20,relief='ridge')
        self.member_age = tk.Entry(row,width=35,font=entry_font,relief='sunken')
        row.pack(side='top', pady=10)
        lab.pack(side='left')
        self.member_age.pack(side='right')

        #relation definition
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row,text='RELATIONSHIP',font=label_font,width=20,relief='ridge')
        self.member_relationship = tk.Entry(row,width=35,font=entry_font,relief='sunken')
        row.pack(side='top', pady=10)
        lab.pack(side='left')
        self.member_relationship.pack(side='right')

        #add button definition
        tk.Button(self.frame.scrollable_frame,text='Add', font=button_font,command=lambda:self.addToList()).pack(pady=15)

        #build listbox
        row = tk.Frame(self.frame.scrollable_frame)
        self.sbar = tk.Scrollbar(row)
        self.family_list = tk.Listbox(row,relief=tk.SUNKEN,width=60)
        self.sbar.config(command=self.family_list.yview)
        self.family_list.config(yscrollcommand=self.sbar.set)
        self.family_list.bind('<Double-1>',self.deleteMember)
        row.pack(side='top')
        self.sbar.pack(side='right', fill='y')
        self.family_list.pack(side='left',expand='yes', fill='x')
        self.family_list_values = []

        #delete hint 
        row = tk.Frame(self.frame.scrollable_frame)
        hint = tk.Label(row, text='hint: Double click on list item to remove from list',font=hint_font)
        row.pack(side='top')
        hint.pack(side='top')

    #handle adding family member to list
    def addToList(self):
        #begin counter at 0
        self.counter = 0

        #get the variable
        name = self.member_name.get()
        age = self.member_age.get()
        relation = self.member_relationship.get()

        print(f'I am adding {name} : {age} : {relation}')
        self.family_list.insert(self.counter, f"Name:{name}        Age:{age}       Relationship:{relation}")
        self.family_list_values.append({
            'name' : name,
            'age'  :age,
            'relationship':relation
        })
        self.counter += 1
        self.member_name.delete(0, 'end')
        self.member_age.delete(0, 'end')
        self.member_relationship.delete(0, 'end')
        self.member_name.focus_set()

    #function to populate 
    def populateWidgets(self, master):

        offender_id = None
        if isinstance(self.master.current_offender,dict):
            offender_id = self.master.current_offender['offender_id']
        else:
            offender_id = self.master.current_offender


        data = {'offender_id': offender_id}
        
        print(json.dumps(data))

        r = requests.post('http://localhost/CorrectionalServices/API/getters/get_family_data.php',json.dumps(data)).json()

        print('Response data')
        print(r)

        if r['success'] == 1:
            print(r['message'])

            self.religion.insert(0,r['religion'])
            self.marital_status.insert(0,r['marital_status'])
            self.marriage_variable.set(r['marriage_type'])

            for (key,value) in enumerate(r['family']):
                self.family_list_values.append(value)
                self.family_list.insert(key, f"Name:{value['name']}        Age:{value['age']}       Relationship:{value['relationship']}")
            
            print('Family populated')
        
        else :
            mb.showinfo('Notice',r['message'])