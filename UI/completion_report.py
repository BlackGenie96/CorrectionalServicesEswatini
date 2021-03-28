import tkinter as tk
import tkinter.messagebox as mb
import requests
import json
import datetime

from constants import *
from scrollable_frame import *

class CompletionReportFrame(tk.Frame):

    def __init__(self,master, flag='new'):
        #super class constructor
        tk.Frame.__init__(self,master)

        #defining local variables
        self.frame = ScrollableFrame(master)

        #checking flag to build appropriate widgets
        self.buildWidgets(master, flag)
        self.getAvailRecords(master)
        
        if flag == 'edit':
            print('Retrieving offender data from database to display')
            self.populateWidgets(master)

        #pack local frame to display all widgets
        self.frame.pack()

    def buildWidgets(self,master, flag):

        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row, text='COMPLETION REPORT',font=label_title_font)
        row.pack(side='top',pady=30)
        lab.pack(side='top')

        #to definition
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row, text='TO',font=label_font,width=25,relief='ridge')
        self.to = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top',pady=10)
        lab.pack(side='left')
        self.to.pack(side='right')

        #criminal case number 
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row,text='CRIMINAL CASE NUMBER',font=label_font,width=25,relief='ridge')
        self.criminal_case_num = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top',pady=10)
        lab.pack(side='left')
        self.criminal_case_num.pack(side='right')

        #offender fullnames
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row, text='OFFENDER FULLNAME',font=label_font,width=25,relief='ridge')
        self.fullnames = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top',pady=10)
        lab.pack(side='left')
        self.fullnames.pack(side='right')

        #date of birth
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='DATE OF BIRTH',width=25,font=label_font,relief='ridge')
        self.date_of_birth = tk.Entry(row, width=25, font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.date_of_birth.pack(side='right')

        row = tk.Frame(big_row)
        hint = tk.Label(row, text='date format(dd-mm-yyyy)',font=hint_font)
        row.pack(side='top')
        hint.pack(side='top')
        big_row.pack(side='top',pady=10)

        #place of residence
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row, text='PLACE OF RESIDENCE',font=label_font)
        row.pack(side='top')
        lab.pack(side='top')

        #region
        row = tk.Frame(big_row)
        lab = tk.Label(row, text='REGION',font=label_font,width=25,relief='ridge')
        self.region = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.region.pack(side='right')

        #inkhundla
        row = tk.Frame(big_row)
        lab = tk.Label(row, text='INKHUNDLA',font=label_font,width=25,relief='ridge')
        self.inkhundla = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.inkhundla.pack(side='right')

        #umphakatsi
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='UMPHAKATSI',font=label_font,width=25,relief='ridge')
        self.umphakatsi = tk.Entry(row,width=25,font=entry_font,relief='sunken')    
        row.pack(side='top')
        lab.pack(side='left')
        self.umphakatsi.pack(side='right')

        #chief
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='CHIEF',font=label_font,width=25,relief='ridge')
        self.chief = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.chief.pack(side='right')

        #indvuna
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='INDVUNA',font=label_font,width=25,relief='ridge')
        self.indvuna = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.indvuna.pack(side='right')

        big_row.pack(side='top',pady=20)

        #offences
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row, text='OFFENCES',font=label_font,width=25,relief='ridge')
        self.offences = tk.Entry(row, width=25,font=entry_font,relief='sunken')
        row.pack(side='top',pady=5)
        lab.pack(side='left')
        self.offences.pack(side='right')

        '''row = tk.Frame(big_row)
        sbar = tk.Scrollbar(row)
        self.offences_list = tk.Listbox(row,relief='sunken',width=60)
        sbar.config(command=self.offences_list.yview)
        self.offences_list.config(yscrollcommand=sbar.set)
        row.pack(side='top')
        sbar.pack(side='right',fill='y')
        self.offences_list.pack(side='left',expand='yes',fill='x')
        self.offences_list_values = []'''


        big_row.pack(side='top',pady=20)

        #court
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row,text='COURT',font=label_font,width=25,relief='ridge')
        self.court_name = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.court_name.pack(side='right')

        #court date
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row, text='COURT DATE',font=label_font,width=25,relief='ridge')
        self.court_date = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.court_date.pack(side='right')

        row = tk.Frame(big_row)
        hint = tk.Label(row,text='date format(dd-mm-yyyy)',font=hint_font)
        row.pack(side='top')
        hint.pack(side='top')

        big_row.pack(side='top',pady=15)

        #sentence
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row, text='SENTECE',font=label_font,width=25,relief='ridge')
        self.sentence = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.sentence.pack(side='right')

        #number of years
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row,text='NUM OF MONTHS/YEARS',font=label_font,width=25,relief='ridge')
        self.num_of_years = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.num_of_years.pack(side='right')

        #date sentence completed
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='SENTENCE COMPLETED',font=label_font,width=25,relief='ridge')
        self.date_sentence_completed = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.date_sentence_completed.pack(side='right')

        row = tk.Frame(big_row)
        hint = tk.Label(row, text='date format(dd-mm-yyyy)',font=hint_font)
        row.pack(side='top')
        hint.pack(side='top')

        big_row.pack(side='top',pady=20)

        #commets
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row, text='COMMENTS',font=label_font)
        row.pack(side='top')
        lab.pack(side='top')

        row = tk.Frame(big_row)
        hint = tk.Label(row, text='(regarding behavior,work performance and overall response)',font=hint_font)
        row.pack(side='top')
        hint.pack(side='top')

        row = tk.Frame(big_row)
        self.comments = tk.Text(row,bg='white',wrap=tk.WORD,width=60, height=10,font=entry_font)
        row.pack(side='top',padx=30)
        self.comments.pack(side='top')

        big_row.pack(side='top',pady=20)

        #reported by
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row,text='REPORT PREPARED BY:',font=label_font,width=25,relief='ridge')
        self.reported_by = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.reported_by.pack(side='right')

        #designation
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row, text='DESIGNATION',font=label_font,width=25,relief='ridge')
        self.designation = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.designation.pack(side='right')

        #date
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row, text='DATE',font=label_font,width=25,relief='ridge')
        self.compilation_date = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.compilation_date.pack(side='right')

        #save button
        row = tk.Frame(self.frame.scrollable_frame)
        but = tk.Button(row,text='Save',font=button_font,width=20,command=lambda:self.postData(master,flag))
        row.pack(side='top',pady=20)
        but.pack(side='top')

        #back button
        if flag == 'edit':
            row = tk.Frame(self.frame.scrollable_frame)
            but = tk.Button(row, text='Back', font=button_font,width=20,command=lambda:self.goToMainMenu(master))
            row.pack(side='top')
            but.pack(side='top')

    #function to handle going to main menu
    def goToMainMenu(self, master):
        from main_menu import MainMenuFrame
        self.frame.destroyMe()
        master.switch_frame(MainMenuFrame)

    def postData(self, master,flag):

        offender_id = None
        if isinstance(self.master.current_offender,dict):
            offender_id = self.master.current_offender['offender_id']
        else:
            offender_id = self.master.current_offender

        data = {
            'offender_id' : offender_id,
            'to': self.to.get(),
            'num_years' : self.num_of_years.get(),
            'sentence_complete' : datetime.datetime.strptime(self.date_sentence_completed.get(),'%d-%m-%Y').isoformat(),
            'comments'  : self.comments.get('1.0','end'),
            'report_by' : self.reported_by.get(),
            'date_created' : datetime.datetime.strptime(self.compilation_date.get(),'%d-%m-%Y').isoformat(),
            'designation' : self.designation.get()
        }

        print(json.dumps(data))
        r = requests.post('http://localhost/CorrectionalServices/API/completion_report.php',json.dumps(data)).json()
        print('\nResponse from server')
        print(r)

        if r['success'] == 1:

            if flag == 'new':
                from firstMenu import FirstMenu
                self.frame.destroyMe()
                master.switch_frame(FirstMenu)
            else:
                mb.showinfo('Notice', r['message'])
        else:
            mb.showinfo('Notice', r['message'])

    def getAvailRecords(self, master):

        offender_id = None   
        if isinstance(self.master.current_offender,dict):
            offender_id = self.master.current_offender['offender_id']
        else:
            offender_id = self.master.current_offender
        
        data = {'offender_id': offender_id} 
        r = requests.post('http://localhost/CorrectionalServices/API/getters/get_avail_completion_report_data.php',json.dumps(data)).json()
        print('\nResponse from server')
        print(r)

        if r['success'] == 1:
            self.criminal_case_num.insert(0,r['criminal_case_number'])
            self.fullnames.insert(0, r['full_names'])
            self.date_of_birth.insert(0, datetime.datetime.strptime(r['date_of_birth'],"%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y'))
            self.region.insert(0, r['region'])
            self.inkhundla.insert(0, r['inkhundla'])
            self.umphakatsi.insert(0, r['umphakatsi'])
            self.chief.insert(0, r['chief'])
            self.indvuna.insert(0, r['indvuna'])
            self.offences.insert(0,r['offences'])
            self.court_name.insert(0, r['court'])
            self.court_date.insert(0, datetime.datetime.strptime(r['court_date'],"%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y'))
            self.sentence.insert(0, r['sentence'])

            print('Populating available complete')
        else:
            mb.showinfo('Notice', r['message'])

    def populateWidgets(self, master):
        offender_id = None   
        if isinstance(self.master.current_offender,dict):
            offender_id = self.master.current_offender['offender_id']
        else:
            offender_id = self.master.current_offender

        data = {'offender_id': offender_id}

        r = requests.post('http://localhost/CorrectionalServices/API/getters/get_completion_report_data.php',json.dumps(data)).json()
        print('\nResponse from server')
        print(r)

        if r['success'] == 1:
            self.to.insert(0,r['to'])
            self.num_of_years.insert(0, r['num_years'])
            self.date_sentence_completed.insert(0, datetime.datetime.strptime(r['date_complete'],"%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y'))
            self.comments.insert('1.0',r['comments'])
            self.reported_by.insert(0, r['report_by'])
            self.designation.insert(0, r['designation'])
            self.compilation_date.insert(0, datetime.datetime.strptime(r['date_created'],"%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y'))

            print('populating extra widgets complete')
        else:
            mb.showinfo('Notice', r['message'])
