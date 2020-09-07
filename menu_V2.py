#MRGS Tuckshop menu V1 Created by Kenny Yu
#Importing modules from Python Libraries
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import *
#pip install tkcalendar
#Importing CSV file created by me
import csv

#Creating GUI window
app = tk.Tk()
app.title("MRGS Tuckshop")
app.iconbitmap('fastfoodicon.ico')
app.geometry('500x620')

#Tuckshop logo
class Header():
    def __init__(self, master):

        self.canvas = tk.Canvas(app, width=201, height=134)
        self.img = tk.PhotoImage(file="tuckshop.PNG")
        
        self.imgArea = self.canvas.create_image(0, 0, anchor=tk.NW, image = self.img)
        self.canvas.grid(row=0, column=0, rowspan=2, pady=(20,0))
        

#Importing list from excel
imenu={}#dictionary of item menu
ilist=[]#list of item list
plist=[]#list of prices
with open('lunch_menu.csv', mode='r') as infile:
    reader = csv.reader(infile)
    imenu = {rows[0]:rows[1] for rows in reader}
    
#Getting list items    
for k in imenu.keys():
    ilist.append(k)
for k in imenu.values():
    plist.append(k)

#School logo
school_canvas = tk.Canvas(app, width=99, height=85)
school_logo = tk.PhotoImage(file="school_logo.PNG")
        
school_imgArea = school_canvas.create_image(0, 0, anchor=tk.NW, image = school_logo)

#Intro text
intro_lbl = tk.Label(app, text="Welcome to the MRGS\ndigital tuckshop menu", font='Helvetica 10 bold', fg="#0f3676")

#Date picker
#Defining open datepicker function
def opendatepick():
    datepick = tk.Toplevel()
    datepick.title("Date picker")
    datepick.iconbitmap('fastfoodicon.ico')
    datepick.geometry('300x280')

    cal = Calendar(datepick, selectmode="day", date_pattern='dd/mm/y', year=2020, month=9)
    cal.pack(pady=20)
    
    def grab_date():
        global date
        date = cal.get_date()
        date_lbl.config(text=date)
        datepick.destroy()
        
    #Creating pick date button
    getdate = tk.Button(datepick, text="Pick date", width=15, command=grab_date, bg="#0f3676", fg="white")
    getdate.pack(pady=10)

#Creating open pick date window button
date = ""
pickdate = tk.Button(app, text="Pick order date", width=15, command=opendatepick, bg="#0f3676", fg="white")

#Name entry
name_entry = tk.Entry(app, width=19)
name_entry.insert(0, "Enter your student ID")

###Confirm student ID button
#Defining confirm student ID function
def confstud():
    if name_entry.get() == "Enter your student ID":
        messagebox.showwarning("Woops!", "Looks like you haven't entered your student ID!\nPlease enter your student ID and try again.")
    else:
        try:
            int(name_entry.get())
            confirm_btn["state"] = "normal"
            pass
        except:
            messagebox.showerror("Woops!", "Please enter a correct student ID and try again.")
            raise

        studentid.set(str(name_entry.get()))
#Creating confirm student ID button
stud = tk.Button(app, text="Confirm", command=confstud, bg="#0f3676", fg="white", width=8)

#Combo box 
comb=tk.StringVar()
comboExample = ttk.Combobox(app, textvariable=comb , values=ilist, width=30)
comboExample.set("Choose your item")

#Quantity entry
quan = tk.StringVar(value=1)
customer_entry = tk.Entry(app,textvariable=quan, width=10)

###Add item button
#Defining add item function
def add_item():
    global total
    item = comb.get()
    
    try:#Checking if letters were entered
        qu = int(quan.get())
        pass
    except ValueError:
        messagebox.showerror("Woops!", "Please enter a numeral quantity and try again.")

    if qu <= 0:#Checking if boundary or negative numbers were entered
        messagebox.showerror("Woops!", "Please enter a positive numeral and try again.")
        raise
    
    try:#Checking if an item is selected in combo box
        itemprice = float((imenu[item]))#istring value comes from dictionary
        pass
    except KeyError:
        messagebox.showerror("Woops!", "Please select an item to order and try again")
        
    tup = (item,qu,"${}".format(itemprice*qu))
    total += itemprice * qu
    tree.insert("", tk.END, values=tup)
    ltotal.set("${}".format(str(1.15*total)))
#Add item button
add_btn = tk.Button(app, text="Add item", width=8, command=add_item, bg="#0f3676", fg="white")
##print(dict(comboExample))

###Clear items button
#Defining clear button function
def clear(label2):
    #Resetting treeview
    for i in tree.get_children():
        tree.delete(i)
    global total
    total = 0
    ltotal.set("No items\nordered")
    label2.config(textvariable=ltotal)
#Clear item button
clear_btn = tk.Button(app, text="Clear items", width=10, command=lambda: clear(label2), bg="#0f3676", fg="white")

