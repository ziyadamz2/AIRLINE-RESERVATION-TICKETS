from customtkinter import *
import customtkinter
from tkinter import * 
from PIL import ImageTk, Image
import tkinter
customtkinter.set_appearance_mode("light")

app = tkinter.Tk()
app.title('AIRLINE RESERVATION TICKET')
app.state('zoomed')

background = ImageTk.PhotoImage(Image.open("background.png"))
l1 = customtkinter.CTkLabel(master=app,image=background)
l1.pack(fill='both', expand=True)


frame=customtkinter.CTkFrame(master=l1, width=500, height=400,corner_radius=5,border_width=3,border_color="#77B5FE",fg_color="white")
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

msg=customtkinter.CTkLabel(master=frame, text="Airline Reservation Ticket",compound="top",font=("Apple Chancery, cursive",30 ),text_color="blue")
msg.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

email = customtkinter.CTkEntry(app, placeholder_text="Email",width=250, height=35,font=("cursive",15 ),border_color="#859BF5",border_width=3)
email.place(relx=0.5, rely=0.39, anchor=tkinter.CENTER)

passworld = customtkinter.CTkEntry(app, placeholder_text="Passworld",width=250, height=35,font=("cursive",17 ),border_color="#859BF5",border_width=3)
passworld.place(relx=0.5, rely=0.47, anchor=tkinter.CENTER)

login=customtkinter.CTkButton(app, text="Login",width=120,fg_color="green")
login.place(relx=0.458, rely=0.55, anchor=tkinter.CENTER)

creat_an_account=customtkinter.CTkButton(app, text="Creat an account",width=120,fg_color="red")
creat_an_account.place(relx=0.543, rely=0.55, anchor=tkinter.CENTER)

login_as_guest=customtkinter.CTkButton(app, text="Login as a guest")
login_as_guest.place(relx=0.5, rely=0.61, anchor=tkinter.CENTER)
app.mainloop()
