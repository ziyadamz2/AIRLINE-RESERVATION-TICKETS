import tkinter as tk
import customtkinter
class MaFenetre(tk.Tk):
    def __init__(self,app):

        self.app=app
        self.entry_var = customtkinter.StringVar()

        self.entry = customtkinter.CTkEntry(self.app, textvariable=self.entry_var)
        self.entry.pack()

        self.bouton = customtkinter.CTkButton(self.app, text="Afficher le contenu", command=lambda: self.afficher_contenu())
        self.bouton.pack()

    def afficher_contenu(self):
        contenu = self.entry_var.get()
        print(contenu)

if __name__ == "__main__":
    app = customtkinter.CTk()
    
    app.mainloop()
    
