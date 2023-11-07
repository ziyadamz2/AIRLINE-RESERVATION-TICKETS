import tkinter as tk
from tkinter import ttk
from tkinter import *
from ttkthemes import ThemedStyle

class menu:
    def __init__(self):
        self.fenetre = tk.Tk()
        self.fenetre.title('AIRLINE RESERVATION TICKET')
        self.style = ThemedStyle(self.fenetre)
        self.fenetre.state('zoomed')
        self.bg = PhotoImage(file="background.png")

        self.background = tk.Label(self.fenetre, image=self.bg)
        self.background.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.fenetre.mainloop()
    
def main():
    menu()

if __name__ == "__main__":
    main()