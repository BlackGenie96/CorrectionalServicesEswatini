import tkinter as tk
from offender import *
from constants import *
from retrieve_offender import *

#for testing 
from family import *
from home_education import *
from employment import *
from health_developmental import *
from quaterly_reviews import *
from record_of_contact import *
from discharge_interview import *
from completion_report import *


class FirstMenu(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)

        tk.Label(self,text=f"Officer No: {master.officer_info['officer_id']}",font=label_font,background='white',width=60).grid(row=1,column=3,ipady=15,ipadx=15)
        tk.Label(self,text=f"Name: {master.officer_info['name']}", background='white',font=label_font,width=60).grid(row=2,column=3,ipady=15,ipadx=15)
        tk.Label(self,text=f"Surname: {master.officer_info['surname']}",background='white',font=label_font,width=60).grid(row=3,column=3,ipady=15,ipadx=15)

        tk.Button(self,text='CREATE\nOFFENDER\nFILE',font=button_font,width=20,command=lambda: self.goToCreateOffender(master)).grid(row=5,column=3,ipady=15,ipadx=15)
        tk.Button(self,text='RETRIEVE\nOFFENDER\nFILE',font=button_font,width=20,command=lambda: self.retrieveOffender(master)).grid(row=6,column=3,ipady=15,ipadx=15)
        tk.Button(self,text='LOG OUT',command=master.quit,font=button_font).grid(row=10,column=3,ipady=5,ipadx=5,pady=30)

    def goToCreateOffender(self,master):
        master.switch_frame(OffenderFrame)
        #master.switch_frame(FamilyFrame)
        #master.switch_frame(HomeEducationFrame)
        #master.switch_frame(EmploymentFrame)
        #master.switch_frame(HealthDevelopmentalFrame)
        #master.switch_frame(QuaterlyReviewsFrame)
        #master.switch_frame(RecordOfContactFrame)
        #master.switch_frame(DischargeInterviewFrame)
        #master.switch_frame(CompletionReportFrame)

    def retrieveOffender(self, master):
        master.switch_frame(RetrieveOffenderFrame)