from customtkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter
from tkinter import * 
from PIL import Image
import tkinter
from typing import Union, Callable
import pymysql
from CTkMessagebox import CTkMessagebox
from tkinter import messagebox
import matplotlib.pyplot as plt
from collections import Counter
import datetime
from tkcalendar import DateEntry
customtkinter.set_appearance_mode("light")

def mysqlconnect(test):
    conn = pymysql.connect(host='localhost', user='root', password="", db='project_oop')  # Establishing connection to the database.
    cur = conn.cursor()  # Creating a cursor object to execute queries.
    cur.execute(test)  # Executing the SQL query passed as a parameter.
    conn.commit()  # Committing the transaction to the database.
    output = cur.fetchall()  # Fetching all the results from the executed query.
    cur.close()  # Closing the cursor.
    conn.close()  # Closing the database connection.
    return(output)  # Returning the fetched results.
class FloatSpinbox(customtkinter.CTkFrame):
    def __init__(self, *args,
                width: int = 200,
                height: int = 32,
                step_size: Union[int, float] = 1,
                command: Callable = None,
                **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands
        self.x=True
        self.subtract_button = customtkinter.CTkButton(self, text="-", width=height-6, height=height-6, command=self.subtract_button_callback,fg_color="#77B5FE")
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = customtkinter.CTkEntry(self, width=width-2, height=height-6, border_width=0,placeholder_text="number of passengers")
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = customtkinter.CTkButton(self, text="+", width=height-6, height=height-6,command=self.add_button_callback,fg_color="#77B5FE")
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
    def add_button_callback(self):
        if self.x==True:
            self.entry.insert(0, "0")
        self.x=False
        if self.command is not None:
            self.command()
            
        try:
            value = int(self.entry.get()) + int(self.step_size)
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            if float(self.entry.get())>0:
                value = int(self.entry.get()) - int(self.step_size)
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
        except ValueError:
            return

    def get(self) -> Union[float, None]:
        try:
            return float(self.entry.get())
        except ValueError:
            return None

class login_gui:
    def __init__(self, l1):# Constructor for login_gui class.
        self.l1 = l1  # Storing the parent widget or window.
        self.frame = customtkinter.CTkFrame(master=self.l1, width=500, height=400, corner_radius=5, border_width=3, border_color="#77B5FE", fg_color="white")# Creating a frame for the login GUI.
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)  # Positioning the frame.
        self.msg = customtkinter.CTkLabel(master=self.frame, text="SkyJourney Booker", compound="top", font=("Apple Chancery, cursive", 30), text_color="blue") # Label for displaying the title.
        self.msg.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)  # Positioning the label.        
        self.email = customtkinter.CTkEntry(self.frame, placeholder_text="Email", width=250, height=35, font=("cursive", 15), border_color="#859BF5", border_width=3)# Entry widget for email input.
        self.email.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)  # Positioning the email entry.
        self.password = customtkinter.CTkEntry(self.frame, placeholder_text="Password", width=250, height=35, font=("cursive", 17), border_color="#859BF5", border_width=3)# Entry widget for password input.
        self.password.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)  # Positioning the password entry.
        self.login = customtkinter.CTkButton(self.frame, text="Login", width=120, fg_color="green", command=lambda: self.Login(self.l1))# Button for logging in.
        self.login.place(relx=0.365, rely=0.58, anchor=tkinter.CENTER)  # Positioning the login button.
        self.creat_an_account = customtkinter.CTkButton(self.frame, text="Create an account", width=120, fg_color="red", command=lambda: self.creat_account())# Button for creating a new account.
        self.creat_an_account.place(relx=0.64, rely=0.58, anchor=tkinter.CENTER)  # Positioning the create account button.
        self.login_as_guest = customtkinter.CTkButton(self.frame, text="Login as a guest", command=lambda: self.logiin_as_guest()) # Button for logging in as a guest.
        self.login_as_guest.place(relx=0.5, rely=0.69, anchor=tkinter.CENTER)  # Positioning the guest login button.
    def Login(self, app):# Method to handle the login process.
        self.app = app
        email = str(self.email.get())  # Getting the email from the entry widget.
        password = str(self.password.get())  # Getting the password from the entry widget.
        # SQL query to check the user's credentials.
        request_sql_connection = "select * from member where email='" + email + "' and password='" + password + "'"
        user = mysqlconnect(request_sql_connection)  # Executing the query.
        if len(user) == 0: # Handling the login process based on the query result.
            messagebox.showerror('Error', 'Error: wrong email or password!')  # Showing an error message.
        else:# Clearing the frame if login is successful.
            for widget in self.frame.winfo_children():
                widget.destroy()
            self.frame.destroy()
            request_sql_permission = "SELECT permission, member_id FROM member WHERE email='" + email + "'"# Query to get the user's permission level.
            permission = mysqlconnect(request_sql_permission)            
            if (permission[0][0] == 1):# Redirecting to the appropriate interface based on the user's permission level.
                AdminGUI(self.l1)  # Admin interface.
            else:
                bookingapp(self.l1, permission[0][1])  # Booking interface for regular users.

    def logiin_as_guest(self):# Method for guest login.
        for widget in self.frame.winfo_children(): # Clearing the frame for the guest login.
            widget.destroy()
        self.frame.destroy()
        bookingapp(self.l1, '0')  # Redirecting to the booking interface as a guest.
    def creat_account(self):# Method to create a new account.
        # Clearing the frame for account creation.
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        CreateAccountGui(self.l1)  # Redirecting to the account creation interface.
             
