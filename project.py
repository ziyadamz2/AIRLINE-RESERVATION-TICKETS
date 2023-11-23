from customtkinter import *
import customtkinter
from tkinter import * 
from PIL import Image
import tkinter
from typing import Union, Callable
import pymysql
from CTkMessagebox import CTkMessagebox
from tkinter import messagebox


customtkinter.set_appearance_mode("light")
conn = pymysql.connect(host='localhost',user='root',password="",db='project_oop')
cur = conn.cursor()
def mysqlconnect(test):
    cur.execute(test)
    output = cur.fetchall()
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

        self.password = customtkinter.CTkEntry(self.frame, placeholder_text="Password",width=250, height=35,font=("cursive",17 ),border_color="#859BF5",border_width=3)
        self.password.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)
        
        self.login=customtkinter.CTkButton(self.frame, text="Login",width=120,fg_color="green",command=lambda:self.Login())
        self.login.place(relx=0.365, rely=0.58, anchor=tkinter.CENTER)

        self.creat_an_account=customtkinter.CTkButton(self.frame, text="Creat an account",width=120,fg_color="red",command=lambda:self.creat_account())
        self.creat_an_account.place(relx=0.64, rely=0.58, anchor=tkinter.CENTER)

        self.login_as_guest=customtkinter.CTkButton(self.frame, text="Login as a guest",command=lambda:self.logiin_as_guest())
        self.login_as_guest.place(relx=0.5, rely=0.69, anchor=tkinter.CENTER)

        
    def Login(self):
        request_sql_connection="select * from member where email='"+str(self.email.get())+"' and password='"+str(self.password.get())+"'"
        user=mysqlconnect(request_sql_connection)
        if len(user)==0:
            messagebox.showerror('', 'Error: wrong email or password!')
        else:                                           #A MODIFIER
            for widget in self.frame.winfo_children():
                widget.destroy()
            self.frame.destroy()
            #request_sql_permission="SELECT permission FROM member"
            #if request_sql_permission==1:
            bookingapp(self.app)
            #elif request_sql_permission==0: 
                
    def logiin_as_guest(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        bookingapp(self.app)
    
    def creat_account(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        CreateAccountGui(self.app)
        


class bookingapp:
    def __init__(self,app):
        self.app=app

        self.frame=customtkinter.CTkFrame(master=self.app, width=1222, height=200,border_color="#77B5FE",fg_color="white")
        self.frame.place(relx=0.5, rely=0.19, anchor=tkinter.CENTER)
        airport=["Paris", 
                "London",
                "Madrid",
                "Franckfort",
                "Amsterdam",
                "Caire | CAI",
                "Istanbul" ,
                "Djibouti"
                ]

        
        self.departure_airport = customtkinter.StringVar()
        self.departure_airport.set("Select Departure Airport") 
        self.departure_airport = customtkinter.CTkComboBox(self.frame,values=airport,border_width=2,variable=self.departure_airport,width=200,border_color="#77B5FE",button_color="#77B5FE")
        self.departure_airport.place(relx=0.1, rely=0.4, anchor=tkinter.CENTER)
        
        self.arrival_airport = customtkinter.StringVar()
        self.arrival_airport.set("Select Arrival Airport")
        self.arrival_airport = customtkinter.CTkComboBox(self.frame,values=airport,border_width=2,variable=self.arrival_airport,width=200,border_color="#77B5FE",button_color="#77B5FE")
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
        
        self.search=customtkinter.CTkButton(self.frame, text="SEARCH A FLIGHT",width=200,height=90,fg_color="red",font=("cursive",23 ),command=lambda:self.research(),corner_radius=10)
        self.search.place(relx=0.89, rely=0.56, anchor=tkinter.CENTER)
    
        self.frame_booking=customtkinter.CTkScrollableFrame(master=self.app, width=1200, height=500,border_color="#77B5FE",fg_color="white")
        self.frame_booking.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)
        self.no_result = customtkinter.CTkLabel(self.frame_booking, text="No Result For Flights", text_color="black",font=("cursive",25 ), fg_color="transparent")
        self.no_result.grid(row=0, column=2,padx=400)
        self.bar = customtkinter.CTkFrame(self.frame_booking,width=240,height=4,corner_radius=10,border_width=5, border_color="grey",fg_color="grey",)
        self.bar.grid(row=1, column=2,padx=400)
        
        
    def research(self):
        if (str(self.departure_airport.get())=='' or str(self.arrival_airport.get())=='' or str(self.Class.get())=='Select Class' or str(self.my_departure_date.get())=='' or str(self.my_arrival_date.get())=='' or str(self.spinbox_1.get())=='None'):
            messagebox.showerror('', 'Error: There is an empty entry area')
        else:
            for widget in self.frame_booking.winfo_children():
                widget.destroy()
            request_sql_departure="select * from flight where departure_airport='"+str(self.departure_airport.get())+"' and arrival_airport='"+str(self.arrival_airport.get())+"' and departing='"+str(self.my_departure_date.get())+"'"
            request_sql_arrival="select * from flight where departure_airport='"+str(self.arrival_airport.get())+"' and arrival_airport='"+str(self.departure_airport.get())+"' and departing='"+str(self.my_arrival_date.get())+"'"
            flight_departure=mysqlconnect(request_sql_departure)
            flight_arrival=mysqlconnect(request_sql_arrival)
            i=0
            if len(flight_departure)==0 and len(flight_arrival)==0 :
                self.no_result = customtkinter.CTkLabel(self.frame_booking, text="No Result For Flights", text_color="black",font=("cursive",25 ), fg_color="transparent")
                self.no_result.grid(row=0, column=2,padx=400)
                self.bar = customtkinter.CTkFrame(self.frame_booking,width=260,height=4,corner_radius=10,border_width=5, border_color="grey",fg_color="grey",)
                self.bar.grid(row=1, column=2,padx=400)
            elif len(flight_departure)==len(flight_arrival):
                for i in range(len(flight_departure)):
                    self.frame_flight = customtkinter.CTkFrame(self.frame_booking,width=1180,height=80,corner_radius=0,border_width=4, border_color="#968080",fg_color="white")
                    self.frame_flight.grid(row=i,padx=10, pady=10)
                    self.book=customtkinter.CTkButton(self.frame_flight, text="Book for "+str(flight_departure[i][8]+flight_arrival[i][8])+" £/pp",width=200,height=60,corner_radius=0,fg_color="red",font=("cursive",20 ),border_width=1,command=lambda:self.booking())
                    self.book.place(relx=0.903, rely=0.5, anchor=tkinter.CENTER)                    
                    self.frame_info_flight = customtkinter.CTkFrame(self.frame_flight,width=950,height=60,corner_radius=0,border_width=2, border_color="#968080",fg_color="white")
                    self.frame_info_flight.place(relx=0.41, rely=0.5, anchor=tkinter.CENTER)
                    self.info_flight = customtkinter.CTkLabel(self.frame_info_flight, text=flight_departure[i][2]+" to "+flight_departure[i][3]+" take off time the "+str(flight_departure[i][4])+" at "+str(flight_departure[i][6])[:-3]+" flight time "+str(flight_departure[i][5])+"\n"+flight_arrival[i][2]+" to "+flight_arrival[i][3]+" take off time the "+str(flight_arrival[i][4])+" at "+str(flight_arrival[i][6])[:-3]+" flight time "+str(flight_arrival[i][5]), text_color="black",font=("cursive",25 ),fg_color="transparent")
                    self.info_flight.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
            elif len(flight_departure)==0 or len(flight_arrival)==0:
                if len(flight_arrival)==0:
                    for i in range(len(flight_departure)):
                        self.frame_flight = customtkinter.CTkFrame(self.frame_booking,width=1180,height=80,corner_radius=0,border_width=4, border_color="#968080",fg_color="white")
                        self.frame_flight.grid(row=i,padx=10, pady=10)
                        self.book=customtkinter.CTkButton(self.frame_flight, text="Book for "+str(flight_departure[i][8])+" £/pp",width=200,height=60,corner_radius=0,fg_color="red",font=("cursive",20 ),border_width=1,command=lambda:self.booking())
                        self.book.place(relx=0.903, rely=0.5, anchor=tkinter.CENTER)      
                        self.frame_info_flight = customtkinter.CTkFrame(self.frame_flight,width=950,height=60,corner_radius=0,border_width=2, border_color="#968080",fg_color="white")
                        self.frame_info_flight.place(relx=0.41, rely=0.5, anchor=tkinter.CENTER)
                        self.info_flight = customtkinter.CTkLabel(self.frame_info_flight, text=flight_departure[i][2]+" to "+flight_departure[i][3]+" take off time the "+str(flight_departure[i][4])+" at "+str(flight_departure[i][6])[:-3]+" flight time "+str(flight_departure[i][5]), text_color="black",font=("cursive",25 ),fg_color="transparent")
                        self.info_flight.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
                else:
                    for i in range(len(flight_arrival)):
                        self.frame_flight = customtkinter.CTkFrame(self.frame_booking,width=1180,height=80,corner_radius=0,border_width=4, border_color="#968080",fg_color="white")
                        self.frame_flight.grid(row=i,padx=10, pady=10)
                        self.book=customtkinter.CTkButton(self.frame_flight, text="Book for "+str(flight_arrival[i][8])+" £/pp",width=200,height=60,corner_radius=0,fg_color="red",font=("cursive",20 ),border_width=1,command=lambda:self.booking())
                        self.book.place(relx=0.903, rely=0.5, anchor=tkinter.CENTER) 
                        self.frame_info_flight = customtkinter.CTkFrame(self.frame_flight,width=950,height=60,corner_radius=0,border_width=2, border_color="#968080",fg_color="white")
                        self.frame_info_flight.place(relx=0.41, rely=0.5, anchor=tkinter.CENTER)
                        self.info_flight = customtkinter.CTkLabel(self.frame_info_flight, text=flight_arrival[i][2]+" to "+flight_arrival[i][3]+" take off time the "+str(flight_arrival[i][4])+" at "+str(flight_arrival[i][6])[:-3]+" flight time "+str(flight_arrival[i][5]), text_color="black",font=("cursive",25 ),fg_color="transparent")
                        self.info_flight.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
            
            else:
                if len(flight_departure)>len(flight_arrival):
                    for i in range(len(flight_arrival)):
                        self.frame_flight = customtkinter.CTkFrame(self.frame_booking,width=1180,height=80,corner_radius=0,border_width=4, border_color="#968080",fg_color="white")
                        self.frame_flight.grid(row=i,padx=10, pady=10)
                        self.book=customtkinter.CTkButton(self.frame_flight, text="Book for "+str(flight_arrival[i][8]+flight_departure[i][8])+" £/pp",width=200,height=60,corner_radius=0,fg_color="red",font=("cursive",20 ),border_width=1,command=lambda:self.booking())
                        self.book.place(relx=0.903, rely=0.5, anchor=tkinter.CENTER) 
                        self.frame_info_flight = customtkinter.CTkFrame(self.frame_flight,width=950,height=60,corner_radius=0,border_width=2, border_color="#968080",fg_color="white")
                        self.frame_info_flight.place(relx=0.41, rely=0.5, anchor=tkinter.CENTER)
                        self.info_flight = customtkinter.CTkLabel(self.frame_info_flight, text=flight_departure[i][2]+" to "+flight_departure[i][3]+" take off time the "+str(flight_departure[i][4])+" at "+str(flight_departure[i][6])[:-3]+" flight time "+str(flight_departure[i][5])+"\n"+flight_arrival[i][2]+" to "+flight_arrival[i][3]+" take off time the "+str(flight_arrival[i][4])+" at "+str(flight_arrival[i][6])[:-3]+" flight time "+str(flight_arrival[i][5]), text_color="black",font=("cursive",25 ),fg_color="transparent")
                        self.info_flight.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
                    for i in range(len(flight_arrival),len(flight_departure)):
                        self.frame_flight = customtkinter.CTkFrame(self.frame_booking,width=1180,height=80,corner_radius=0,border_width=4, border_color="#968080",fg_color="white")
                        self.frame_flight.grid(row=i,padx=10, pady=10)
                        self.book=customtkinter.CTkButton(self.frame_flight, text="Book for "+str(flight_departure[i][8])+" £/pp",width=200,height=60,corner_radius=0,fg_color="red",font=("cursive",20 ),border_width=1,command=lambda:self.booking())
                        self.book.place(relx=0.906, rely=0.5, anchor=tkinter.CENTER)
                        self.frame_info_flight = customtkinter.CTkFrame(self.frame_flight,width=950,height=60,corner_radius=0,border_width=2, border_color="#968080",fg_color="white")
                        self.frame_info_flight.place(relx=0.41, rely=0.5, anchor=tkinter.CENTER)
                        self.info_flight = customtkinter.CTkLabel(self.frame_info_flight, text=flight_departure[i][2]+" to "+flight_departure[i][3]+" take off time the "+str(flight_departure[i][4])+" at "+str(flight_departure[i][6])[:-3]+" flight time "+str(flight_departure[i][5]), text_color="black",font=("cursive",25 ),fg_color="transparent")
                        self.info_flight.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)  
                else:
                    for i in range(len(flight_departure)):
                        self.frame_flight = customtkinter.CTkFrame(self.frame_booking,width=1180,height=80,corner_radius=0,border_width=4, border_color="#968080",fg_color="white")
                        self.frame_flight.grid(row=i,padx=10, pady=10)
                        self.book=customtkinter.CTkButton(self.frame_flight, text="Book for "+str(flight_departure[8])+" £/pp",width=200,height=60,corner_radius=0,fg_color="red",font=("cursive",20 ),border_width=1,command=lambda:self.booking())
                        self.book.place(relx=0.906, rely=0.5, anchor=tkinter.CENTER)
                        self.frame_info_flight = customtkinter.CTkFrame(self.frame_flight,width=950,height=60,corner_radius=0,border_width=2, border_color="#968080",fg_color="white")
                        self.frame_info_flight.place(relx=0.41, rely=0.5, anchor=tkinter.CENTER)
                        self.info_flight = customtkinter.CTkLabel(self.frame_info_flight, text=flight_departure[i][2]+" to "+flight_departure[i][3]+" take off time the "+str(flight_departure[i][4])+" at "+str(flight_departure[i][6])[:-3]+" flight time "+str(flight_departure[i][5])+"\n"+flight_arrival[i][2]+" to "+flight_arrival[i][3]+" take off time the "+str(flight_arrival[i][4])+" at "+str(flight_arrival[i][6])[:-3]+" flight time "+str(flight_arrival[i][5]), text_color="black",font=("cursive",25 ),fg_color="transparent")
                        self.info_flight.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
                    for i in range(len(flight_departure),len(flight_arrival)):
                        self.frame_flight = customtkinter.CTkFrame(self.frame_booking,width=1180,height=80,corner_radius=0,border_width=4, border_color="#968080",fg_color="white")
                        self.frame_flight.grid(row=i,padx=10, pady=10)
                        self.book=customtkinter.CTkButton(self.frame_flight, text="Book for "+str(flight_departure[8])+" £/pp",width=200,height=25,corner_radius=0,fg_color="red",font=("cursive",20 ),border_width=1,command=lambda:self.booking())
                        self.book.place(relx=0.906, rely=0.5, anchor=tkinter.CENTER)
                        self.frame_info_flight = customtkinter.CTkFrame(self.frame_flight,width=950,height=60,corner_radius=0,border_width=2, border_color="#968080",fg_color="white")
                        self.frame_info_flight.place(relx=0.41, rely=0.5, anchor=tkinter.CENTER)
                        self.info_flight = customtkinter.CTkLabel(self.frame_info_flight, text=flight_arrival[i][2]+" to "+flight_arrival[i][3]+" take off time the "+str(flight_arrival[i][4])+" at "+str(flight_arrival[i][6])[:-3]+" flight time "+flight_arrival[i][5], text_color="black",font=("cursive",25 ),fg_color="transparent")
                        self.info_flight.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)        
        return
    
    def booking(self):
        "Payment"
        return
    

