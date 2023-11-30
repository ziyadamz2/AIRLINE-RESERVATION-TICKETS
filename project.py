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
customtkinter.set_appearance_mode("light")

def mysqlconnect(test):
    conn = pymysql.connect(host='localhost',user='root',password="",db='project_oop')
    cur = conn.cursor()
    cur.execute(test)
    conn.commit()
    output = cur.fetchall()
    cur.close()
    conn.close()
    return(output)

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
    def __init__(self,l1):
        

        self.l1=l1
        self.frame=customtkinter.CTkFrame(master=self.l1, width=500, height=400,corner_radius=5,border_width=3,border_color="#77B5FE",fg_color="white")
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.msg=customtkinter.CTkLabel(master=self.frame, text="Airline Reservation Ticket",compound="top",font=("Apple Chancery, cursive",30 ),text_color="blue")
        self.msg.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

        self.email = customtkinter.CTkEntry(self.frame, placeholder_text="Email",width=250, height=35,font=("cursive",15 ),border_color="#859BF5",border_width=3)
        self.email.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.password = customtkinter.CTkEntry(self.frame, placeholder_text="Password",width=250, height=35,font=("cursive",17 ),border_color="#859BF5",border_width=3)
        self.password.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)
        
        self.login=customtkinter.CTkButton(self.frame, text="Login",width=120,fg_color="green",command=lambda:self.Login(self.l1))
        self.login.place(relx=0.365, rely=0.58, anchor=tkinter.CENTER)

        self.creat_an_account=customtkinter.CTkButton(self.frame, text="Create an account",width=120,fg_color="red",command=lambda:self.creat_account())
        self.creat_an_account.place(relx=0.64, rely=0.58, anchor=tkinter.CENTER)

        self.login_as_guest=customtkinter.CTkButton(self.frame, text="Login as a guest",command=lambda:self.logiin_as_guest())
        self.login_as_guest.place(relx=0.5, rely=0.69, anchor=tkinter.CENTER)
        

        
    def Login(self,app):
        self.app=app
        email=str(self.email.get())
        password=str(self.password.get())
        request_sql_connection="select * from member where email='"+email+"' and password='"+password+"'"
        user=mysqlconnect(request_sql_connection)
        if len(user)==0:
            messagebox.showerror('Error', 'Error: wrong email or password!')
        else:                                           #A MODIFIER
            for widget in self.frame.winfo_children():
                widget.destroy()
            self.frame.destroy()

            request_sql_permission="SELECT permission,member_id FROM member WHERE email='"+email+"'"
            permission=mysqlconnect(request_sql_permission)
            if (permission[0][0]==1):
                AdminGUI(self.l1)
            else:
                bookingapp(self.l1,permission[0][1])

                
    def logiin_as_guest(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        bookingapp(self.l1,'0')
    
    def creat_account(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        CreateAccountGui(self.l1)
        

        


class bookingapp:
    def __init__(self,app,member_id):
        self.app=app

        self.frame=customtkinter.CTkFrame(master=self.app, width=1222, height=200,corner_radius=5,border_width=3,border_color="#77B5FE",fg_color="white")
        self.frame.place(relx=0.5, rely=0.19, anchor=tkinter.CENTER)
        request_sql_dairport="SELECT departure_airport FROM `flight`;"
        dairport=mysqlconnect(request_sql_dairport)
        airport=[item[0] for item in dairport]

        self.departure_airport = customtkinter.StringVar()
        self.departure_airport.set("Select Departure Airport") 
        self.departure_airport = customtkinter.CTkComboBox(self.frame,values=airport,border_width=2,variable=self.departure_airport,width=200,border_color="#77B5FE",button_color="#77B5FE")
        self.departure_airport.place(relx=0.1, rely=0.4, anchor=tkinter.CENTER)

        request_sql_dairport="SELECT arrival_airport FROM `flight`"
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
        
        
        self.my_departure_date =customtkinter.CTkEntry(self.frame, placeholder_text="departure date:yyyy-mm-dd",width=200,font=("cursive",15 ),border_color="#77B5FE",border_width=2)
        self.my_departure_date.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
        
        self.my_arrival_date = customtkinter.CTkEntry(self.frame, placeholder_text="arrival date:yyyy-mm-dd",width=200,font=("cursive",15 ),border_color="#77B5FE",border_width=2)
        self.my_arrival_date.place(relx=0.7, rely=0.4, anchor=tkinter.CENTER)
                

        self.spinbox_1 = FloatSpinbox(self.frame, width=140, step_size=1)
        self.spinbox_1.place(relx=0.1, rely=0.7, anchor=tkinter.CENTER)
        
        self.search=customtkinter.CTkButton(self.frame, text="SEARCH A FLIGHT",width=200,height=90,fg_color="red",font=("cursive",23 ),command=lambda:self.research(member_id),corner_radius=10)
        self.search.place(relx=0.89, rely=0.56, anchor=tkinter.CENTER)

        self.historic=customtkinter.CTkButton(self.frame, text="HISTORIC",width=100,height=20,text_color="black",fg_color="white",font=("cursive",15),command=lambda:self.historique(member_id),corner_radius=0)
        self.historic.place(relx=0.05, rely=0.1, anchor=tkinter.CENTER)
        
        self.log_out=customtkinter.CTkButton(self.frame, text="LOG OUT",width=100,height=20,text_color="black",fg_color="white",font=("cursive",15),command=lambda:self.logout(),corner_radius=0)
        self.log_out.place(relx=0.15, rely=0.1, anchor=tkinter.CENTER)
    
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
            
        
        
    def research(self,member_id):
        date_actuelle = str(datetime.datetime.now().month)
        anne_actuelle = str(datetime.datetime.now().year)
        jour_actuelle = str(datetime.datetime.now().day)
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
    
    def booking(self,price,member_id,number,flight_id1,flight_id2):
        for widget in self.frame.winfo_children():
            widget.destroy()
        for widget in self.frameb.winfo_children():
            widget.destroy()
        self.frame.destroy()
        self.frameb.destroy()
        bookGUI(self.app,price,member_id,number,flight_id1,flight_id2)

    def historique(self,member_id):
        if member_id=='0':
            messagebox.showerror('', 'Error: Your are not log')
            return
        else:
            for widget in self.frame.winfo_children():
                widget.destroy()
            for widget in self.frameb.winfo_children():
                widget.destroy()
            self.frame.destroy()
            self.frameb.destroy()
            HistoricGUI(self.app,member_id)
    

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

    def create_account(self):
        name = self.name.get()
        email = self.email.get()
        password = self.password.get()
        age = self.age.get()
        adress = self.adress.get()
        permission = 0
        if name=="" or email=="" or age=="" or adress=="":
            messagebox.showerror("Error", "field is empty!")
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

    def Login(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        login_gui(self.app)

class AdminGUI:

    def __init__(self, app):

        self.app=app
        
        self.frame=customtkinter.CTkFrame(master=self.app, width=1222, height=200,corner_radius=5,border_width=3,border_color="#77B5FE",fg_color="white")
        self.frame.place(relx=0.5, rely=0.19, anchor=tkinter.CENTER)
        

        self.departure_airport = customtkinter.CTkEntry(self.frame,border_width=2,width=200,border_color="#77B5FE",placeholder_text="Select Departure Airport")
        self.departure_airport.place(relx=0.1, rely=0.4, anchor=tkinter.CENTER)
        
        self.arrival_airport = customtkinter.CTkEntry(self.frame,border_width=2,width=200,border_color="#77B5FE",placeholder_text="Select Arrival Airport")
        self.arrival_airport.place(relx=0.3, rely=0.4, anchor=tkinter.CENTER)        
        
        self.departure_date =customtkinter.CTkEntry(self.frame, placeholder_text="departure date:yyyy-mm-dd",width=200,font=("cursive",15 ),border_color="#77B5FE",border_width=2)
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

    def logout(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        for widget in self.framea.winfo_children():
            widget.destroy()
        self.framea.destroy()
        login_gui(self.app)
        

    def add(self):
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
    def __init__(self,app,price,member_id,number,flight_id1,flight_id2):

        self.app =app
        self.member_id=member_id
        price=int(price)*int(number)

        self.frame=customtkinter.CTkFrame(master=self.app, width=500, height=500,corner_radius=5,border_width=3,border_color="#77B5FE",fg_color="white")
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.msg=customtkinter.CTkLabel(master=self.frame, text="Booking a flight",compound="top",font=("Arial, Helvetica, sans-serif", 30), text_color="#0066cc")
        self.msg.place(relx=0.5, rely=0.08, anchor=tkinter.CENTER)

        self.price=customtkinter.CTkLabel(master=self.frame,text=f"Price: {price}$", text_color="red",font=("Arial, Helvetica, sans-serif", 25))
        self.price.place(relx=0.25,rely=0.20, anchor=tkinter.CENTER)

        self.promotion=customtkinter.CTkLabel(master=self.frame,text='Promotion: ',text_color="black",font=("Arial, Helvetica, sans-serif", 20))
        self.promotion.place(relx=0.5,rely=0.28, anchor=tkinter.CENTER)
       

        request_sql_age="SELECT age FROM member WHERE member_id='"+str(member_id)+"'"
        age=mysqlconnect(request_sql_age)
        if (len(age)==0):
            self.promotiont=customtkinter.CTkLabel(master=self.frame,text="There is no promotion.",text_color="black",font=("Arial, Helvetica, sans-serif", 20))
            self.promotiont.place(relx=0.31,rely=0.34, anchor=tkinter.CENTER)
        elif (age[0][0]>21 and age[0][0]<67):
            self.promotiont=customtkinter.CTkLabel(master=self.frame,text="There is no promotion.",text_color="black",font=("Arial, Helvetica, sans-serif", 20))
            self.promotiont.place(relx=0.31,rely=0.34, anchor=tkinter.CENTER)
        else:
            price=int(price)*0.8
            self.promotiont=customtkinter.CTkLabel(master=self.frame,text='Promotion of 20%. The new price is: ',text_color="black",font=("Arial, Helvetica, sans-serif", 20))
            self.promotiont.place(relx=0.45,rely=0.34, anchor=tkinter.CENTER)

            self.pricet=customtkinter.CTkLabel(master=self.frame,text=str(price)+"$",text_color="red",font=("Arial, Helvetica, sans-serif", 20))
            self.pricet.place(relx=0.5,rely=0.4, anchor=tkinter.CENTER)
            
        
        self.namecard = customtkinter.CTkEntry(self.frame, placeholder_text="Name on the card",width=250, height=35,font=("cursive",15 ),border_color="#859BF5",border_width=3)
        self.namecard.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.numbercard = customtkinter.CTkEntry(self.frame, placeholder_text="card number",width=250, height=35,font=("cursive",15 ),border_color="#859BF5",border_width=3)
        self.numbercard.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        self.cvv = customtkinter.CTkEntry(self.frame, placeholder_text="CVV",width=60, height=35,font=("cursive",15 ),border_color="#859BF5",border_width=3)
        self.cvv.place(relx=0.31, rely=0.7, anchor=tkinter.CENTER)
        
        self.dateexp = customtkinter.CTkEntry(self.frame, placeholder_text="MM/YYYY",width=60, height=35,font=("cursive",15 ),border_color="#859BF5",border_width=3)
        self.dateexp.place(relx=0.51, rely=0.7, anchor=tkinter.CENTER)
        
        self.pay=customtkinter.CTkButton(self.frame, text="PAY",width=100,height=40,fg_color="red",font=("cursive",23 ),command=lambda:self.payer(flight_id1,flight_id2,member_id,number),corner_radius=10)
        self.pay.place(relx=0.65, rely=0.9, anchor=tkinter.CENTER)
        
        self.goback=customtkinter.CTkButton(self.frame, text="GO  BACK",width=100,height=40,fg_color="white",text_color="black",font=("cursive",23 ),command=lambda:self.back(),corner_radius=10)
        self.goback.place(relx=0.4, rely=0.9, anchor=tkinter.CENTER)

    def payer(self,flight_id1,flight_id2,member_id,number):
        
        namecard=self.namecard.get()
        numbercard=self.numbercard.get()
        cvv=self.cvv.get()
        dateexp=str(self.dateexp.get())

        date_actuelle = str(datetime.datetime.now().month)
        anne_actuelle = str(datetime.datetime.now().year)

        if namecard=='' or len(str(numbercard))!=14 or len(str(cvv))!=3 or date_actuelle>dateexp[:2] or anne_actuelle>dateexp[-4:]:
            messagebox.showerror('', 'Error: There is somthing wrong')
        else:
            messagebox.showerror("Success", 'Thank you for your order')
            request_historic1= (f"INSERT INTO historique (member_id,flight_id,number) VALUES ('{member_id}','{flight_id1}','{number}')")
            mysqlconnect(request_historic1)
            request_number1= (f"UPDATE flight SET place=place - '{number}' WHERE flight_id = '{flight_id1}' ")
            mysqlconnect(request_number1)
            if flight_id2!=0:
                request_historic2= (f"INSERT INTO historique (member_id,flight_id,number) VALUES ('{member_id}','{flight_id2}','{number}')")
                request_number2= (f"UPDATE flight SET place=place - '{number}' WHERE flight_id = '{flight_id2}' ")
                mysqlconnect(request_historic2)
                mysqlconnect(request_number2)
    
    def back(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        bookingapp(self.app,self.member_id)
        


class HistoricGUI:
    def __init__(self, app, member_id):
        
        self.app = app
        self.member_id = member_id
        self.title = customtkinter.CTkLabel(self.app, width=1222, height=60,text="Historic Flights", text_color="white",font=("cursive",30 ), fg_color="#5077F5")
        self.title.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)
        
        self.tampon=customtkinter.CTkFrame(master=self.app, width=1222, height=500,border_color="#77B5FE",fg_color="white")
        self.tampon.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)
        self.frameee=customtkinter.CTkScrollableFrame(master=self.tampon, width=1200, height=500,border_color="#77B5FE",fg_color="white")
        self.frameee.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)


        self.afficher_historique()
        self.goback=customtkinter.CTkButton(self.tampon, text="GO  BACK",width=100,height=40,fg_color="white",text_color="black",font=("cursive",23 ),command=lambda:self.back(),corner_radius=10)
        self.goback.place(relx=0.51, rely=0.95, anchor=tkinter.CENTER)
    
    def back(self):
            for widget in self.tampon.winfo_children():
                widget.destroy()
            self.tampon.destroy()
            self.title.destroy()
            bookingapp(self.app,self.member_id)
            

    def afficher_historique(self):
        
        sql_query ="SELECT flight_id,sum(number) as number FROM `historique` WHERE member_id ="+str(self.member_id)+" group BY flight_id"
        historique_vols = mysqlconnect(sql_query)
        if len(historique_vols)!=0:
            for i in range(0,len(historique_vols)):
                    flight_departure=mysqlconnect("Select * from flight where flight_id="+str(historique_vols[i][0]))
                    print(flight_departure)
                    self.frame_flight = customtkinter.CTkFrame(self.frameee,width=1180,height=60,corner_radius=0,border_width=4, border_color="#968080",fg_color="white")
                    self.frame_flight.grid(row=i,padx=10, pady=10)                
                    self.info_flight = customtkinter.CTkLabel(self.frame_flight, text=str(historique_vols[i][1])+" flight(s) for "+flight_departure[0][2]+" to "+flight_departure[0][3]+" take off time the "+str(flight_departure[0][4])+" at "+str(flight_departure[0][6])[:-3]+" flight time "+str(flight_departure[0][5]), text_color="black",font=("cursive",25),fg_color="transparent")
                    self.info_flight.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        
                
def main():
    app = tkinter.Tk()
    app.title('AIRLINE RESERVATION TICKET')
    app.state('zoomed')
    background =customtkinter.CTkImage(Image.open("background.png"),size=(app.winfo_screenwidth(), app.winfo_screenheight()))
    l1 = customtkinter.CTkLabel(master=app,image=background,text="")
    l1.pack(fill='both', expand=True)
    app1 = login_gui(l1)
    app.mainloop()
    
if __name__ == "__main__":
    main()