class bookingapp:
    def __init__(self,app,member_id):
        self.app=app

        self.frame=customtkinter.CTkFrame(master=self.app, width=1222, height=200,corner_radius=5,border_width=3,border_color="#77B5FE",fg_color="white")
        self.frame.place(relx=0.5, rely=0.19, anchor=tkinter.CENTER)
        request_sql_dairport="SELECT DISTINCT(departure_airport) FROM `flight`;"
        dairport=mysqlconnect(request_sql_dairport)
        airport=[item[0] for item in dairport]

        self.departure_airport = customtkinter.StringVar()
        self.departure_airport.set("Select Departure Airport") 
        self.departure_airport = customtkinter.CTkComboBox(self.frame,values=airport,border_width=2,variable=self.departure_airport,width=200,border_color="#77B5FE",button_color="#77B5FE")
        self.departure_airport.place(relx=0.1, rely=0.4, anchor=tkinter.CENTER)

        request_sql_dairport="SELECT DISTINCT(arrival_airport) FROM `flight`"
        a_airport=mysqlconnect(request_sql_dairport)
        airport_a=[item[0] for item in a_airport]

        self.arrival_airport = customtkinter.StringVar()
        self.arrival_airport.set("Select Arrival Airport")
        self.arrival_airport = customtkinter.CTkComboBox(self.frame,values=airport_a,border_width=2,variable=self.arrival_airport,width=200,border_color="#77B5FE",button_color="#77B5FE")
        self.arrival_airport.place(relx=0.3, rely=0.4, anchor=tkinter.CENTER)
                
        self.Class = customtkinter.StringVar()
        self.Class.set("Select Class")
        self.Class = customtkinter.CTkComboBox(self.frame,values=['Economy Class','First Class'],border_width=2,variable=self.Class,width=200,border_color="#77B5FE",button_color="#77B5FE")
        self.Class.place(relx=0.3, rely=0.7, anchor=tkinter.CENTER)
        
        
        self.my_departure_date = DateEntry(self.frame, width=12, background='darkblue',
                                           foreground='white', borderwidth=2, 
                                           font=("cursive", 15), year=datetime.datetime.now().year,
                                           month=datetime.datetime.now().month, day=datetime.datetime.now().day,
                                           date_pattern='y-mm-dd')
        self.my_departure_date.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

        self.my_arrival_date = DateEntry(self.frame, width=12, background='darkblue',
                                           foreground='white', borderwidth=2, 
                                           font=("cursive", 15), year=datetime.datetime.now().year,
                                           month=datetime.datetime.now().month, day=datetime.datetime.now().day,
                                           date_pattern='y-mm-dd')
        self.my_arrival_date.place(relx=0.7, rely=0.4, anchor=tkinter.CENTER)
                

        self.spinbox_1 = FloatSpinbox(self.frame, width=140, step_size=1)
        self.spinbox_1.place(relx=0.1, rely=0.7, anchor=tkinter.CENTER)
        
        self.search=customtkinter.CTkButton(self.frame, text="SEARCH A FLIGHT",width=200,height=90,fg_color="red",font=("cursive",23 ),command=lambda:self.research(member_id),corner_radius=10)
        self.search.place(relx=0.89, rely=0.56, anchor=tkinter.CENTER)

        self.historic=customtkinter.CTkButton(self.frame, text="HISTORIC",width=100,height=20,text_color="black",fg_color="white",font=("cursive",15),command=lambda:self.historique(member_id),corner_radius=0)
        self.historic.place(relx=0.05, rely=0.1, anchor=tkinter.CENTER)
        
        self.log_out=customtkinter.CTkButton(self.frame, text="LOG OUT",width=100,height=20,text_color="black",fg_color="white",font=("cursive",15),command=lambda:self.logout(),corner_radius=0)
        self.log_out.place(relx=0.15, rely=0.1, anchor=tkinter.CENTER)
        if(member_id!='0'):
            self.info=customtkinter.CTkButton(self.frame, text="USER INFO",width=100,height=20,text_color="black",fg_color="white",font=("cursive",15),command=lambda:self.info_display(member_id),corner_radius=0)
            self.info.place(relx=0.25, rely=0.1, anchor=tkinter.CENTER)
        
    
        self.frameb=customtkinter.CTkFrame(master=self.app, width=1222, height=500,border_color="#77B5FE",fg_color="white")
        self.frameb.place(relx=0.5, rely=0.66, anchor=tkinter.CENTER)
        
        self.framebooking=customtkinter.CTkScrollableFrame(master=self.frameb, width=1200, height=500,border_color="#77B5FE",fg_color="white")
        self.framebooking.place(relx=0.5, rely=0.50, anchor=tkinter.CENTER)
        self.no_result = customtkinter.CTkLabel(self.framebooking, text="No Result For Flights", text_color="black",font=("cursive",25 ), fg_color="transparent")
        self.no_result.grid(row=0, column=2,padx=400)
        self.bar = customtkinter.CTkFrame(self.framebooking,width=240,height=4,corner_radius=10,border_width=5, border_color="grey",fg_color="grey",)
        self.bar.grid(row=1, column=2,padx=400)
        
    def logout(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        for widget in self.frameb.winfo_children():
            widget.destroy()
        self.frame.destroy()
        self.frameb.destroy()
        login_gui(self.app)

    def info_display(self,member_id):
        for widget in self.frame.winfo_children():
            widget.destroy()
        for widget in self.frameb.winfo_children():
            widget.destroy()
        self.frame.destroy()
        self.frameb.destroy()
        user(self.app,member_id)
                    
    def research(self,member_id):
        if (str(self.departure_airport.get())=='' or str(self.arrival_airport.get())=='' or str(self.Class.get())=='Select Class' or str(self.my_departure_date.get())=='' or str(self.my_arrival_date.get())=='' or str(self.spinbox_1.get())=='None'):
            messagebox.showerror('', 'Error: There is an empty entry area')
        else:
            for widget in self.framebooking.winfo_children():
                widget.destroy()
            request_sql_departure="select * from flight where departure_airport='"+str(self.departure_airport.get())+"' and arrival_airport='"+str(self.arrival_airport.get())+"' and departing='"+str(self.my_departure_date.get())+"'"
            request_sql_arrival="select * from flight where departure_airport='"+str(self.arrival_airport.get())+"' and arrival_airport='"+str(self.departure_airport.get())+"' and departing='"+str(self.my_arrival_date.get())+"'"
            flight_departure=mysqlconnect(request_sql_departure)
            flight_arrival=mysqlconnect(request_sql_arrival)
            i=0
            if len(flight_departure)==0 and len(flight_arrival)==0 :
                self.no_result = customtkinter.CTkLabel(self.framebooking, text="No Result For Flights", text_color="black",font=("cursive",25 ), fg_color="transparent")
                self.no_result.grid(row=0, column=2,padx=400)
                self.bar = customtkinter.CTkFrame(self.framebooking,width=260,height=4,corner_radius=10,border_width=5, border_color="grey",fg_color="grey",)
                self.bar.grid(row=1, column=2,padx=400)
            elif len(flight_departure)==len(flight_arrival):
                for i in range(len(flight_departure)):
                    if (flight_departure[i][7]-self.spinbox_1.get()<=0 or flight_arrival[i][7]-self.spinbox_1.get()<=0):
                        pass                        
                    else:
                        self.frame_flight = customtkinter.CTkFrame(self.framebooking,width=1180,height=80,corner_radius=0,border_width=4, border_color="#968080",fg_color="white")
                        self.frame_flight.grid(row=i,padx=10, pady=10)
                        self.book=customtkinter.CTkButton(self.frame_flight, text="Book for "+str(flight_departure[i][8]+flight_arrival[i][8])+" £/pp",width=200,height=60,corner_radius=0,fg_color="red",font=("cursive",20 ),border_width=1,command=lambda i=i:self.booking(flight_departure[i][8]+flight_arrival[i][8],member_id,self.spinbox_1.get(),flight_departure[i][0],flight_arrival[i][0]))
                        self.book.place(relx=0.903, rely=0.5, anchor=tkinter.CENTER)                    
                        self.frame_info_flight = customtkinter.CTkFrame(self.frame_flight,width=950,height=60,corner_radius=0,border_width=2, border_color="#968080",fg_color="white")
                        self.frame_info_flight.place(relx=0.41, rely=0.5, anchor=tkinter.CENTER)
                        self.info_flight = customtkinter.CTkLabel(self.frame_info_flight, text=flight_departure[i][2]+" to "+flight_departure[i][3]+" take off time the "+str(flight_departure[i][4])+" at "+str(flight_departure[i][6])[:-3]+" flight time "+str(flight_departure[i][5])+"\n"+flight_arrival[i][2]+" to "+flight_arrival[i][3]+" take off time the "+str(flight_arrival[i][4])+" at "+str(flight_arrival[i][6])[:-3]+" flight time "+str(flight_arrival[i][5]), text_color="black",font=("cursive",25 ),fg_color="transparent")
                        self.info_flight.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
            elif len(flight_departure)==0 or len(flight_arrival)==0:
                if len(flight_arrival)==0:
                    for i in range(len(flight_departure)):
                        if (flight_departure[i][7]-self.spinbox_1.get()<=0):
                            pass                        
                        else:
                            self.frame_flight = customtkinter.CTkFrame(self.framebooking,width=1180,height=80,corner_radius=0,border_width=4, border_color="#968080",fg_color="white")
                            self.frame_flight.grid(row=i,padx=10, pady=10)
                            self.book=customtkinter.CTkButton(self.frame_flight, text="Book for "+str(flight_departure[i][8])+" £/pp",width=200,height=60,corner_radius=0,fg_color="red",font=("cursive",20 ),border_width=1,command=lambda i=i:self.booking(flight_departure[i][8],member_id,self.spinbox_1.get(),flight_departure[i][0],'0'))
                            self.book.place(relx=0.903, rely=0.5, anchor=tkinter.CENTER)      
                            self.frame_info_flight = customtkinter.CTkFrame(self.frame_flight,width=950,height=60,corner_radius=0,border_width=2, border_color="#968080",fg_color="white")
                            self.frame_info_flight.place(relx=0.41, rely=0.5, anchor=tkinter.CENTER)
                            self.info_flight = customtkinter.CTkLabel(self.frame_info_flight, text=flight_departure[i][2]+" to "+flight_departure[i][3]+" take off time the "+str(flight_departure[i][4])+" at "+str(flight_departure[i][6])[:-3]+" flight time "+str(flight_departure[i][5]), text_color="black",font=("cursive",25 ),fg_color="transparent")
                            self.info_flight.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
                else:
                    for i in range(len(flight_arrival)):
                        if (flight_arrival[i][7]-self.spinbox_1.get()<=0):
                            pass                        
                        else:
                            self.frame_flight = customtkinter.CTkFrame(self.framebooking,width=1180,height=80,corner_radius=0,border_width=4, border_color="#968080",fg_color="white")
                            self.frame_flight.grid(row=i,padx=10, pady=10)
                            self.book=customtkinter.CTkButton(self.frame_flight, text="Book for "+str(flight_arrival[i][8])+" £/pp",width=200,height=60,corner_radius=0,fg_color="red",font=("cursive",20 ),border_width=1,command=lambda i=i:self.booking(flight_departure[i][8],member_id,self.spinbox_1.get(),flight_departure[i][0],'0'))
                            self.book.place(relx=0.903, rely=0.5, anchor=tkinter.CENTER) 
                            self.frame_info_flight = customtkinter.CTkFrame(self.frame_flight,width=950,height=60,corner_radius=0,border_width=2, border_color="#968080",fg_color="white")
                            self.frame_info_flight.place(relx=0.41, rely=0.5, anchor=tkinter.CENTER)
                            self.info_flight = customtkinter.CTkLabel(self.frame_info_flight, text=flight_arrival[i][2]+" to "+flight_arrival[i][3]+" take off time the "+str(flight_arrival[i][4])+" at "+str(flight_arrival[i][6])[:-3]+" flight time "+str(flight_arrival[i][5]), text_color="black",font=("cursive",25 ),fg_color="transparent")
                            self.info_flight.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
            
            else:
                if len(flight_departure)>len(flight_arrival):
                    
                    for i in range(len(flight_arrival)):
                        if (flight_arrival[i][7]-self.spinbox_1.get()<=0):
                            pass                        
                        else:
                            self.frame_flight = customtkinter.CTkFrame(self.framebooking,width=1180,height=80,corner_radius=0,border_width=4, border_color="#968080",fg_color="white")
                            self.frame_flight.grid(row=i,padx=10, pady=10)
                            self.book=customtkinter.CTkButton(self.frame_flight, text="Book for "+str(flight_arrival[i][8]+flight_departure[i][8])+" £/pp",width=200,height=60,corner_radius=0,fg_color="red",font=("cursive",20 ),border_width=1,command=lambda i=i: self.booking(flight_departure[i][8] + flight_arrival[i][8],member_id,self.spinbox_1.get(),flight_departure[i][0],flight_arrival[i][0]))
                            self.book.place(relx=0.903, rely=0.5, anchor=tkinter.CENTER) 
                            self.frame_info_flight = customtkinter.CTkFrame(self.frame_flight,width=950,height=60,corner_radius=0,border_width=2, border_color="#968080",fg_color="white")
                            self.frame_info_flight.place(relx=0.41, rely=0.5, anchor=tkinter.CENTER)
                            self.info_flight = customtkinter.CTkLabel(self.frame_info_flight, text=flight_departure[i][2]+" to "+flight_departure[i][3]+" take off time the "+str(flight_departure[i][4])+" at "+str(flight_departure[i][6])[:-3]+" flight time "+str(flight_departure[i][5])+"\n"+flight_arrival[i][2]+" to "+flight_arrival[i][3]+" take off time the "+str(flight_arrival[i][4])+" at "+str(flight_arrival[i][6])[:-3]+" flight time "+str(flight_arrival[i][5]), text_color="black",font=("cursive",25 ),fg_color="transparent")
                            self.info_flight.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
                    for i in range(len(flight_arrival),len(flight_departure)):
                        if (flight_departure[i][7]-self.spinbox_1.get()<=0):
                            pass                        
                        else:
                            self.frame_flight = customtkinter.CTkFrame(self.framebooking,width=1180,height=80,corner_radius=0,border_width=4, border_color="#968080",fg_color="white")
                            self.frame_flight.grid(row=i,padx=10, pady=10)
                            self.book=customtkinter.CTkButton(self.frame_flight, text="Book for "+str(flight_departure[i][8])+" £/pp",width=200,height=60,corner_radius=0,fg_color="red",font=("cursive",20 ),border_width=1,command=lambda i=i:self.booking(flight_departure[i][8],member_id,self.spinbox_1.get(),flight_departure[i][0],'0'))
                            self.book.place(relx=0.906, rely=0.5, anchor=tkinter.CENTER)
                            self.frame_info_flight = customtkinter.CTkFrame(self.frame_flight,width=950,height=60,corner_radius=0,border_width=2, border_color="#968080",fg_color="white")
                            self.frame_info_flight.place(relx=0.41, rely=0.5, anchor=tkinter.CENTER)
                            self.info_flight = customtkinter.CTkLabel(self.frame_info_flight, text=flight_departure[i][2]+" to "+flight_departure[i][3]+" take off time the "+str(flight_departure[i][4])+" at "+str(flight_departure[i][6])[:-3]+" flight time "+str(flight_departure[i][5]), text_color="black",font=("cursive",25 ),fg_color="transparent")
                            self.info_flight.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)  
                else:
                    for i in range(len(flight_departure)):
                        if (flight_departure[i][7]-self.spinbox_1.get()<=0):
                            pass                        
                        else:
                            self.frame_flight = customtkinter.CTkFrame(self.framebooking,width=1180,height=80,corner_radius=0,border_width=4, border_color="#968080",fg_color="white")
                            self.frame_flight.grid(row=i,padx=10, pady=10)
                            self.book=customtkinter.CTkButton(self.frame_flight, text="Book for "+str(flight_departure[8])+" £/pp",width=200,height=60,corner_radius=0,fg_color="red",font=("cursive",20 ),border_width=1,command=lambda:self.booking(flight_departure[i][8],member_id,self.spinbox_1.get(),flight_departure[i][0],'0'))
                            self.book.place(relx=0.906, rely=0.5, anchor=tkinter.CENTER)
                            self.frame_info_flight = customtkinter.CTkFrame(self.frame_flight,width=950,height=60,corner_radius=0,border_width=2, border_color="#968080",fg_color="white")
                            self.frame_info_flight.place(relx=0.41, rely=0.5, anchor=tkinter.CENTER)
                            self.info_flight = customtkinter.CTkLabel(self.frame_info_flight, text=flight_departure[i][2]+" to "+flight_departure[i][3]+" take off time the "+str(flight_departure[i][4])+" at "+str(flight_departure[i][6])[:-3]+" flight time "+str(flight_departure[i][5])+"\n"+flight_arrival[i][2]+" to "+flight_arrival[i][3]+" take off time the "+str(flight_arrival[i][4])+" at "+str(flight_arrival[i][6])[:-3]+" flight time "+str(flight_arrival[i][5]), text_color="black",font=("cursive",25 ),fg_color="transparent")
                            self.info_flight.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
                    for i in range(len(flight_departure),len(flight_arrival)):
                        if (flight_departure[i][7]-self.spinbox_1.get()<=0):
                            pass                        
                        else:
                            self.frame_flight = customtkinter.CTkFrame(self.framebooking,width=1180,height=80,corner_radius=0,border_width=4, border_color="#968080",fg_color="white")
                            self.frame_flight.grid(row=i,padx=10, pady=10)
                            self.book=customtkinter.CTkButton(self.frame_flight, text="Book for "+str(flight_departure[8])+" £/pp",width=200,height=25,corner_radius=0,fg_color="red",font=("cursive",20 ),border_width=1,command=lambda:self.booking(flight_departure[i][8],member_id,self.spinbox_1.get(),flight_departure[i][0],'0'))
                            self.book.place(relx=0.906, rely=0.5, anchor=tkinter.CENTER)
                            self.frame_info_flight = customtkinter.CTkFrame(self.frame_flight,width=950,height=60,corner_radius=0,border_width=2, border_color="#968080",fg_color="white")
                            self.frame_info_flight.place(relx=0.41, rely=0.5, anchor=tkinter.CENTER)
                            self.info_flight = customtkinter.CTkLabel(self.frame_info_flight, text=flight_arrival[i][2]+" to "+flight_arrival[i][3]+" take off time the "+str(flight_arrival[i][4])+" at "+str(flight_arrival[i][6])[:-3]+" flight time "+flight_arrival[i][5], text_color="black",font=("cursive",25 ),fg_color="transparent")
                            self.info_flight.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)        
        return
    
    def booking(self, price, member_id, number, flight_id1, flight_id2):
        # Function for handling booking action
        # Clears all widgets from the current frames
        for widget in self.frame.winfo_children():
            widget.destroy()
        for widget in self.frameb.winfo_children():
            widget.destroy()

        # Destroys the current frames to free up resources
        self.frame.destroy()
        self.frameb.destroy()

        # Calls the bookGUI class to initiate the booking process
        # Passes necessary parameters like price, member_id, etc.
        bookGUI(self.app, price, member_id, number, flight_id1, flight_id2)

    def historique(self, member_id):
        # Function to display the booking history for a member
        # Checks if a valid member_id is provided
        if member_id == '0':
            # Shows an error message if member_id is not valid
            messagebox.showerror('', 'Error: You are not logged in')
            return
        else:
            # Clears all widgets from the current frames
            for widget in self.frame.winfo_children():
                widget.destroy()
            for widget in self.frameb.winfo_children():
                widget.destroy()

            # Destroys the current frames
            self.frame.destroy()
            self.frameb.destroy()

            # Calls the HistoricGUI class to show the booking history for the member
            HistoricGUI(self.app, member_id)

