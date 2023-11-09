from customtkinter import *
import customtkinter
from tkinter import * 
from PIL import Image
import tkinter
import ttkbootstrap as tb
from datetime import date
from ttkbootstrap.dialogs import Querybox
customtkinter.set_appearance_mode("light")


class login_gui:
    def __init__(self,app):
        self.app=app
        self.app.title('AIRLINE RESERVATION TICKET')
        self.app.state('zoomed')

        self.background =customtkinter.CTkImage(Image.open("background.png"),size=(app.winfo_screenwidth(), app.winfo_screenheight()))
        self.l1 = customtkinter.CTkLabel(master=app,image=self.background,text="")
        self.l1.pack(fill='both', expand=True)


        self.frame=customtkinter.CTkFrame(master=self.l1, width=500, height=400,corner_radius=5,border_width=3,border_color="#77B5FE",fg_color="white")
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.msg=customtkinter.CTkLabel(master=self.frame, text="Airline Reservation Ticket",compound="top",font=("Apple Chancery, cursive",30 ),text_color="blue")
        self.msg.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

        self.email = customtkinter.CTkEntry(self.frame, placeholder_text="Email",width=250, height=35,font=("cursive",15 ),border_color="#859BF5",border_width=3)
        self.email.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.passworld = customtkinter.CTkEntry(self.frame, placeholder_text="Passworld",width=250, height=35,font=("cursive",17 ),border_color="#859BF5",border_width=3)
        self.passworld.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

        self.login=customtkinter.CTkButton(self.frame, text="Login",width=120,fg_color="green",command=lambda:self.logiin())
        self.login.place(relx=0.365, rely=0.58, anchor=tkinter.CENTER)

        self.creat_an_account=customtkinter.CTkButton(self.frame, text="Creat an account",width=120,fg_color="red",command=lambda:self.creat_an_account())
        self.creat_an_account.place(relx=0.64, rely=0.58, anchor=tkinter.CENTER)

        self.login_as_guest=customtkinter.CTkButton(self.frame, text="Login as a guest",command=lambda:self.logiin_as_guest())
        self.login_as_guest.place(relx=0.5, rely=0.69, anchor=tkinter.CENTER)

        
    def logiin(self):
        
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        bookingapp(self.app)
        
    def logiin_as_guest(self):
        
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        bookingapp(self.app)
    
    def creat_an_account(self):
        
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        #create a class to creat an account 


class bookingapp:
    def __init__(self,app):
        self.app=app
        self.frame=customtkinter.CTkFrame(master=self.app, width=1222, height=200,border_color="#77B5FE",fg_color="white")
        self.frame.place(relx=0.5, rely=0.19, anchor=tkinter.CENTER)
        airport=["Aéroport Charles de Gaulle | CDG", 
                "Aéroport Adolfo-Suárez de Madrid-Barajas | MAD",
                "Aéroport de Francfort | FRA",
                "Aéroport d'Amsterdam-Schiphol	| AMS",
                "Aéroport international du Caire | CAI",
                "Aéroport d'Istanbul | IST" ,
                "Aéroport international du roi Fahd | JIB"
                 ]
        
        self.arrival_airport = customtkinter.StringVar()
        self.arrival_airport.set("Select Arrival Airport")
        self.arrival_airport = customtkinter.CTkComboBox(self.frame,values=airport,border_width=2,variable=self.arrival_airport,width=200,border_color="#77B5FE",button_color="#77B5FE")
        self.arrival_airport.place(relx=0.3, rely=0.4, anchor=tkinter.CENTER)
        
        self.departure_airport = customtkinter.StringVar()
        self.departure_airport.set("Select Departure Airport") 
        self.departure_airport = customtkinter.CTkComboBox(self.frame,values=airport,border_width=2,variable=self.departure_airport,width=200,border_color="#77B5FE",button_color="#77B5FE")
        self.departure_airport.place(relx=0.1, rely=0.4, anchor=tkinter.CENTER)
        
        self.Class = customtkinter.StringVar()
        self.Class.set("Select Class")
        self.Class = customtkinter.CTkComboBox(self.frame,values=['Economy Class','First Class'],border_width=2,variable=self.Class,width=200,border_color="#77B5FE",button_color="#77B5FE")
        self.Class.place(relx=0.3, rely=0.7, anchor=tkinter.CENTER)
        
        """"
        self.my_departue_date = tb.DateEntry(self.frame, bootstyle="danger",firstweekday=0, startdate=date(2023, 2, 14))
        self.my_departue_date.pack(relx=0.3, rely=0.7, anchor=tkinter.CENTER)
        
        self.my_arrival_date = tb.DateEntry(self.frame, bootstyle="danger",firstweekday=0, startdate=date(2023, 2, 14))
        self.my_arrival_date.pack(relx=0.3, rely=0.6, anchor=tkinter.CENTER)
        """
        
        self.frame_booking=customtkinter.CTkScrollableFrame(master=self.app, width=1200, height=500,border_color="#77B5FE",fg_color="white")
        self.frame_booking.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)
        
        
        



        
         
        
def main():
    app = tkinter.Tk()
    app1 = login_gui(app)
    app.mainloop()

if __name__ == "__main__":
    main()