class CreateAccountGui:

    def __init__(self, app):
        
        self.app =app

        self.frame=customtkinter.CTkFrame(master=self.app, width=500, height=500,border_color="#77B5FE",fg_color="white")
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

        self.create=customtkinter.CTkButton(self.frame, text="Creat an account",width=120,fg_color="red",command=lambda:self.create_account())
        self.create.place(relx=0.32, rely=0.9, anchor=tkinter.CENTER)

        self.loogin=customtkinter.CTkButton(self.frame, text="Log in",width=120,fg_color="green",command=lambda:self.loogin())
        self.loogin.place(relx=0.64, rely=0.9, anchor=tkinter.CENTER)

    def create_account(self):

        name = self.name.get()
        email = self.email.get()
        password = self.password.get()
        age = self.age.get()
        adress = self.adress.get()
        permission = 0

        cur.execute(f"SELECT * FROM member WHERE email='{email}'")

        if cur.rowcount > 0:
            messagebox.showerror("Error", "User already exists!")
            return

        cur.execute(f"INSERT INTO member (name, email, password, age, adress, permission) VALUES ('{name}', '{email}', '{password}', '{age}', '{adress}', '{permission}')")
        conn.commit()
        messagebox.showinfo("Success", "Account created successfully!")
        conn.close()

        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        bookingapp(self.app)

    def loogin(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        login_gui(self.app)

class AdminGUI:
    def __init__(self, app):
        
                
def main():
    app = tkinter.Tk()
    app1 = login_gui(app)
    app.mainloop()
    
if __name__ == "__main__":
    main()