class CreateAccountGui:

    def __init__(self, app):
        
        self.app =app

        self.frame=customtkinter.CTkFrame(master=self.app, width=500, height=500,corner_radius=5,border_width=3,border_color="#77B5FE",fg_color="white")
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.msg=customtkinter.CTkLabel(master=self.frame, text="Creating account",compound="top",font=("Apple Chancery, cursive",30 ),text_color="blue")
        self.msg.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

        self.name = customtkinter.CTkEntry(self.frame, placeholder_text="Name",width=250, height=35,font=("cursive",15 ),border_color="#859BF5",border_width=3)
        self.name.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.email = customtkinter.CTkEntry(self.frame, placeholder_text="Email",width=250, height=35,font=("cursive",17 ),border_color="#859BF5",border_width=3)
        self.email.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

        self.password = customtkinter.CTkEntry(self.frame, placeholder_text="Password",width=250, height=35,font=("cursive",17 ),border_color="#859BF5",border_width=3)
        self.password.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.age = customtkinter.CTkEntry(self.frame, placeholder_text="Age",width=250, height=35,font=("cursive",17 ),border_color="#859BF5",border_width=3)
        self.age.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        self.adress = customtkinter.CTkEntry(self.frame, placeholder_text="Adress",width=250, height=35,font=("cursive",17 ),border_color="#859BF5",border_width=3)
        self.adress.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        self.create=customtkinter.CTkButton(self.frame, text="Create an account",width=120,fg_color="red",command=lambda:self.create_account())
        self.create.place(relx=0.35, rely=0.85, anchor=tkinter.CENTER)

        self.loogin=customtkinter.CTkButton(self.frame, text="Log in",width=120,fg_color="green",command=lambda:self.Login())
        self.loogin.place(relx=0.66, rely=0.85, anchor=tkinter.CENTER)

    def create_account(self):# Function to handle account creation logic
        name = self.name.get()
        email = self.email.get()
        password = self.password.get()
        age = self.age.get()
        adress = self.adress.get()
        permission = 0
        if name=="" or email=="" or age=="" or adress==""or age<"18":
            messagebox.showerror("Error", "field is empty or wrong!")
        else:
            request_sql_creat_member="SELECT * FROM member WHERE email='"+email+"'"
            new_member=mysqlconnect(request_sql_creat_member)
            if len(new_member) != 0:
                messagebox.showerror("Error", "User already exists!")
                return

            request_sql_creat_member="INSERT INTO member (name, email, password, age, adress, permission) VALUES ('"+name+"', '"+email+"', '"+password+"', '"+age+"', '"+adress+"', 0)"
            new_member=mysqlconnect(request_sql_creat_member)
            member_id=mysqlconnect("Select member_id from member where email='"+email+"' and password='"+password+"'")
            messagebox.showinfo("Success", "Account created successfully!")
            for widget in self.frame.winfo_children():
                widget.destroy()
            self.frame.destroy()
            bookingapp(self.app,member_id[0][0])

    def Login(self):# Function to switch to the login GUI
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        login_gui(self.app)

