import tkinter as tk
import tkinter.messagebox as mb

from constants import *
from scrollable_frame import *
from API.main_menu_services import *

class MainMenuFrame(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)

        #definiting local variables
        self.frame = ScrollableFrame(master)

        self.buildWidgets(master)
        self.frame.pack()

    
    def buildWidgets(self, master):
        #offender general info display
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        name = tk.Label(row, text=master.current_offender['name'],font=label_font)
        surname = tk.Label(row, text=master.current_offender['surname'],font = label_font)
        row.pack(side='top',pady=10)
        name.pack(side='left')
        surname.pack(side='right')

        #offender id number
        row = tk.Frame(big_row)
        lab = tk.Label(row, text='ID Number : ',font=label_font)
        id_num = tk.Label(row, text=master.current_offender['id_number'],font=label_font)
        row.pack(side='top',pady=10)
        lab.pack(side='left')
        id_num.pack(side='right')

        #gaol number
        row = tk.Frame(big_row)
        lab = tk.Label(row, text='GAOL Number : ', font=label_font)
        gaol_num = tk.Label(row, text=master.current_offender['gaol_number'],font=label_font)
        row.pack(side='top',pady=10)
        lab.pack(side='left')
        gaol_num.pack(side='right')

        big_row.pack(side='top',)

        #topic / title
        row = tk.Frame(self.frame.scrollable_frame)
        lab = tk.Label(row, text='OFFENDER FILE OPTIONS',font=label_font)
        row.pack(side='top',pady=20)
        lab.pack(side='top')

        #case record and religion & family buttons
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        case_record = tk.Button(row, text='CASE\nRECORD', width=20,font=label_font,command=lambda:self.editCaseRecord(master))
        family = tk.Button(row, text='RELIGION &\nFAMILY', width=20,font=label_font,command=lambda:self.editReligionAndFamily(master))
        row.pack(side='top')
        case_record.pack(side='left',ipady=20)
        family.pack(side='right', ipady=20)
        big_row.pack(side='top', pady=15, padx=55)

        #home/education and employment buttons
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        home = tk.Button(row, text='HOME &\nEDUCATION',width=20, font=label_font,command=lambda:self.editHomeAndEducation(master))
        employment = tk.Button(row, text='EMPLOYMENT\n',width=20, font=label_font,command=lambda:self.editEmployment(master))
        row.pack(side='top')
        home.pack(side='left', ipady=20)
        employment.pack(side='right', ipady=20)
        big_row.pack(side='top',pady=15)

        #health/development and case assessment buttons
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        health = tk.Button(row, text='HEALTH &\nDEVELOPMENTAL\nHISTORY',width=20,font=label_font,command=lambda:self.editHealthAndDevelopmental(master))
        reviews = tk.Button(row, text='CASE ASSESSMENT\nor QUATERLY\nREVIEWS',width=20, font=label_font,command=lambda:self.editCaseAssessment(master))
        row.pack(side='top')
        health.pack(side='left',ipady=20)
        reviews.pack(side='right', ipady=20)
        big_row.pack(side='top',pady=15)

        #record of contact and discharge interview buttons
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        contact = tk.Button(row, text='RECORD OF\nCONTACT', width=20, font=label_font,command=lambda:self.editRecordOfContact(master))
        discharge = tk.Button(row, text='DISCHARGE\nINTERVIEW',width=20, font=label_font,command=lambda:self.editDischargeInterview(master))
        row.pack(side='top')
        contact.pack(side='left',ipady=20)
        discharge.pack(side='right',ipady=20)
        big_row.pack(side='top', pady=15)

        #completion report and exit button
        big_row = tk.Frame(self.frame.scrollable_frame)
        row = tk.Frame(big_row)
        completion = tk.Button(row, text='COMPLETION\nREPORT',width=20, font=label_font,command=lambda:self.editCompletionReport(master))
        exit_but = tk.Button(row, text='EXIT\nOFFENDER MENU', width=20, font=label_font,command=lambda:self.goToFirstMenu(master))
        row.pack(side='top')
        completion.pack(side='left', ipady=20)
        exit_but.pack(side='right', ipady=20)
        big_row.pack(side='top',pady=15)

    #function to route to case record editing
    def editCaseRecord(self, master):
        from offender import OffenderFrame
        self.frame.destroyMe()
        master.switch_frame(OffenderFrame(master,flag='edit'))

    #function to route to religion and family
    def editReligionAndFamily(self, master):
        from family import FamilyFrame
        self.frame.destroyMe()
        master.switch_frame(FamilyFrame(master,flag='edit'))

    #function to route to home and education
    def editHomeAndEducation(self, master):
        from home_education import HomeEducationFrame
        self.frame.destroyMe()
        master.switch_frame(HomeEducationFrame(master, flag='edit'))

    #function to route to employment
    def editEmployment(self, master):
        from employment import EmploymentFrame
        self.frame.destroyMe()
        master.switch_frame(EmploymentFrame(master,flag='edit'))
    
    #function to route to health and developmental history
    def editHealthAndDevelopmental(self, master):
        from health_developmental import HealthDevelopmentalFrame
        self.frame.destroyMe()
        master.switch_frame(HealthDevelopmentalFrame(master, flag='edit'))

    #function to route to case assessment
    def editCaseAssessment(self, master):
        from quaterly_reviews import QuaterlyReviewsFrame
        self.frame.destroyMe()
        master.switch_frame(QuaterlyReviewsFrame(master, flag='edit'))

    #function to route to record of contact
    def editRecordOfContact(self, master):
        from record_of_contact import RecordOfContactFrame
        self.frame.destroyMe()
        master.switch_frame(RecordOfContactFrame(master, flag='edit'))
    
    #function to route to discharge interview
    def editDischargeInterview(self, master):
        from discharge_interview import DischargeInterviewFrame
        self.frame.destroyMe()
        master.switch_frame(DischargeInterviewFrame(master, flag='edit'))

    #function to route to completion report
    def editCompletionReport(self, master):
        from completion_report import CompletionReportFrame
        self.frame.destroyMe()
        master.switch_frame(CompletionReportFrame(master, flag='edit'))

    #function to route to first frame
    def goToFirstMenu(self, master):
        from firstMenu import FirstMenu
        self.frame.destroyMe()
        master.switch_frame(FirstMenu(master))