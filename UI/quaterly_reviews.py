import tkinter as tk
import tkinter.messagebox as mb
import datetime
import requests
import json

from constants import *
from scrollable_frame import *
from record_of_contact import *

class QuaterlyReviewsFrame(tk.Frame):

    def __init__(self,master, flag='new'):
        tk.Frame.__init__(self,master)

        self.frame = ScrollableFrame(master)
        
        self.buildWidgets(master, flag)
        
        if flag == 'edit':
            print('Retrieving offender data from database to display')
            self.populateWidgets(master)

        self.frame.pack()

    
    def buildWidgets(self, master,flag):
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row, text='CASE ASSESMENT / QUATERLY REVIEWS',font=label_title_font)
        row.pack(side='top',pady=40)
        lab.pack(side='top')

        if flag == 'edit':
            
            row = tk.Frame(self.frame.scrollable_frame)
            lab = tk.Label(row, text='Previous Records:',font=label_font)
            row.pack(side='top')
            lab.pack(side='top')

            #listbox to view older quaterly reviews
            row = tk.Frame(self.frame.scrollable_frame)
            self.case_listbox = tk.Listbox(row, relief='sunken',width=80)
            self.sbar = tk.Scrollbar(row)
            self.sbar.config(command=self.case_listbox.yview)
            self.case_listbox.config(yscrollcommand=self.sbar.set)
            row.pack(side='top')
            self.sbar.pack(side='right',fill='y')
            self.case_listbox.pack(side='left',expand='yes',fill='x')


        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row, text='Add New Record:',font=label_font)
        row.pack(side='top',pady=15)
        lab.pack(side='top')

        row = tk.Frame(self.frame.scrollable_frame)
        self.review = tk.Text(row,bg='white',wrap=tk.WORD,font=entry_font,width=60,height=10)
        row.pack(side='top',padx=30,pady=20)
        self.review.pack(side='top')
        
        row = tk.Frame(self.frame.scrollable_frame)
        but = tk.Button(row,text='Add',font=button_font,width=20,command=lambda:self.addReview(master, flag))
        row.pack(side='top')
        but.pack(side='top')

        #skip button
        if flag == 'new':
            row = tk.Frame(self.frame.scrollable_frame)
            skip = tk.Button(row,text='Skip',font=button_font,width=20,command=lambda:self.skipReviews(master))
            row.pack(side='top')
            skip.pack(side='top')

        #back button
        if flag == 'edit':
            row = tk.Frame(self.frame.scrollable_frame)
            back = tk.Button(row, text='Back', width=20,font=button_font,command=lambda:self.goToMainMenu(master))
            row.pack(side='top',pady=15)
            back.pack(side='top')

    #handles going back to main menu frame
    def goToMainMenu(self, master):
        from main_menu import MainMenuFrame
        self.frame.destroyMe()
        master.switch_frame(MainMenuFrame)

    #function to send post data containing review
    def addReview(self,master, flag):
        
        offender_id = None
        if isinstance(self.master.current_offender,dict):
            offender_id = self.master.current_offender['offender_id']
        else:
            offender_id = self.master.current_offender
        
        data = {
            'offender_id' : offender_id,
            'review'      : self.review.get("1.0", 'end') 
        }

        print(json.dumps(data))

        r = requests.post('http://localhost/CorrectionalServices/API/quaterly_reviews.php',json.dumps(data)).json()

        print('\nResponse from server:\n')
        print(r)

        if r['success'] == 1:

            if flag == 'new':
                self.frame.destroyMe()
                master.switch_frame(RecordOfContactFrame)
            else:
                mb.showinfo('Notice',f"{r['message']}")

        else:
            mb.showinfo('Notice',f"{r['message']}")

    #function to populate widgets
    def populateWidgets(self,master):
        offender_id = None
        if isinstance(self.master.current_offender,dict):
            offender_id = self.master.current_offender['offender_id']
        else:
            offender_id = self.master.current_offender

        data = {'offender_id' : offender_id}
        print(json.dumps(data))

        r = requests.post('http://localhost/CorrectionalServices/API/getters/get_case_assessment_data.php',json.dumps(data)).json()

        print('\nResponse from server')
        print(r)

        if r['success'] == 1:

            for key, value in enumerate(r['case_assess']):
                value['date_added'] = datetime.datetime.strptime(value['date_added'],"%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y')
                self.case_listbox.insert(key, f"{value['date_added']}: \n{value['review']}")
            print('populating complete')
        else: 
            mb.showinfo('Notice',r['message'])

    def skipReviews(self,master):
        self.frame.destroyMe()
        master.switch_frame(RecordOfContactFrame)