class AdminGUI:

    def __init__(self, app):# Initialize the GUI components for admin interface

        self.app=app
        
        self.frame=customtkinter.CTkFrame(master=self.app, width=1222, height=200,corner_radius=5,border_width=3,border_color="#77B5FE",fg_color="white")
        self.frame.place(relx=0.5, rely=0.19, anchor=tkinter.CENTER)
        

        self.departure_airport = customtkinter.CTkEntry(self.frame,border_width=2,width=200,border_color="#77B5FE",placeholder_text="Select Departure Airport")
        self.departure_airport.place(relx=0.1, rely=0.4, anchor=tkinter.CENTER)
        
        self.arrival_airport = customtkinter.CTkEntry(self.frame,border_width=2,width=200,border_color="#77B5FE",placeholder_text="Select Arrival Airport")
        self.arrival_airport.place(relx=0.3, rely=0.4, anchor=tkinter.CENTER)        
        
        self.departure_date = DateEntry(self.frame, width=12, background='darkblue',
                                           foreground='white', borderwidth=2, 
                                           font=("cursive", 15), year=datetime.datetime.now().year,
                                           month=datetime.datetime.now().month, day=datetime.datetime.now().day,
                                           date_pattern='y-mm-dd')
        self.departure_date.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

        self.time = customtkinter.CTkEntry(self.frame, placeholder_text="Time flight",width=200,font=("cursive",15 ),border_color="#77B5FE",border_width=2)
        self.time.place(relx=0.7, rely=0.4, anchor=tkinter.CENTER)

        self.takeoff = customtkinter.CTkEntry(self.frame, placeholder_text="Take off time",width=200,font=("cursive",15 ),border_color="#77B5FE",border_width=2)
        self.takeoff.place(relx=0.7, rely=0.7, anchor=tkinter.CENTER)

        self.number = customtkinter.CTkEntry(self.frame, placeholder_text="Flight number",width=200,font=("cursive",15 ),border_color="#77B5FE",border_width=2)
        self.number.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
        
        self.price = customtkinter.CTkEntry(self.frame, placeholder_text="Price",width=200,font=("cursive",15 ),border_color="#77B5FE",border_width=2)
        self.price.place(relx=0.3, rely=0.7, anchor=tkinter.CENTER)

        self.spinbox_1 = FloatSpinbox(self.frame, width=140, step_size=1)
        self.spinbox_1.place(relx=0.1, rely=0.7, anchor=tkinter.CENTER)

        self.search=customtkinter.CTkButton(self.frame, text="ADD A FLIGHT",width=200,height=90,fg_color="red",font=("cursive",23 ),command=lambda:self.add(),corner_radius=10)
        self.search.place(relx=0.89, rely=0.56, anchor=tkinter.CENTER)
        
        self.log_out=customtkinter.CTkButton(self.frame, text="LOG OUT",width=100,height=20,text_color="black",fg_color="white",font=("cursive",15),command=lambda:self.logout(),corner_radius=0)
        self.log_out.place(relx=0.05, rely=0.1, anchor=tkinter.CENTER)

        self.log_out=customtkinter.CTkButton(self.frame, text="USERS",width=80,height=20,text_color="black",fg_color="white",font=("cursive",15),command=lambda:self.users(),corner_radius=0)
        self.log_out.place(relx=0.26, rely=0.1, anchor=tkinter.CENTER)
        
        self.remoove=customtkinter.CTkButton(self.frame, text="REMOVE A FLIGHT",width=100,height=20,text_color="black",fg_color="white",font=("cursive",15),command=lambda:self.update(),corner_radius=0)
        self.remoove.place(relx=0.16, rely=0.1, anchor=tkinter.CENTER)
        
        self.framea=customtkinter.CTkFrame(master=self.app, width=1220, height=500,border_color="#77B5FE",fg_color="white")
        self.framea.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)
        
        vendu=mysqlconnect("SELECT CONCAT(flight.departure_airport,'/',flight.arrival_airport),  SUM(historique.number) AS number,flight.place FROM flight, historique Where flight.flight_id=historique.flight_id GROUP BY flight.flight_id")
        X=Y=[]
        for element in vendu:
            if element[2]==0:
                pass
            else:
                X=X+[element[0]]
                Y=Y+[element[1]]
            
        fig1,ax1=plt.subplots()
        ax1=plt.bar(X,Y)
        ax1=plt.ylim(0, max(Y)+20)
        ax1=plt.xlabel("City")
        ax1=plt.ylabel("Number of flights")
        ax1=plt.title("Flight analysis")
        
        Canvas1=FigureCanvasTkAgg(fig1,self.framea)
        Canvas1.get_tk_widget().place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)
        
    def update(self):# Function to handle updating flight information
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        for widget in self.framea.winfo_children():
            widget.destroy()
        self.framea.destroy()
        updateFlightGUI(self.app)

    def users(self):# Function to view user information
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        for widget in self.framea.winfo_children():
            widget.destroy()
        self.framea.destroy()
        adminview(self.app)
        
    
    def logout(self):# Function to handle logout logic
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        for widget in self.framea.winfo_children():
            widget.destroy()
        self.framea.destroy()
        login_gui(self.app)
        

    def add(self):# Function to handle adding a new flight
        depart=self.departure_airport.get()
        arrival=self.arrival_airport.get()
        departd=self.departure_date.get()
        flightnumber=self.number.get()
        takeoff=self.takeoff.get()
        duration=self.time.get()
        number=self.spinbox_1.get()
        price=self.price.get()

        if depart=="" or arrival=="" or departd=="" or flightnumber=="" or takeoff=="" or duration=="" or price=="":
            messagebox.showerror("Error", "field is empty!")
        else:
            request_sql_new_flight="INSERT INTO flight (flight_number, departure_airport, arrival_airport, departing, timings, take_off_time, place, price) VALUES ('"+flightnumber+"','"+depart+"', '"+arrival+"', '"+departd+"', '"+duration+"','"+takeoff+"', '"+str(number)+"','"+price+"')"
            mysqlconnect( request_sql_new_flight)
            messagebox.showinfo("Success", "Flight add successfully!")



