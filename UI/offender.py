import tkinter as tk
import tkinter.messagebox as mb
from scrollable_frame import *
import requests
import datetime

from family import *
from constants import *

class OffenderFrame(tk.Frame):
    def __init__(self,master,flag='new'):
        tk.Frame.__init__(self,master)

        #defining local variables
        self.frame = ScrollableFrame(master)

        #check flag value
        if flag == 'new':
            self.buildWidgets(master,flag)
        elif flag == 'edit':
            #get data from database to display
            self.buildWidgets(master,flag)
            self.populateWidgets(master)

        #pack to display all widgets
        self.frame.pack()


    #function to create widgets to create or show offender
    def buildWidgets(self, master,flag):
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row,text='CASE RECORD',font=label_title_font)
        row.pack(side='top',pady=20)
        lab.pack(side='top')

        #C.F definition
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row ,text='C.F.',font=label_font,width=22,relief='ridge')
        self.cf = tk.Entry(row ,width=35,relief='sunken',font=entry_font)
        row.pack(side='top',pady=10)
        lab.pack(side='left')
        self.cf.pack(side='right')

        #Gaol number definition
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row ,text='GAOL NUMBER',font=label_font,width=22,relief='ridge')
        self.gaol_number = tk.Entry(row ,width=15,relief='sunken',font=entry_font)
        self.gaol_but = tk.Button(row, text='Generate',font=button_font,width=20)
        row.pack(side='top',pady=10)
        lab.pack(side='left')
        self.gaol_but.pack(side='right')
        self.gaol_number.pack(side='right')

        #Firstname definition
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row, text='FULL NAMES', font=label_font, width=22, relief='ridge')
        self.full_names = tk.Entry(row,width=35, relief='sunken',font=entry_font)
        row.pack(side='top',pady=10)
        lab.pack(side='left')
        self.full_names.pack(side='right')

        #surname definition
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row,text='SURNAME', font=label_font, width=22, relief='ridge')
        self.surname = tk.Entry(row, width=35, relief='sunken',font=entry_font)
        row.pack(side='top',pady=10)
        lab.pack(side='left')
        self.surname.pack(side='right')

        #sex definition
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row, text="SEX",font=label_font,width=22, relief='ridge')
        row.pack(side='top', pady=10)
        lab.pack(side='left')
        self.sex_values = {
            'Female': 'Female',
            'Male':  'Male'
        }
        self.sex_variable = tk.StringVar()
        for (text, value) in self.sex_values.items():
            tk.Radiobutton(row,text=text, variable=self.sex_variable,value=value,indicator=0,width=18,font=('Bold',12),relief='sunken').pack(side='right')
        
        #date of birth definition
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row ,text='DATE OF BIRTH', font=label_font, width=22,relief='ridge')
        self.date_of_birth = tk.Entry(row,width=35,relief='sunken',font=entry_font)
        row.pack(side='top',)
        lab.pack(side='left')
        self.date_of_birth.pack(side='right')
        
        row = tk.Frame(big_row)
        hint = tk.Label(row,text='date format (dd-mm-yyyy)',font=hint_font)
        row.pack(side='top')
        hint.pack(side='top')
        big_row.pack(side='top',pady=20)

        #age definition
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row,text='AGE', font=label_font, width=22, relief='ridge')
        self.age = tk.Entry(row,width=35,relief='sunken',font=entry_font)
        row.pack(side='top')
        lab.pack(side='left')
        self.age.pack(side='right')

        #id number definition
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row,text='ID NUMBER',font=label_font, width=22, relief='ridge')
        self.id_number = tk.Entry(row,width=35,relief='sunken',font=entry_font)
        row.pack(side='top',pady=15)
        lab.pack(side='left')
        self.id_number.pack(side='right')

        #Place of residence definition
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='PLACE OF RESIDENCE',font=label_title_font)
        row.pack(side='top')
        lab.pack(side='top')

        row = tk.Frame(big_row)
        lab = tk.Label(row,text='REGION',font=label_font,width=22, relief='ridge')
        self.region = tk.Entry(row, width=35, font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.region.pack(side='right')

        #inkhundla definition
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='INKHUNDLA',font=label_font,width=22, relief='ridge')
        self.inkhundla = tk.Entry(row, width=35, font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.inkhundla.pack(side='right')

        #umphakatsi definition
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='UMPHAKATSI',font=label_font,width=22,relief='ridge')
        self.umphakatsi = tk.Entry(row,width=35,font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.umphakatsi.pack(side='right')

        #chief definition
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='CHIEF',font=label_font, width=22, relief='ridge')
        self.chief = tk.Entry(row,width=35, font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.chief.pack(side='right')

        #indvuna definition
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='INDVUNA',font=label_font,width=22, relief='ridge')
        self.indvuna = tk.Entry(row,width=35,font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.indvuna.pack(side='right')
        big_row.pack(side='top',pady=30)
        
        #next of kin name definition
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row, text='NEXT OF KIN (name)',font=label_font,width=22,relief='ridge')
        self.next_of_kin = tk.Entry(row, width=35, font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.next_of_kin.pack(side='right')

        #next of kin phone definition
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='NEXT OF KIN (phone)',font=label_font,width=22,relief='ridge')
        self.next_of_kin_phone = tk.Entry(row,width=35, font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.next_of_kin_phone.pack(side='right')

        big_row.pack(side='top', pady=15)

        #offences definition
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='OFFENCES',font=label_font,width=22,relief='ridge')
        self.offences = tk.Entry(row,width=35,font=entry_font, relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.offences.pack(side='right')

        row = tk.Frame(big_row)
        lab = tk.Label(row,text='If offences are more than one, separate using semi-colon(;)',font=hint_font)
        row.pack(side='top')
        lab.pack(side='top')

        big_row.pack(side='top',pady=15)

        #court definition
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row,text='COURT',font=label_font,width=22,relief='ridge')
        self.court = tk.Entry(row,width=35, font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.court.pack(side='right')

        #court date
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='COURT DATE',font=label_font,width=22,relief='ridge')
        self.court_date = tk.Entry(row,width=35, font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.court_date.pack(side='right')

        row = tk.Frame(big_row)
        hint = tk.Label(row,text='date format (dd-mm-yyyy)',font=hint_font)
        row.pack(side='top')
        hint.pack(side='top')
        big_row.pack(side='top',pady=15)

        #sentence definition
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row,text='SENTENCE',font=label_font,width=22, relief='ridge')
        self.sentence = tk.Entry(row,width=35, font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.sentence.pack(side='right')

        #criminal case number definition
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row,text='CRIMINAL CASE NO.',font=label_font,width=22,relief='ridge')
        self.criminal_case_num = tk.Entry(row,width=35, font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.criminal_case_num.pack(side='right')

        #admitting center definition
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row,text='ADMITTING CENTER',font=label_font,width=22,relief='ridge')
        self.admitting_center = tk.Entry(row,width=35, font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.admitting_center.pack(side='right')

        #date of reception definition
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='DATE OF RECEPTION',font=label_font,width=22,relief='ridge')
        self.date_of_reception = tk.Entry(row,width=35, font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.date_of_reception.pack(side='right')

        row = tk.Frame(big_row)
        hint = tk.Label(row,text='date format (dd-mm-yyyy)',font=hint_font)
        row.pack(side='top')
        hint.pack(side='top')
        big_row.pack(side='top',pady=15)

        #rehabilitation & re-integration officer definition
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row, text='REHABILITAION OFFICER',font=label_font,width=22,relief='ridge')
        self.rehabilitation_officer = tk.Entry(row,width=35,font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.rehabilitation_officer.pack(side='right')

        #E.D.R definition
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row,text='E.D.R',font=label_font,width=22,relief='ridge')
        self.e_d_r = tk.Entry(row,width=35, font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.e_d_r.pack(side='right') 

        #L.D.R definition
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row,text='L.D.R',font=label_font,width=22,relief='ridge')
        self.l_d_r = tk.Entry(row,width=35, font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.l_d_r.pack(side='right')

        #transfer center definition
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row, text='TRANSFER CENTER',font=label_font,width=22,relief='ridge')
        self.transfer_center = tk.Entry(row,width=35, font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.transfer_center.pack(side='right')

        #transfer center date
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='TRANSFER CENTER DATE',font=label_font,width=22,relief='ridge')
        self.transfer_center_date = tk.Entry(row,width=35,font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.transfer_center_date.pack(side='right')

        row = tk.Frame(big_row)
        hint = tk.Label(row,text='date format (dd-mm-yyyy)',font=hint_font)
        row.pack(side='top')
        hint.pack(side='top')

        big_row.pack(side='top', pady=15)

        #actual date of release definition
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='ACTUAL RELEASE DATE',font=label_font,width=22,relief='ridge')
        self.actual_release_date = tk.Entry(row,width=35,font=entry_font,relief='sunken')
        row.pack(side='top')
        lab.pack(side='left')
        self.actual_release_date.pack(side='right')

        row = tk.Frame(big_row)
        hint = tk.Label(row,text='date format (dd-mm-yyyy)',font=hint_font)
        row.pack(side='top')
        hint.pack(side='top')
        big_row.pack(side='top',pady=15)

        #after care/ post sentence assistance requested
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row,text='POST SENTENCE ASSISTANCE',font=label_font,width=27,relief='ridge')
        row.pack(side='top')
        lab.pack(side='left')
        self.post_care_values = {
            'NO' : 0,
            'YES' : 1
        }
        self.post_care_variable = tk.StringVar()
        for (text, value) in self.post_care_values.items():
            tk.Radiobutton(row,text=text,variable=self.post_care_variable,value=value,indicator=0,width=18,relief='sunken').pack(side='right')

        #date case closed definition
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        lab = tk.Label(row,text='DATE CASE CLOSED',font=label_font,width=22,relief='ridge')
        self.date_case_closed = tk.Entry(row,width=35,relief='sunken',font=entry_font)
        row.pack(side='top')
        lab.pack(side='left')
        self.date_case_closed.pack(side='right')

        row = tk.Frame(big_row)
        hint = tk.Label(row,text='date format (dd-mm-yyyy)',font=hint_font)
        row.pack(side='top')
        hint.pack(side='top')
        big_row.pack(side='top',pady=15)

        #save button
        tk.Button(self.frame.scrollable_frame,text='Save',width=20,font=button_font,command=lambda: self.saveOffenderData(master)).pack(ipadx=15,ipady=5,pady=25)

        #back button
        if flag == 'edit':
            tk.Button(self.frame.scrollable_frame,text='Back',width=20,font=button_font,command=lambda:self.goBack(master)).pack(ipadx=15,ipady=5,pady=10)
        elif flag == 'new':
            tk.Button(self.frame.scrollable_frame,text='Back',width=20,font=button_font,command=lambda:self.goBackFirstMenu(master)).pack(ipadx=15,ipady=5,pady=10)

    #handles going back to first menu frame
    def goBackFirstMenu(self, master):
        from firstMenu import FirstMenu
        self.frame.destroyMe()
        master.switch_frame(FirstMenu)

    #handles going back to main menu frame
    def goBack(self, master):
        from main_menu import MainMenuFrame
        self.frame.destroyMe()
        master.switch_frame(MainMenuFrame)

    #handle the button click and save offender info in database
    def saveOffenderData(self,master):
        
        #save data to dictionary
        post_data = {
            'c_f'               : self.cf.get(),
            'gaol_number'       : self.gaol_number.get(),
            'full_names'        : self.full_names.get(),
            'surname'           : self.surname.get(),
            'sex'               : self.sex_variable.get(),
            'date_of_birth'     : datetime.datetime.strptime(self.date_of_birth.get(),"%d-%m-%Y"),
            'age'               : self.age.get(),
            'id_number'         : self.id_number.get(),
            'region'            : self.region.get(),
            'inkhundla'         : self.inkhundla.get(),
            'umphakatsi'        : self.umphakatsi.get(),
            'chief'             : self.chief.get(),
            'indvuna'           : self.indvuna.get(),
            'next_of_kin_name'  : self.next_of_kin.get(),
            'next_of_kin_phone' : self.next_of_kin_phone.get(),
            'offences'          : self.offences.get(),
            'court'             : self.court.get(),
            'sentence'          : self.sentence.get(),
            'criminal_case_num' : self.criminal_case_num.get(),
            'admitting_center'  : self.admitting_center.get(),
            'rehabilitation_officer' : self.rehabilitation_officer.get(),
            'post_sentence_assistance': self.post_care_variable.get(),
            'e_d_r'             : self.e_d_r.get(),
            'l_d_r'             : self.l_d_r.get(),
            'transfer_center'   : self.transfer_center.get(),
            'transfer_center_date': self.transfer_center_date.get(),
            'officer_id'        : master.officer_info['officer_id']
        }

        
        if len(self.court_date.get()) > 0:
            post_data['court_date'] = datetime.datetime.strptime(self.court_date.get(),"%d-%m-%Y")

        if len(self.date_of_reception.get()) > 0:
            post_data['date_of_reception'] = datetime.datetime.strptime(self.date_of_reception.get(), "%d-%m-%Y")

        if len(self.actual_release_date.get()) > 0:
            post_data['actual_release_date'] = datetime.datetime.strptime(self.actual_release_date.get(),"%d-%m-%Y")
        
        if len(self.date_case_closed.get()) > 0:
            post_data['date_case_closed'] = datetime.datetime.strptime(self.date_case_closed.get(),"%d-%m-%Y")

        post_data['data_set'] = '1'
        print(f"{post_data}")

        r = requests.post('http://localhost/CorrectionalServices/API/create_offenders.php', post_data).json()
        
        print('\nResponse from server:\n')
        print(json.dumps(r))

        if r['success'] == 1:
            master.current_offender = r["offender_id"]
            self.frame.destroyMe()
            master.switch_frame(FamilyFrame)
        else:
            if r['family_error'] != None:
                mb.showinfo('Notice', f"{r['family_error']}")
            elif r['error_offender'] != None:
                mb.showinfo('Notice', f"{r['error_offender']}")


    #function to get offender data for viewing and edit 
    def populateWidgets(self, master):

        offender_id = None
        if isinstance(self.master.current_offender,dict):
            offender_id = self.master.current_offender['offender_id']
        else:
            offender_id = self.master.current_offender

        #get data from server
        data = {'id_number' : offender_id}

        r = requests.post('http://localhost/CorrectionalServices/API/getters/get_offender_data.php',json.dumps(data)).json()

        print('Response data')
        print(r)

        if r['success'] == 1:
            print(r['message'])

            self.cf.insert(0,['c_f'])
            self.gaol_number.insert(0,r['gaol_number'])
            self.gaol_but.config(state='disabled')
            self.full_names.insert(0,r['full_names'])
            self.surname.insert(0,r['surname'])
            self.sex_variable.set(r['sex'])
            self.date_of_birth.insert(0,datetime.datetime.strptime(r['date_of_birth'],"%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y'))
            self.age.insert(0,r['age'])
            self.id_number.insert(0,r['id_number'])
            self.region.insert(0,r['region'])
            self.inkhundla.insert(0,r['inkhundla'])
            self.umphakatsi.insert(0,r['umphakatsi'])
            self.chief.insert(0,r['chief'])
            self.indvuna.insert(0,r['indvuna'])
            self.next_of_kin.insert(0,r['next_of_kin_name'])
            self.next_of_kin_phone.insert(0,r['next_of_kin_phone'])
            self.offences.insert(0,r['offences'])
            self.court.insert(0,r['court_name'])
            self.court_date.insert(0,datetime.datetime.strptime(r['court_date'],"%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y'))
            self.sentence.insert(0,r['sentence'])
            self.criminal_case_num.insert(0,r['criminal_case_number'])
            self.admitting_center.insert(0,r['admitting_center'])
            self.rehabilitation_officer.insert(0,f"{r['rehabilitation_officer_number']} {r['rehabilitation_officer_name']} {r['rehabilitation_officer_surname']}")
            self.post_care_variable.set(r['after_case_sentence_assistance'])
            self.e_d_r.insert(0, r['e_d_r'])
            self.l_d_r.insert(0,r['l_d_r'])
            self.transfer_center.insert(0,r['transfer_centre'])
            self.transfer_center_date.insert(0,datetime.datetime.strptime(r['transfer_centre_date'],"%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y'))
            self.date_of_reception.insert(0,datetime.datetime.strptime(r['date_of_reception'],"%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y'))
            self.actual_release_date.insert(0,datetime.datetime.strptime(r['actual_release_date'],"%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y'))
            self.date_case_closed.insert(0,datetime.datetime.strptime(r['date_case_closed'],"%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y'))
        
            print("done populating")
        else:
            mb.showinfo('Notice',r['message'])
            print('Error getting data from server')