#Ordered items treeview
tree = ttk.Treeview(app, column=("column1", "column2", "column3"), show='headings', height=12)
tree.heading("#1", text="ITEM")#Naming
tree.heading("#2", text="QTY")#Naming
tree.heading("#3", text="PRICE")#Naming
tree.column("#2",minwidth=40,width=40)#Formating column
tree.column("#3",minwidth=40,width=40)#Formating column

#Order date label
date_lbl = tk.Label(app, text="", font='Helvetica 18 bold', fg="#0f3676")

#Student ID label
studentid = tk.StringVar()
studentid.set("")
stud_lbl = tk.Label(app, textvariable=studentid, font='Helvetica 18 bold', fg="#0f3676")

#Total bill label
label1 = tk.Label(app, text = "Total Bill:",font='Helvetica 18 bold', fg="#0f3676")

#Total cost label
total = 0
ltotal = tk.StringVar()
ltotal.set("No items\nordered")
label2 = tk.Label(app,font='Helvetica 18 bold',textvariable=ltotal, fg="#0f3676")
##print(comboExample.current(), comboExample.get())

###Confirm order button
#Defining confirm order function
def confirm(name_entry):
    global total
    global date
    if date == "":
        messagebox.showwarning("Woops", "Please select an order date")
        raise
    else:
        pass
    if total == 0:
        messagebox.showwarning("Woops!", "Looks like you haven't ordered anything!\nPlease select an item to order and try again.")
    else:
        conf_opt = messagebox.askyesno("Confirming order", "Would you like to confirm your order?")
        if conf_opt == 1:
            messagebox.showinfo("MRGS Tuckshop", "Your order has been sent to the tuck shop.\nThanks for using this digital menu!")
            #Appending onto orders csv
            with open('orders.csv', mode='a') as outfile:
                writer = csv.writer(outfile)
                writer.writerow([date, name_entry.get(), "${}".format(1.15*total)])
                for line in tree.get_children():
                    itemw = tree.item(line)['values'][0]
                    pricew = tree.item(line)['values'][1]
                    writer.writerow([itemw, pricew])
                #Resetting treeview
                    tree.delete(line)
                total = 0
                date = ""
                date_lbl.config(text=date)
                ltotal.set("No items\nordered")
                label2.config(textvariable=ltotal)
                comboExample.set("Choose your item")
                name_entry.delete(0, tk.END)
                name_entry.insert(0, "Enter your student ID")
                studentid.set("")
                confirm_btn["state"] = "disabled"
                    
        elif conf_opt == 0:
            pass
#Creating confirm item button
confirm_btn = tk.Button(app, text="Confirm order", width=12, state=tk.DISABLED, command=lambda: confirm(name_entry), bg="#0f3676", fg="white")


###Price list window
def openpricelist():
    top = tk.Toplevel()
    top.title("Price list")
    top.iconbitmap('fastfoodicon.ico')
    top.geometry('350x550')
    #Price list treeview
    items = ttk.Treeview(top, column=("column1", "column2"), show='headings', height=len(ilist))
    items.heading("#1", text="Item name")
    items.heading("#2", text="Item price")
    items.pack(pady=10)
    items.column("#1", minwidth=40, width=200)
    items.column("#2", minwidth=40, width=100)

    for i in range(len(ilist)):
        menu=(ilist[i], "${}".format(plist[i]))
        items.insert("", tk.END, values=menu)
    #Creatng Exit button
    exitbutton = tk.Button(top, text="Exit Price List", command=top.destroy, bg="#0f3676", fg="white")
    exitbutton.pack(pady=10)
#Price list button
pricelistbutton = tk.Button(app, text="Open price list", width=15, command=openpricelist, bg="#0f3676", fg="white")


#Positioning items in window
school_canvas.grid(row=0, column=1, columnspan=2, sticky="s")
intro_lbl.grid(row=1, column=1, columnspan=2, sticky="n")

name_entry.grid(row=2, column=1, pady=(10,0))
stud.grid(row=2, column=2, pady=(10,0))
comboExample.grid(row=3,column=0)
customer_entry.grid(row=3, column=1, pady=10, sticky="w")
add_btn.grid(row=3, column=2, pady=10, padx=10)
pickdate.grid(row=4 ,column=1 ,columnspan=2 ,pady=10)

clear_btn.grid(row=4, column=0, sticky="w", padx=10, pady=10)
tree.grid(row=5, column=0, rowspan=5, padx=(10,0))

date_lbl.grid(column=1, row=5, columnspan=2)
stud_lbl.grid(column=1, row=6, columnspan=2)
label1.grid(column=1, row=7, columnspan=2)
label2.grid(column=1, row=8, columnspan=2)
confirm_btn.grid(column=1, row=9, columnspan=2)

pricelistbutton.grid(column=0, row=10, pady=20)


#Running
##gui = Header(app)
h=Header(app)
app.mainloop()