class bookGUI:
   
    def __init__(self, app, price, member_id, number, flight_id1, flight_id2):
        # Initialize the bookGUI class with parameters like app instance, price, member ID, etc.
        self.app = app
        self.member_id = member_id

        # Check if the number of passengers is more than 1
        if int(number) - 1 != 0:
            # Create and place the main frame of the GUI
            self.frame = customtkinter.CTkFrame(master=self.app, width=500, height=500, corner_radius=5, border_width=3, border_color="#77B5FE", fg_color="white")
            self.frame.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

            # Add a title label
            self.msg = customtkinter.CTkLabel(master=self.frame, text="Booking a flight", compound="top", font=("Arial, Helvetica, sans-serif", 30), text_color="#0066cc")
            self.msg.place(relx=0.5, rely=0.08, anchor=tkinter.CENTER)

            # Create a frame and a scrollable frame inside it for passenger details
            self.fr = customtkinter.CTkFrame(master=self.frame, width=230, height=330, fg_color="white")
            self.fr.place(relx=0.5, rely=0.48, anchor=tkinter.CENTER)
            self.info = customtkinter.CTkScrollableFrame(master=self.fr, width=210, height=320, fg_color="white")
            self.info.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

            # Initialize variables for passenger names and ages
            c = 1
            l = 0
            request_sql_age = "SELECT age FROM member WHERE member_id='" + str(member_id) + "'"
            age = mysqlconnect(request_sql_age)
            if len(age) == 0:
                self.agepass = [None] * int(number)
            if len(age) != 0:
                self.agepass = [int(age[0][0])] + [None] * int(number - 1)
            self.namepass = [None] * int(number - 1)

            # Create entry fields for passenger names and ages
            for i in range(1, int(2 * number) - 1, 2):
                self.namepass[l] = customtkinter.CTkEntry(self.info, placeholder_text="Name Passenger" + str(c), width=200, height=35, font=("cursive", 15), border_color="#859BF5", border_width=3)
                self.namepass[l].grid(row=i)
                self.agepass[c] = customtkinter.CTkEntry(self.info, placeholder_text="Age Passenger" + str(c), width=200, height=35, font=("cursive", 15), border_color="#859BF5", border_width=3)
                self.agepass[c].grid(row=i + 1, pady=10)
                c = c + 1
                l = l + 1

            # Create buttons for payment and going back
            self.pay = customtkinter.CTkButton(self.frame, text="PAY", width=100, height=40, fg_color="red", font=("cursive", 23), command=lambda: self.payer(flight_id1, flight_id2, member_id, number, price), corner_radius=10)
            self.pay.place(relx=0.65, rely=0.9, anchor=tkinter.CENTER)
            self.goback = customtkinter.CTkButton(self.frame, text="GO BACK", width=100, height=40, fg_color="white", text_color="black", font=("cursive", 23), command=lambda: self.back(), corner_radius=10)
            self.goback.place(relx=0.4, rely=0.9, anchor=tkinter.CENTER)
        else:
            # If there's only one passenger, call BOOKGUI again with the same parameters
            BOOKGUI(self.app, price, member_id, number, flight_id1, flight_id2)

    def payer(self, flight_id1, flight_id2, member_id, number, pricee):
        # Initialize total price and a flag variable
        price = 0
        c = 1

        # Loop through all age entries to calculate total price
        for i in range(0, len(self.agepass)):
            if self.agepass[0] == None:
                # If the first age entry is None, add full price
                price = float(price + pricee)
                c = c * 1
            elif type(self.agepass[i]) != int:
                # Get the age from the entry, check if it is empty
                age = self.agepass[i].get()
                if age == '':
                    # Show error message if any age entry is empty
                    messagebox.showerror('', 'Error: There is an empty entry area')
                    c = c * 0
                    break
                else:
                    # Calculate price based on age criteria
                    if (int(age) > 21 and int(age) < 67):
                        price = float(price + pricee)
                    else:
                        price = float(price + pricee * 0.8)
                    c = c * 1
            else:
                # Calculate price for the first passenger
                if (int(self.agepass[0]) > 21 and int(self.agepass[0]) < 67):
                    price = float(price + pricee)
                else:
                    price = float(price + pricee * 0.8)
                c = c * 1
        
        # Check if all entries are valid and proceed to the next GUI
        if c == 1:
            # Clear the current frame and call BOOKGUI with updated price
            for widget in self.frame.winfo_children():
                widget.destroy()
            self.frame.destroy()
            BOOKGUI(self.app, price, member_id, number, flight_id1, flight_id2)
        else:
            # If there's an error in input, return from the function
            return

    def back(self):
        # Function to handle the 'back' action
        # Clears the current frame and switches to the booking application
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        bookingapp(self.app, self.member_id)

