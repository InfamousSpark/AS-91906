import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv

#Creating window
app = tk.Tk()
app.title("MRGS Tuckshop")
app.iconbitmap('fastfoodicon.ico')
app.geometry('500x600')

#Some header within class?
class Header():
    def __init__(self, master):

        self.canvas = tk.Canvas(app, width=150, height=150)
        self.img = tk.PhotoImage(file="tuckshop.PNG")
        
        self.imgArea = self.canvas.create_image(0, 0, anchor=tk.NW, image = self.img)
        self.canvas.grid(row=0, column=0, pady=(20,0))
        

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

#Intro text
intro_lbl = tk.Label(app, text="Welcome to the MRGS\ndigital tuckshop menu", font='Helvetica 10 bold')
intro_lbl.grid(row=0, column=1, columnspan=2)

#Name entry
name_entry = tk.Entry(app, width=29)
name_entry.insert(0, "Enter your student ID")
name_entry.grid(row=1,column=1, columnspan=2, pady=10)

#Combo box 
comb=tk.StringVar()
comboExample = ttk.Combobox(app, textvariable=comb , values=ilist, width=30)
comboExample.grid(row=2,column=0)
comboExample.set("Choose your item")

#Quantity entry
quan = tk.StringVar(value=1)
customer_entry = tk.Entry(app,textvariable=quan, width=10)
customer_entry.grid(row=2, column=1, pady=10, padx=10)

###Add item
#Defining add item function
def add_item():
    global total
    item = comb.get()
    
    try:#Checking if letters were entered
        qu = int(quan.get())
        pass
    except ValueError:
        messagebox.showerror("Woops!", "Please enter a correct quantity and try again.")

    if qu <= 0:#Checking if boundary or negative numbers were entered
        messagebox.showerror("Woops!", "Please enter a correct quantity and try again.")
        raise
    
    try:#Checking if an item is selected in combo box
        itemprice = float((imenu[item]))#istring value comes from dictionary
        pass
    except KeyError:
        messagebox.showerror("Woops!", "Please select an item to order and try again")
        
    tup = (item,qu,"${}".format(itemprice*qu))
    total += itemprice * qu
    tree.insert("", tk.END, values=tup)
    ltotal.set("${}".format(str(total)))
#Add item button
add_btn = tk.Button(app, text="Add item", width=12, command=add_item)
add_btn.grid(row=2, column=2, pady=10, padx=10)
##print(dict(comboExample))

###Clear items
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
clear_btn = tk.Button(app, text="Clear items", width=10, command=lambda: clear(label2))
clear_btn.grid(row=3, column=0, sticky="w", padx=10, pady=10)

#Ordered items treeview
tree = ttk.Treeview(app, column=("column1", "column2", "column3"), show='headings')
tree.heading("#1", text="ITEM")#Naming
tree.heading("#2", text="QTY")#Naming
tree.heading("#3", text="PRICE")#Naming
tree.grid(row=4, column=0, rowspan=3, padx=(10,0))
tree.column("#2",minwidth=40,width=40)#Formating column
tree.column("#3",minwidth=40,width=40)#Formating column


#Total bill label
label1 = tk.Label(app, text = "Total Bill:",font='Helvetica 18 bold')
label1.grid(column=1, row=4, columnspan=2)

#Total cost label
total = 0
ltotal = tk.StringVar()
ltotal.set("No items\nordered")
label2 = tk.Label(app,font='Helvetica 18 bold',textvariable=ltotal)
label2.grid(column=1, row=5, columnspan=2)
##print(comboExample.current(), comboExample.get())

###Confirm order
#Defining confirm order function
def confirm(name_entry):
    global total
    if total == 0:
        messagebox.showwarning("Woops!", "Looks like you haven't ordered anything!\nPlease select an item to order and try again.")
    elif name_entry.get() == "Enter your student ID":
        messagebox.showwarning("Woops!", "Looks like you haven't entered your student ID!\nPlease enter your student ID and try again.")
    else:
        try:
            int(name_entry.get())
            pass
        except:
            messagebox.showerror("Woops!", "Please enter a correct student ID and try again.")
            raise

        conf_opt = messagebox.askyesno("Confirming order", "Would you like to confirm your order?")
        if conf_opt == 1:
            messagebox.showinfo("MRGS Tuckshop", "Your order has been sent to the tuck shop.\nThanks for using this digital menu!")
            #Appending onto orders csv
            with open('orders.csv', mode='a') as outfile:
                writer = csv.writer(outfile)
                writer.writerow([name_entry.get(), "${}".format(total)])
                for line in tree.get_children():
                    itemw = tree.item(line)['values'][0]
                    pricew = tree.item(line)['values'][1]
                    writer.writerow([itemw, pricew])
                    #Resetting treeview
                    tree.delete(line)
                total = 0
                ltotal.set("No items\nordered")
                label2.config(textvariable=ltotal)
                comboExample.set("Choose your item")
                name_entry.delete(0, tk.END)
                name_entry.insert(0, "Enter your student ID")
                    
        elif conf_opt == 0:
            pass

confirm_btn = tk.Button(app, text="Confirm order", width=12, command=lambda: confirm(name_entry))
confirm_btn.grid(column=1, row=6, columnspan=2)


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
    #Exit button
    exitbutton = tk.Button(top, text="Exit Price List", command=top.destroy)
    exitbutton.pack(pady=10)
#Price list button
pricelistbutton = tk.Button(app, text="Open price list", width=15, command=openpricelist)
pricelistbutton.grid(column=0, row=7, pady=20)

#Running
##gui = Header(app)
h=Header(app)
app.mainloop()
