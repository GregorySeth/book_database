from tkinter import *
from back import Database
from tkinter import messagebox

class MainWindow(object):

    def __init__(self, window):

        #Window
        self.window = window
        self.window.title("Book database")
        self.window.geometry("500x370")

        #Labels
        lbl_title = Label(self.window, text="Tytuł: ")
        lbl_title.grid(column=0, row=0)
        lbl_author = Label(self.window, text="Autor: ")
        lbl_author.grid(column=2, row=0)
        lbl_year = Label(self.window, text="Rok: ")
        lbl_year.grid(column=0, row=1)
        lbl_isbn = Label(self.window, text="ISBN: ")
        lbl_isbn.grid(column=2, row=1)
        lbl_info = Label(self.window, text="ID   |   Tytuł   |   Autor   |   Rok   |   ISBN")
        lbl_info.grid(column=0, columnspan=3, row=2)

        #Entries
        self.en_title_var = StringVar()
        self.en_title = Entry(self.window, textvariable=self.en_title_var)
        self.en_title.grid(column=1, row=0)
        self.en_author_var = StringVar()
        self.en_author = Entry(self.window, textvariable=self.en_author_var)
        self.en_author.grid(column=3, row=0)
        self.en_year_var = StringVar()
        self.en_year = Entry(self.window, textvariable=self.en_year_var)
        self.en_year.grid(column=1, row=1)
        self.en_isbn_var = StringVar()
        self.en_isbn = Entry(self.window, textvariable=self.en_isbn_var)
        self.en_isbn.grid(column=3, row=1)

        #Listbox
        self.lbx1 = Listbox(self.window, height=12, width=50)
        self.lbx1.grid(column=0, row=3, columnspan=2, rowspan=4, padx=10)
        self.lbx1.bind("<<ListboxSelect>>", self.show_selected)

        #Scrollbars
        scr1 = Scrollbar(self.window)
        scr1.grid(column=2, row=3, rowspan=4, sticky="ns")
        scr2 = Scrollbar(self.window, orient="horizontal")
        scr2.grid(column=0, row=7, columnspan=2, padx=10, sticky="we")
        #Scrollbars commands
        self.lbx1.configure(yscrollcommand = scr1.set, xscrollcommand= scr2.set)
        scr1.configure(command = self.lbx1.yview)
        scr2.configure(command = self.lbx1.xview)

        #Buttons
        bt1 = Button(self.window, text="Pokaż wszystko", width=15, height=2, command=self.view_option)
        bt1.grid(column=3, row=2)
        bt2 = Button(self.window, text="Wyszukaj wpis", width=15, height=2, command=self.find_option)
        bt2.grid(column=3, row=3)
        bt3 = Button(self.window, text="Dodaj wpis", width=15, height=2, command=self.add_option)
        bt3.grid(column=3, row=4)
        bt4 = Button(self.window, text="Edytuj wpis", width=15, height=2, command=self.edit_option)
        bt4.grid(column=3, row=5)
        bt5 = Button(self.window, text="Usuń wpis", width=15, height=2, command=self.delete_option)
        bt5.grid(column=3, row=6)
        bt6 = Button(self.window, text="Zamknij", width=15, height=2, command=window.destroy)
        bt6.grid(column=3, row=7)

        #Listbox showing data on start
        self.view_option()

    #Window functions
    def show_selected(self, event): #shows details of the selected item in entry fields
        try:
            global selection
            index = self.lbx1.curselection()[0]
            self.selection = self.lbx1.get(index)
            self.en_title.delete(0,END)
            self.en_author.delete(0,END)
            self.en_year.delete(0,END)
            self.en_isbn.delete(0,END)
            self.en_title.insert(END, self.selection[1])
            self.en_author.insert(END, self.selection[2])
            self.en_year.insert(END, self.selection[3])
            self.en_isbn.insert(END, self.selection[4])
        except IndexError:
            pass

    def view_option(self): #show all items rom database
        self.lbx1.delete(0,END)
        for i in database.view():
            self.lbx1.insert(END, i)

    def find_option(self): #find item in database
        self.lbx1.delete(0,END)
        for i in database.find(self.en_title_var.get(), self.en_author_var.get(), self.en_year_var.get(), self.en_isbn_var.get()):
            self.lbx1.insert(END, i)

    def add_option(self): #add new item to database
        database.add(self.en_title_var.get(), self.en_author_var.get(), self.en_year_var.get(), self.en_isbn_var.get())
        self.view_option()
        messagebox.showinfo("Dodano", "Dodano - Tytuł: %s, Autor: %s, Rok: %s, ISBN: %s" %(self.en_title_var.get(), self.en_author_var.get(), self.en_year_var.get(), self.en_isbn_var.get()))

    def delete_option(self): #delete selected item from database
        database.delete(self.selection[0])
        self.view_option()
        messagebox.showinfo("Usunięto", "Usunięto - %s, %s, %s, %s" %(self.selection[1], self.selection[2], self.selection[3], self.selection[4]))

    def edit_option(self): #edit selected item by changing its values with the new values from entries
        database.edit(self.selection[0], self.en_title_var.get(), self.en_author_var.get(), self.en_year_var.get(), self.en_isbn_var.get())
        self.view_option()
        messagebox.showinfo("Zrobione", "Gotowe")

database = Database("book_base.db")
window = Tk()
MainWindow(window)
window.mainloop()