class BOOKGUI:
    def __init__(self, app, price, member_id, number, flight_id1, flight_id2):
        # Constructor for the BOOKGUI class
        self.app = app
        self.member_id = member_id

        # Create the main frame of the booking GUI
        self.frame = customtkinter.CTkFrame(master=self.app, width=500, height=500, corner_radius=5, border_width=3, border_color="#77B5FE", fg_color="white")
        self.frame.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

        # Add a title label to the frame
        self.msg = customtkinter.CTkLabel(master=self.frame, text="Booking a flight", compound="top", font=("Arial, Helvetica, sans-serif", 30), text_color="#0066cc")
        self.msg.place(relx=0.5, rely=0.08, anchor=tkinter.CENTER)

        # Create a frame to contain the booking details
        self.frame1 = customtkinter.CTkFrame(master=self.frame, width=494, height=400, fg_color="white")
        self.frame1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # Display the price of the booking
        self.price = customtkinter.CTkLabel(master=self.frame1, text=f"Price: {price}$", text_color="red", font=("Arial, Helvetica, sans-serif", 25))
        self.price.place(relx=0.5, rely=0.20, anchor=tkinter.CENTER)

        # Create entry fields for payment information like name on card, card number, etc.
        self.namecard = customtkinter.CTkEntry(self.frame1, placeholder_text="Name on the card", width=250, height=35, font=("cursive", 15), border_color="#859BF5", border_width=3)
        self.namecard.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.numbercard = customtkinter.CTkEntry(self.frame1, placeholder_text="card number", width=250, height=35, font=("cursive", 15), border_color="#859BF5", border_width=3)
        self.numbercard.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        self.cvv = customtkinter.CTkEntry(self.frame1, placeholder_text="CVV", width=60, height=35, font=("cursive", 15), border_color="#859BF5", border_width=3)
        self.cvv.place(relx=0.31, rely=0.7, anchor=tkinter.CENTER)

        self.dateexp = customtkinter.CTkEntry(self.frame1, placeholder_text="MM/YYYY", width=60, height=35, font=("cursive", 15), border_color="#859BF5", border_width=3)
        self.dateexp.place(relx=0.51, rely=0.7, anchor=tkinter.CENTER)

        # Create buttons for payment and going back
        self.pay = customtkinter.CTkButton(self.frame1, text="PAY", width=100, height=40, fg_color="red", font=("cursive", 23), command=lambda: self.payer(flight_id1, flight_id2, member_id, number), corner_radius=10)
        self.pay.place(relx=0.65, rely=0.9, anchor=tkinter.CENTER)

        self.goback = customtkinter.CTkButton(self.frame1, text="GO BACK", width=100, height=40, fg_color="white", text_color="black", font=("cursive", 23), command=lambda: self.back(), corner_radius=10)
        self.goback.place(relx=0.4, rely=0.9, anchor=tkinter.CENTER)

    def payer(self, flight_id1, flight_id2, member_id, number):
        # Function to handle payment processing
        # Retrieves card details and performs validation
        namecard = self.namecard.get()
        numbercard = self.numbercard.get()
        cvv = self.cvv.get()
        dateexp = str(self.dateexp.get())
        date_actuelle = str(datetime.datetime.now().month)
        anne_actuelle = str(datetime.datetime.now().year)

        # Validation checks for card details
        if namecard == '' or len(str(numbercard)) != 14 or len(str(cvv)) != 3 or date_actuelle > dateexp[:2] or anne_actuelle > dateexp[-4:]:
            messagebox.showerror('', 'Error: There is somthing wrong')
        else:
            # Insert the booking details into the database and update flight information
            request_historic1 = (f"INSERT INTO historique (member_id, flight_id, number) VALUES ('{member_id}', '{flight_id1}', '{number}')")
            mysqlconnect(request_historic1)
            request_number1 = (f"UPDATE flight SET place=place - '{number}' WHERE flight_id = '{flight_id1}' ")
            mysqlconnect(request_number1)

            # If there is a return flight, process it similarly
            if int(flight_id2) != 0:
                request_historic2 = (f"INSERT INTO historique (member_id, flight_id, number) VALUES ('{member_id}', '{flight_id2}', '{number}')")
                request_number2 = (f"UPDATE flight SET place=place - '{number}' WHERE flight_id = '{flight_id2}' ")
                mysqlconnect(request_historic2)
                mysqlconnect(request_number2)

            # Display success message
            messagebox.showinfo("Success", "Account created successfully!")

    
    def back(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        bookingapp(self.app,self.member_id)


class HistoricGUI:
    def __init__(self, app, member_id):
        # Constructor for the HistoricGUI class
        self.app = app
        self.member_id = member_id

        # Create a label for the title of the historic flights section
        self.title = customtkinter.CTkLabel(self.app, width=1222, height=60, text="Historic Flights", text_color="white", font=("cursive", 30), fg_color="#5077F5")
        self.title.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)

        # Create a frame to hold the historic flight information
        self.tampon = customtkinter.CTkFrame(master=self.app, width=1222, height=500, border_color="#77B5FE", fg_color="white")
        self.tampon.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

        # Add a scrollable frame inside the main frame for displaying flight details
        self.frameee = customtkinter.CTkScrollableFrame(master=self.tampon, width=1200, height=500, border_color="#77B5FE", fg_color="white")
        self.frameee.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # Call the method to display historic flight information
        self.afficher_historique()

        # Create a 'Go Back' button to return to the previous screen
        self.goback = customtkinter.CTkButton(self.tampon, text="GO BACK", width=100, height=40, fg_color="white", text_color="black", font=("cursive", 23), command=lambda: self.back(), corner_radius=10)
        self.goback.place(relx=0.51, rely=0.95, anchor=tkinter.CENTER)

    def back(self):
        # Function to handle the 'back' action
        # Clears all widgets in the frame and destroys the frame and title
        # Returns to the booking application
        for widget in self.tampon.winfo_children():
            widget.destroy()
        self.tampon.destroy()
        self.title.destroy()
        bookingapp(self.app, self.member_id)

    def afficher_historique(self):
        # Function to display the historic flights of a member
        # Queries the database for historic flight information
        sql_query = "SELECT flight_id, sum(number) as number FROM `historique` WHERE member_id =" + str(self.member_id) + " group BY flight_id"
        historique_vols = mysqlconnect(sql_query)

        # Check if there are historic flights and display them
        if len(historique_vols) != 0:
            for i in range(0, len(historique_vols)):
                # Retrieve flight details for each historic flight
                flight_departure = mysqlconnect("Select * from flight where flight_id=" + str(historique_vols[i][0]))

                # Create a frame for each flight and display flight details
                self.frame_flight = customtkinter.CTkFrame(self.frameee, width=1180, height=60, corner_radius=0, border_width=4, border_color="#968080", fg_color="white")
                self.frame_flight.grid(row=i, padx=10, pady=10)
                self.info_flight = customtkinter.CTkLabel(self.frame_flight, text=str(historique_vols[i][1]) + " flight(s) for " + flight_departure[0][2] + " to " + flight_departure[0][3] + " take off time the " + str(flight_departure[0][4]) + " at " + str(flight_departure[0][6])[:-3] + " flight time " + str(flight_departure[0][5]), text_color="black", font=("cursive", 25), fg_color="transparent")
                self.info_flight.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        

