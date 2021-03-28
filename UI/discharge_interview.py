import tkinter as tk
import tkinter.messagebox as mb
import json
import requests
import datetime

from constants import *
from scrollable_frame import *
from completion_report import *

class DischargeInterviewFrame(tk.Frame):

    def __init__(self, master, flag='new'):
        tk.Frame.__init__(self,master)

        self.frame = ScrollableFrame(master)

        self.buildWidgets(master,flag)
        if flag == 'edit':
            print('Retrieving offender data from database to display')
            self.populateWidgets(master, flag)

        self.getAvailableData(master,flag)
        self.frame.pack()

    def buildWidgets(self, master, flag):
        #title
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row, text='REHABILITATION AND RE-INTEGRATION \nOFFICER DISCHARGE INTERVIEW',font=label_title_font)
        row.pack(side='top')
        lab.pack(side='top')

        #fullnames definition
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row,text='FULLNAMES',width=25,font=label_font,relief='ridge')
        self.fullnames = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top',pady=15)
        lab.pack(side='left')
        self.fullnames.pack(side='right')

        #sex definition
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row, text='SEX',font=label_font,width=25,relief='ridge')
        self.sex = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top',pady=15)
        lab.pack(side='left')
        self.sex.pack(side='right')

        #date of birth definition
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row,text='DATE OF BIRTH',width=25,font=label_font,relief='ridge')
        self.dob = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top',pady=15)
        lab.pack(side='left')
        self.dob.pack(side='right')

        #age definition
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row,text='AGE',font=label_font,width=25,relief='ridge')
        self.age = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top',pady=15)
        lab.pack(side='left')
        self.age.pack(side='right')

        #place of residence title
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='PLACE OF RESIDENCE',font=label_title_font)
        row.pack(side='top',pady=10)
        lab.pack(side='top')

        #region definition
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='REGION',font=label_font,width=25,relief='ridge')
        self.region = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top',pady=5)
        lab.pack(side='left')
        self.region.pack(side='right')

        #inkhundla definition
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='INKHUNDLA',font=label_font,width=25,relief='ridge')
        self.inkhundla = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top',pady=5)
        lab.pack(side='left')
        self.inkhundla.pack(side='right')

        #umphakatsi definition
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='UMPHAKATSI',font=label_font,width=25,relief='ridge')
        self.umphakatsi = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top',pady=5)
        lab.pack(side='left')
        self.umphakatsi.pack(side='right')
        
        #chief definition
        row = tk.Frame(big_row)
        lab = tk.Label(row, text='CHIEF',font=label_font, width=25,relief='ridge')
        self.chief = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top',pady=5)
        lab.pack(side='left')
        self.chief.pack(side='right')

        #indvuna definition
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='INDVUNA',font=label_font,width=25,relief='ridge')
        self.indvuna = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top',pady=5)
        lab.pack(side='left')
        self.indvuna.pack(side='right')

        big_row.pack(side='top',pady=20)

        #date of release definition
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='DATE OF RELEASE',font=label_font,width=25,relief='ridge')
        self.date_of_release = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top',pady=15)
        lab.pack(side='left')
        self.date_of_release.pack(side='right')

        row = tk.Frame(big_row)
        hint= tk.Label(row, text='date format(dd-mm-yyyy)',font=hint_font)
        row.pack(side='top')
        hint.pack(side='top')

        big_row.pack(side='top',pady=20)

        #release address definition
        big_row = tk.Frame(self.frame.scrollable_frame)
        first_row = tk.Frame(big_row)
        row = tk.Frame(first_row)
        lab = tk.Label(row,text='RELEASE ADDRESSS',font=label_title_font)
        row.pack(side='top')
        lab.pack(side='top')

        row = tk.Frame(first_row)
        hint = tk.Label(row,text='if different from above',font=hint_font)
        row.pack(side='top')
        hint.pack(side='top')
        first_row.pack(side='top',pady=10)

        #release region
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='REGION',font=label_font,width=25,relief='ridge')
        self.release_region = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top',pady=5)
        lab.pack(side='left')
        self.release_region.pack(side='right')

        #release inkhundla
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='INKHUNDLA',font=label_font,width=25,relief='ridge')
        self.release_inkhundla = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top',pady=5)
        lab.pack(side='left')
        self.release_inkhundla.pack(side='right')

        #release umphakatsi
        row = tk.Frame(big_row)
        lab = tk.Label(row, text='UMPHAKATSI',font=label_font,width=25,relief='ridge')
        self.release_umphakatsi = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top',pady=5)
        lab.pack(side='left')
        self.release_umphakatsi.pack(side='right')

        #release chief
        row = tk.Frame(big_row)
        lab = tk.Label(row, text='CHIEF',font=label_font,width=25,relief='ridge')
        self.release_chief = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top',pady=5)
        lab.pack(side='left')
        self.release_chief.pack(side='right')

        #release indvuna
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='INDVUNA',font=label_font,width=25,relief='ridge')
        self.release_indvuna = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top',pady=5)
        lab.pack(side='left')
        self.release_indvuna.pack(side='right')

        big_row.pack(side='top',pady=20)

        #family members ready? definition
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='ARE FAMILY MEMBERS AWARE\n OF IMPENDING RELEASE / RETURN HOME',font=label_font)
        row.pack(side='top')
        lab.pack(side='top')

        values = {
            "YES" : "YES",
            "NO"  : "NO"
        }
        self.family_ready_var = tk.StringVar()
        row = tk.Frame(big_row)
        row.pack(side='top')
        for (text,value) in values.items():
            tk.Radiobutton(row,text=text,variable=self.family_ready_var,value=value,indicator=0,relief='sunken',width=10).pack(side='left')
        big_row.pack(side='top', pady=20)

        #immediate problems
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row, text='IMMEDIATE PROBLEMS POST RELEASE',font=label_font)
        row.pack(side='top')
        lab.pack(side='top')

        row = tk.Frame(big_row)
        hint = tk.Label(row,text='(include any problems in family /community,\ncaused by release, and likely response of local community)',font=hint_font)
        row.pack(side='top')
        hint.pack(side='top')

        row = tk.Frame(big_row)
        self.post_release_problems = tk.Text(row, bg='white',wrap=tk.WORD,font=entry_font,width=60,height=10)
        row.pack(side='top',padx=30)
        self.post_release_problems.pack(side='top')

        big_row.pack(side='top',pady=30)

        #offender employment post release
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row, text='HAS OFFENDER GOT EMPLOYMENT TO \nCOMMENCE ON RELEASE?',font=label_font)
        row.pack(side='top',pady=15)
        lab.pack(side='top')

        row = tk.Frame(big_row)
        row.pack(side='top')
        self.post_release_employment = tk.StringVar()
        for (text,value) in values.items():
            tk.Radiobutton(row,text=text,variable=self.post_release_employment,value=value,indicator=0,relief='sunken',width=10).pack(side='left')

        row = tk.Frame(big_row)
        lab = tk.Label(row,text='IF NO, WHAT PLANS HAS HE/SHE GOT FOR \nEMPLOYMENT/EDUCATION:',font=label_font)
        row.pack(side='top',pady=15)
        lab.pack(side='top')

        row = tk.Frame(big_row)
        self.employment_plan = tk.Text(row, bg='white',font=entry_font,wrap=tk.WORD,width=60,height=10)
        row.pack(side='top',padx=30)
        self.employment_plan.pack(side='top')
        big_row.pack(side='top',pady=30)

        #clothing definition
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='CLOTHING: HAS OFFENDER GOT\nADEQUATE CLOTHING FOR RELEASE?',font=label_font)
        row.pack(side='top')
        lab.pack(side='top')

        row = tk.Frame(big_row)
        row.pack(side='top')
        self.clothing = tk.StringVar()
        for (text,value) in values.items():
            tk.Radiobutton(row,text=text,value=value,variable=self.clothing,indicator=0,relief='sunken',width=10).pack(side='left')
        big_row.pack(side='top',pady=20)

        #offender request
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='OFFENDER REQUEST:',font=label_font)
        row.pack(side='top')
        lab.pack(side='top')

        row = tk.Frame(big_row)
        self.offender_request = tk.Text(row,bg='white',wrap=tk.WORD,font=entry_font,width=60,height=10)
        row.pack(side='top',padx=30)
        self.offender_request.pack(side='top')
        big_row.pack(side='top',pady=20)

        #after care contact definition
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row, text='DOES OFFENDER REQUIRE AFTER CARE CONTACT:',font=label_font)
        row.pack(side='top')
        lab.pack(side='top')

        row = tk.Frame(big_row)
        hint = tk.Label(row,text='(offer appointment if yes)',font=hint_font)
        row.pack(side='top')
        hint.pack(side='top')

        row = tk.Frame(big_row)
        self.after_care_contact_var = tk.StringVar()
        row.pack(side='top')
        for (text,value) in values.items():
            tk.Radiobutton(row,text=text,variable=self.after_care_contact_var,value=value,indicator=0,relief='sunken',width=10).pack(side='left')
        
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='APPOINTMENT DATE',font=label_font,width=25,relief='ridge')
        self.offered_appointment = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.offered_appointment.pack(side='right')

        big_row.pack(side='top', pady=30)

        #offender problems requiring referal to another agency
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='DOES THE OFFENDER HAVE ANY PROBLEMS THAT\nREQUIRE REFERAL TO ANOTHER AGENCY ?',font=label_font)
        row.pack(side='top')
        lab.pack(side='top')

        row = tk.Frame(big_row)
        self.problems_referal_var = tk.StringVar()
        row.pack(side='top')
        for (text,value) in values.items():
            tk.Radiobutton(row,text=text,value=value,variable=self.problems_referal_var,indicator=0,width=10,relief='sunken').pack(side='left')

        row = tk.Frame(big_row)
        lab = tk.Label(row,text='(if yes, give details)',font=hint_font)
        row.pack(side='top')
        lab.pack(side='top')

        row = tk.Frame(big_row)
        self.problems_referal_details = tk.Text(row, bg='white',wrap=tk.WORD,font=entry_font,width=60,height=10)
        row.pack(side='top',padx=30)
        self.problems_referal_details.pack(side='top')

        big_row.pack(side='top',pady=20)

        #action to be taken by rehabilitation officer
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='ACTION TO BE TAKEN BY REHABILITAION OFFICER:',font=label_font)
        row.pack(side='top')
        lab.pack(side='top')

        row = tk.Frame(big_row)
        self.rehab_officer_actions = tk.Text(row, bg='white',wrap=tk.WORD,font=entry_font,width=60,height=10)
        row.pack(side='top',padx=30)
        self.rehab_officer_actions.pack(side='top')

        big_row.pack(side='top',pady=20)

        #comments and other relevant information
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='COMMENTS OF REHABILITATION OFFICER AND\nOTHER RELEVANT INFORMATION:',font=label_font)
        row.pack(side='top')
        lab.pack(side='top')

        row = tk.Frame(big_row)
        self.comments = tk.Text(row, bg='white',wrap=tk.WORD,font=entry_font,width=60,height=10)
        row.pack(side='top',padx=30)
        self.comments.pack(side='top')
        
        big_row.pack(side='top',pady=20)

        #officer information
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='NAME OF OFFICER',font=label_font,width=25,relief='ridge')
        self.officer_name = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.officer_name.pack(side='right')

        row = tk.Frame(big_row)
        lab = tk.Label(row,text='DATE',font=label_font,width=25,relief='ridge')
        self.officer_date = tk.Entry(row,width=25,font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.officer_date.pack(side='right')

        row = tk.Frame(big_row)
        hint = tk.Label(row, text='date format(dd-mm-yyyy)',font=hint_font)
        row.pack(side='top')
        hint.pack(side='top')

        big_row.pack(side='top',pady=20)

        #save button definition
        row = tk.Frame(self.frame.scrollable_frame)
        but = tk.Button(row, text='Save',font=button_font,width=20,command=lambda:self.postData(master,flag))
        row.pack(side='top')
        but.pack(side='top')

        if flag == 'edit':
            row = tk.Frame(self.frame.scrollable_frame)
            but = tk.Button(row, text='Back', font=button_font, width=20,command=lambda:self.goToMainMenu(master))
            row.pack(side='top',pady=15)
            but.pack(side='top')

    #function to handle going to main menu frame
    def goToMainMenu(self,master):
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
            'date_of_release' : datetime.datetime.strptime(self.date_of_release.get(),'%d-%m-%Y').isoformat(),
            'family_aware' : self.family_ready_var.get(),
            'immediate_problems_post_release' : self.post_release_problems.get('1.0','end'),
            'clothing_availability' : self.clothing.get(),
            'offender_request' : self.offender_request.get('1.0', 'end'),
            'rehab_officer_actions' : self.rehab_officer_actions.get('1.0','end'),
            'comments' : self.comments.get('1.0', 'end'),
            'officer_name' : self.officer_name.get(),
            'officer_date' : datetime.datetime.strptime(self.officer_date.get(),'%d-%m-%Y').isoformat()
        }

        if self.release_region.get() != None or self.release_region.get() != '':
            data['release_region'] = self.release_region.get()

        if self.release_inkhundla.get() != None or self.release_inkhundla.get() != '':
            data['release_inkhundla'] = self.release_inkhundla.get()

        if self.release_umphakatsi.get() != None or self.release_umphakatsi.get() != '':
            data['release_umphakatsi'] = self.release_umphakatsi.get()
        
        if self.release_chief.get() != None or self.release_chief.get() != '':
            data['release_chief'] = self.release_chief.get()
        
        if self.release_indvuna.get() != None or self.release_indvuna.get() != '':
            data['release_indvuna'] = self.release_indvuna.get()

        if self.post_release_employment.get() == 'NO':
            data['plans_for_employment_education'] = self.employment_plan.get('1.0','end')

        if self.after_care_contact_var.get() == 'YES' and self.offered_appointment.get() != None:
            data['after_care_contact'] = datetime.datetime.strptime(self.offered_appointment.get(),'%d-%m-%Y').isoformat()
        
        if self.problems_referal_var.get() == 'YES' :
            data['problems_referal_details'] = self.problems_referal_details.get('1.0','end')
        
        print(json.dumps(data))

        r = requests.post('http://localhost/CorrectionalServices/API/discharge_interview.php',json.dumps(data)).json()

        print('\nResponse from server')
        print(r)

        if r['success'] == 1:
            
            if flag == 'new':
                self.frame.destroyMe()
                master.switch_frame(CompletionReportFrame)
            else:
                mb.showinfo('Notice', r['message'])
        else: 
            mb.showinfo('Notice',r['message'])

    #function to fetch already available data from database
    def getAvailableData(self, master,flag):

        offender_id = None
        if isinstance(self.master.current_offender,dict):
            offender_id = self.master.current_offender['offender_id']
        else:
            offender_id = self.master.current_offender

        data = {'offender_id' : offender_id}

        r = requests.post('http://localhost/CorrectionalServices/API/getters/get_avail_discharge_data.php', json.dumps(data)).json()

        print('\nResponse from server')
        print(r)

        if r['success'] == 1:
            self.fullnames.insert(0, r['full_names'])
            self.sex.insert(0, r['sex'])
            self.dob.insert(0, datetime.datetime.strptime(r['date_of_birth'],"%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y'))
            self.age.insert(0, r['age'])
            self.region.insert(0, r['region'])
            self.inkhundla.insert(0, r['inkhundla'])
            self.umphakatsi.insert(0, r['umphakatsi'])
            self.chief.insert(0, r['chief'])
            self.indvuna.insert(0, r['indvuna'])
            self.date_of_release.insert(0, datetime.datetime.strptime(r['release_date'],"%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y'))

        else: 
            mb.showinfo('Notice', r['message'])

    #function to populate widgets for edit
    def populateWidgets(self, master, flag):

        offender_id = None
        if isinstance(self.master.current_offender,dict):
            offender_id = self.master.current_offender['offender_id']
        else:
            offender_id = self.master.current_offender
        
        data = {'offender_id' : offender_id}
        r = requests.post('http://localhost/CorrectionalServices/API/getters/get_discharge_data.php',json.dumps(data)).json()
        print('\nResponse from server')
        print(r)

        if r['success'] == 1:

            self.date_of_release.insert(0,datetime.datetime.strptime(r['date_of_release'],"%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y'))
            self.family_ready_var.set(r['family_aware'])
            self.post_release_problems.insert('1.0',r['immediate_problems'])
            self.clothing.set( r['clothing'])
            self.offender_request.insert('1.0',r['offender_request'])
            self.rehab_officer_actions.insert('1.0',r['rehab_officer_actions'])
            self.comments.insert('1.0',r['comments'])
            self.officer_name.insert(0,r['officer_name'])
            self.officer_date.insert(0,datetime.datetime.strptime(r['officer_date'],"%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y'))
            self.release_region.insert(0,r['region'])
            self.release_inkhundla.insert(0,r['inkhundla'])
            self.release_umphakatsi.insert(0, r['umphakatsi'])
            self.release_chief.insert(0,r['chief'])
            self.release_indvuna.insert(0,r['indvuna'])
            
            if r['plans_for_employment'] != None:
                self.post_release_employment.set('YES')
                self.employment_plan.insert('1.0',r['plans_for_employment'])
            else:
                self.post_release_employment.set('NO')

            if r['after_care_contact'] != None:
                self.after_care_contact_var.set('YES')
                self.offered_appointment.insert(0, datetime.datetime.strptime(r['after_care_contact'],"%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y'))
            else:
                self.after_care_contact_var.set('NO')

            if r['problems_referal'] != None:
                self.problems_referal_var.set('YES')
                self.problems_referal_details.insert('1.0',r['problems_referal'])
            else:
                self.problems_referal_var.set('NO')

            print('Populating complete.')
        else: 
            mb.showinfo('Notice', r['message'])