from customtkinter import *
import customtkinter
from tkinter import * 
from PIL import ImageTk
from PIL import Image
import tkinter
customtkinter.set_appearance_mode("light")


class menu():
    def __init__(self):
        self.app = tkinter.Tk()
        self.app.title('AIRLINE RESERVATION TICKET')
        self.app.state('zoomed')
        


        self.background = ImageTk.PhotoImage(Image.open("background.png"))
        self.l1 = customtkinter.CTkLabel(master=self.app,image=self.background)
        self.l1.pack(fill='both', expand=True)


        self.frame=customtkinter.CTkFrame(master=self.l1, width=500, height=400,corner_radius=5,border_width=3,border_color="#77B5FE",fg_color="white")
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.msg=customtkinter.CTkLabel(master=self.frame, text="Airline Reservation Ticket",compound="top",font=("Apple Chancery, cursive",30 ),text_color="blue")
        self.msg.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

        self.email = customtkinter.CTkEntry(self.app, placeholder_text="Email",width=250, height=35,font=("cursive",15 ),border_color="#859BF5",border_width=3)
        self.email.place(relx=0.5, rely=0.39, anchor=tkinter.CENTER)

        self.passworld = customtkinter.CTkEntry(self.app, placeholder_text="Passworld",width=250, height=35,font=("cursive",17 ),border_color="#859BF5",border_width=3)
        self.passworld.place(relx=0.5, rely=0.47, anchor=tkinter.CENTER)

        self.login=customtkinter.CTkButton(self.app, text="Login",width=120,fg_color="green")
        self.login.place(relx=0.458, rely=0.55, anchor=tkinter.CENTER)

        self.creat_an_account=customtkinter.CTkButton(self.app, text="Creat an account",width=120,fg_color="red")
        self.creat_an_account.place(relx=0.543, rely=0.55, anchor=tkinter.CENTER)

        self.login_as_guest=customtkinter.CTkButton(self.app, text="Login as a guest")
        self.login_as_guest.place(relx=0.5, rely=0.61, anchor=tkinter.CENTER)
        self.app.mainloop()


if __name__ == "__main__":
    menu()