class modifier:

    def __init__(self, app, flight_id):

        self.app=app
        sql_query ="SELECT * FROM flight where flight_id="+str(flight_id)
        flight_historic = mysqlconnect(sql_query)
        
        self.frame=customtkinter.CTkFrame(master=self.app, width=1222, height=250,corner_radius=5,border_width=3,border_color="#77B5FE",fg_color="white")
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.departure_airport = customtkinter.CTkEntry(self.frame,border_width=2,width=200,border_color="#77B5FE",placeholder_text=flight_historic[0][2])
        self.departure_airport.place(relx=0.1, rely=0.4, anchor=tkinter.CENTER)
        
        self.arrival_airport = customtkinter.CTkEntry(self.frame,border_width=2,width=200,border_color="#77B5FE",placeholder_text=flight_historic[0][3])
        self.arrival_airport.place(relx=0.3, rely=0.4, anchor=tkinter.CENTER)
        
        self.departure_date =DateEntry(self.frame, width=12, background='darkblue',
                                           foreground='white', borderwidth=2, 
                                           font=("cursive", 15), year=datetime.datetime.now().year,
                                           month=datetime.datetime.now().month, day=datetime.datetime.now().day,
                                           date_pattern='y-mm-dd')

        self.departure_date.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

        self.time = customtkinter.CTkEntry(self.frame, placeholder_text=flight_historic[0][5],width=200,font=("cursive",15 ),border_color="#77B5FE",border_width=2)
        self.time.place(relx=0.7, rely=0.4, anchor=tkinter.CENTER)

        self.takeoff = customtkinter.CTkEntry(self.frame, placeholder_text=flight_historic[0][6],width=200,font=("cursive",15 ),border_color="#77B5FE",border_width=2)
        self.takeoff.place(relx=0.7, rely=0.7, anchor=tkinter.CENTER)

        self.number = customtkinter.CTkEntry(self.frame, placeholder_text=flight_historic[0][1],width=200,font=("cursive",15 ),border_color="#77B5FE",border_width=2)
        self.number.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
        
        self.price = customtkinter.CTkEntry(self.frame, placeholder_text=flight_historic[0][8],width=200,font=("cursive",15 ),border_color="#77B5FE",border_width=2)
        self.price.place(relx=0.3, rely=0.7, anchor=tkinter.CENTER)

        self.spinbox_1 = FloatSpinbox(self.frame, width=140, step_size=1)
        self.spinbox_1.place(relx=0.1, rely=0.7, anchor=tkinter.CENTER)

        self.search=customtkinter.CTkButton(self.frame, text="MODIFY",width=100,height=20,fg_color="red",font=("cursive",23 ),command=lambda:self.modify(flight_id),corner_radius=10)
        self.search.place(relx=0.89, rely=0.4, anchor=tkinter.CENTER)

        self.search=customtkinter.CTkButton(self.frame, text="DELETE",width=100,height=20,fg_color="red",font=("cursive",23 ),command=lambda:self.delete(flight_id),corner_radius=10)
        self.search.place(relx=0.89, rely=0.7, anchor=tkinter.CENTER)
        
        self.log_out = customtkinter.CTkButton(self.frame, text="GO BACK", width=100, height=30, fg_color="green", font=("cursive", 20),command=lambda:self.update(), corner_radius=10)        
        self.log_out.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

    def delete(self, flight_id):
        # Function to delete the flight from the database
        sql_delete = "DELETE FROM flight WHERE flight_id =" + str(flight_id)
        mysqlconnect(sql_delete)
        sql_delete = "DELETE FROM historique WHERE flight_id =" + str(flight_id)
        mysqlconnect(sql_delete)
        messagebox.showinfo("Success", "Flight deleted successfully!")


    def modify(self, flight_id):
        # Function to modify the flight details
        # Deletes the existing flight entry and creates a new one with updated details
        sql_delete = "DELETE FROM flight WHERE flight_id =" + str(flight_id)
        mysqlconnect(sql_delete)
        depart=self.departure_airport.get()
        arrival=self.arrival_airport.get()
        departd=self.departure_date.get()
        flightnumber=self.number.get()
        takeoff=self.takeoff.get()
        duration=self.time.get()
        number=self.spinbox_1.get()
        price=self.price.get()

        if depart=="" or arrival=="" or departd=="" or flightnumber=="" or takeoff=="" or duration=="" or price=="":
            messagebox.showerror("Error", "field is empty!")
        else:
            request_sql_new_flight="INSERT INTO flight (flight_number, departure_airport, arrival_airport, departing, timings, take_off_time, place, price) VALUES ('"+flightnumber+"','"+depart+"', '"+arrival+"', '"+departd+"', '"+duration+"','"+takeoff+"', '"+str(number)+"','"+price+"')"
            mysqlconnect( request_sql_new_flight)

            messagebox.showinfo("Success", "Flight updated successfully!")

    def update(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        updateFlightGUI(self.app)

        
class user:
    def __init__(self, app, member_id):
        
        self.app = app
        self.member_id=member_id
        sql_query = "SELECT * FROM member WHERE member_id = "+str(member_id)
        member_data = mysqlconnect(sql_query)
        self.frame = customtkinter.CTkFrame(master=self.app, width=600, height=400, corner_radius=5, border_width=2, border_color="#77B5FE", fg_color="white")
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.name_label = customtkinter.CTkLabel(self.frame, text="Name:", width=150, font=("cursive", 15), fg_color="transparent")
        self.name_label.place(relx=0.2, rely=0.2, anchor=tkinter.CENTER)

        self.name_entry = customtkinter.CTkEntry(self.frame, width=300, font=("cursive", 15), border_color="#77B5FE", border_width=2, placeholder_text=member_data[0][1])
        self.name_entry.place(relx=0.6, rely=0.2, anchor=tkinter.CENTER)

        self.email_label = customtkinter.CTkLabel(self.frame, text="Email:", width=150, font=("cursive", 15), fg_color="transparent")
        self.email_label.place(relx=0.2, rely=0.3, anchor=tkinter.CENTER)

        self.email_entry = customtkinter.CTkEntry(self.frame, width=300, font=("cursive", 15), border_color="#77B5FE", border_width=2, placeholder_text=member_data[0][2])
        self.email_entry.place(relx=0.6, rely=0.3, anchor=tkinter.CENTER)

        self.age_label = customtkinter.CTkLabel(self.frame, text="Age:", width=150, font=("cursive", 15), fg_color="transparent")
        self.age_label.place(relx=0.2, rely=0.4, anchor=tkinter.CENTER)

        self.age_entry = customtkinter.CTkEntry(self.frame, width=300, font=("cursive", 15), border_color="#77B5FE", border_width=2, placeholder_text=str(member_data[0][4]))
        self.age_entry.place(relx=0.6, rely=0.4, anchor=tkinter.CENTER)

        self.address_label = customtkinter.CTkLabel(self.frame, text="Address:", width=150, font=("cursive", 15), fg_color="transparent")
        self.address_label.place(relx=0.2, rely=0.5, anchor=tkinter.CENTER)

        self.address_entry = customtkinter.CTkEntry(self.frame, width=300, font=("cursive", 15), border_color="#77B5FE", border_width=2, placeholder_text=member_data[0][5])
        self.address_entry.place(relx=0.6, rely=0.5, anchor=tkinter.CENTER)

        self.update_button = customtkinter.CTkButton(self.frame, text="Update", width=100, height=30, fg_color="red", font=("cursive", 20), command=self.update_data, corner_radius=10)
        self.update_button.place(relx=0.6, rely=0.7, anchor=tkinter.CENTER)
        
        self.go_back = customtkinter.CTkButton(self.frame, text="GO BACK", width=100, height=30, fg_color="green", font=("cursive", 20), command=self.goback, corner_radius=10)
        self.go_back.place(relx=0.4, rely=0.7, anchor=tkinter.CENTER)
        

    def update_data(self):
        # Retrieves the input values from the GUI entry fields.
        name = self.name_entry.get()   # Gets the name from the name entry field.
        email = self.email_entry.get() # Gets the email from the email entry field.
        age = self.age_entry.get()     # Gets the age from the age entry field.
        address = self.address_entry.get() # Gets the address from the address entry field.
        # Constructs an SQL update query to modify the member's details in the database.
        # It updates the name, email, age, and address for a specific member_id.
        update_query = "UPDATE member SET name='" + name + "', email='" + email + "', age=" + age + ", adress='" + address + "' WHERE member_id=" + str(self.member_id)
        # Executes the SQL query to update the member information in the database.
        # The `mysqlconnect` function (defined elsewhere) likely handles the database connection and executes the SQL command.
        mysqlconnect(update_query)
        # Displays a messagebox to inform the user that the data update was successful.
        messagebox.showinfo("Success", "Your data has been updated successfully!")
    
    def goback(self):
            for widget in self.frame.winfo_children():
                widget.destroy()
            self.frame.destroy()
            bookingapp(self.app,self.member_id)
        

class adminview:
    
    def __init__(self, app):
        # Initializes the AdminView class with a reference to the main application window.
        self.app = app

        # Creates a label widget at the top of the window, displaying the text "Historic Flights".
        self.title = customtkinter.CTkLabel(self.app, width=1222, height=60, text="Users", text_color="white", font=("cursive", 30), fg_color="#5077F5")
        self.title.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)
        
        # Creates a main frame (container) for other widgets.
        self.tampon = customtkinter.CTkFrame(master=self.app, width=1222, height=500, border_color="#77B5FE", fg_color="white")
        self.tampon.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

        # Creates a scrollable frame inside the main frame for displaying member data.
        self.frameee = customtkinter.CTkScrollableFrame(master=self.tampon, width=1200, height=500, border_color="#77B5FE", fg_color="white")
        self.frameee.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # Calls the method to display member data in the scrollable frame.
        self.afficher_membre()

        # Creates a "GO BACK" button for navigation.
        self.goback = customtkinter.CTkButton(self.tampon, text="GO  BACK", width=100, height=40, fg_color="white", text_color="black", font=("cursive", 23), command=lambda: self.back(), corner_radius=10)
        self.goback.place(relx=0.51, rely=0.95, anchor=tkinter.CENTER)

    def afficher_membre(self):
        # Queries the database for member data and displays each member in the scrollable frame.
        sql_query = "SELECT * FROM member"
        member_data = mysqlconnect(sql_query)
        if len(member_data) != 0:
            for i in range(0, len(member_data)):
                # Determines if the member is an admin or a user.
                h = "admin" if str(member_data[i][6]) == '1' else "user"
                
                # Creates a frame for each member to display their details.
                self.frame_flight = customtkinter.CTkFrame(self.frameee, width=1180, height=60, corner_radius=0, border_width=4, border_color="#968080", fg_color="white")
                self.frame_flight.grid(row=i, padx=10, pady=10)
                
                # Displays member information in a label.
                self.info_flight = customtkinter.CTkLabel(self.frame_flight, text=f"Name={member_data[i][1]} Email={member_data[i][2]} Password={member_data[i][3]} Age={member_data[i][4]} Adress={member_data[i][5][:-3]} type of user={h}", text_color="black", font=("cursive", 20), fg_color="transparent")
                self.info_flight.place(relx=0.4, rely=0.5, anchor=tkinter.CENTER)
                
                # Creates a "DELETE" button for each member.
                self.button = customtkinter.CTkButton(self.frame_flight, text="DELETE", width=100, height=40, fg_color="RED", text_color="black", font=("cursive", 23), command=lambda: self.mdr(member_data[i][0]), corner_radius=10)
                self.button.place(relx=0.9, rely=0.5, anchor=tkinter.CENTER)


    def mdr(self, member_id):
        # Deletes the selected member from the database.
        sql_query = f"DELETE FROM member where member_id={member_id}"
        mysqlconnect(sql_query)
        messagebox.showinfo("Success", "Account deleted successfully!")

    def back(self):
        # Destroys the current widgets and navigates back to the AdminGUI.
        for widget in self.tampon.winfo_children():
            widget.destroy()
        self.tampon.destroy()
        self.title.destroy()
        AdminGUI(self.app)


class updateFlightGUI:
    def __init__(self, app):
        # Constructor for the updateFlightGUI class
        self.app = app

        self.title = customtkinter.CTkLabel(self.app, width=1222, height=60,text="Modify flights", text_color="white",font=("cursive",30 ), fg_color="#5077F5")
        self.title.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)
        
        self.tampon=customtkinter.CTkFrame(master=self.app, width=1222, height=500,border_color="#77B5FE",fg_color="white")
        self.tampon.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)
        self.frameee=customtkinter.CTkScrollableFrame(master=self.tampon, width=1200, height=500,border_color="#77B5FE",fg_color="white")
        self.frameee.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        # Call the method to display existing flight information
        self.afficher_historique()
        self.goback=customtkinter.CTkButton(self.tampon, text="GO  BACK",width=100,height=40,fg_color="white",text_color="black",font=("cursive",23 ),command=lambda:self.back(),corner_radius=10)
        self.goback.place(relx=0.51, rely=0.95, anchor=tkinter.CENTER)
    
    def back(self):
        # Function to handle the 'back' action
        # Clears all widgets in the frame and destroys the frame and title
        # Returns to the AdminGUI
        for widget in self.tampon.winfo_children():
            widget.destroy()
        self.tampon.destroy()
        self.title.destroy()
        AdminGUI(self.app)
            
    def afficher_historique(self):
        # Function to display the existing flights
        # Queries the database for all flight information
        sql_query = "SELECT * FROM flight"
        flight_historic = mysqlconnect(sql_query)
        # Check if there are flights and display them
        if len(flight_historic)!=0: 
            for i in range(0,len(flight_historic)): 
                    self.frame_flight = customtkinter.CTkFrame(self.frameee,width=1180,height=60,corner_radius=0,border_width=4, border_color="#968080",fg_color="white")
                    self.frame_flight.grid(row=i,padx=10, pady=10)                
                    self.info_flight = customtkinter.CTkLabel(self.frame_flight, text="From "+flight_historic[i][2]+" to "+flight_historic[i][3]+" as "+flight_historic[i][1]+" at "+str(flight_historic[0][4])+" and price="+str(flight_historic[i][8])+" and "+str(flight_historic[i][7])+" places               ", text_color="black",font=("cursive",25),fg_color="transparent")
                    self.info_flight.place(relx=0.45, rely=0.5, anchor=tkinter.CENTER)

                    self.goback=customtkinter.CTkButton(self.frame_flight, text="UPDATE",width=100,height=40,fg_color="RED",text_color="black",font=("cursive",23 ),corner_radius=10,command=lambda:self.modifier(flight_historic[i][0]))
                    self.goback.place(relx=0.9, rely=0.5, anchor=tkinter.CENTER)

    def modifier(self, flight_id):
        # Function to handle flight modification
        # Clears current frames and switches to the modifier GUI for the selected flight
        for widget in self.tampon.winfo_children():
            widget.destroy()
        self.tampon.destroy()
        self.title.destroy()
        modifier(self.app, flight_id)
                
def main():
    app = tkinter.Tk()
    app.title('SkyJourney Booker')
    app.state('zoomed')
    background =customtkinter.CTkImage(Image.open("background.png"),size=(app.winfo_screenwidth(), app.winfo_screenheight()))
    l1 = customtkinter.CTkLabel(master=app,image=background,text="")
    l1.pack(fill='both', expand=True)
    app1 = login_gui(l1)
    app.mainloop()
    
if __name__ == "__main__":
    main()