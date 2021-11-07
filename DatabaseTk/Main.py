from tkinter import *
from PIL import Image, ImageTk
import sqlite3


root = Tk()
root.geometry("400x600")

#create a database or conect to one
conn = sqlite3.connect("addres_book.db")

#create cursor
c = conn.cursor()

#create table
'''
c.execute("""CREATE TABLE addresses (
    first_name text, 
    last_name text,
    adress text, 
    city text,
    state text,
    zipcode integer
    )
        """)
'''
#create function to delete record
def deleteRecord():
    conn = sqlite3.connect("addres_book.db")
    c = conn.cursor()

    #delete a record
    c.execute("DELETE FROM addresses WHERE oid = "+select_box.get())

    conn.commit()
    conn.close()


def update():
    conn = sqlite3.connect("addres_book.db")
    c = conn.cursor()

    record_id = select_box.get()

    c.execute("""UPDATE addresses SET
            first_name = :first,
            last_name = :last,
            adress = :address,
            city = :city,
            state = :state,
            zipcode = :zipcode
            
            WHERE oid = :oid""",
              {
                  "first": f_name_editor.get(),
                  "last" : l_name_editor.get(),
                  "address": adress_editor.get(),
                  "city": city_editor.get(),
                  "state": state_editor.get(),
                  "zipcode": zipcode_editor.get(),

                  "oid": record_id
              }
              )




    conn.commit()
    conn.close()

    editor.destroy()


def editRecord():
    global editor
    editor = Tk()
    editor.title("Edit A Record")
    editor.geometry("400x400")

    record_id = select_box.get()
    conn = sqlite3.connect("addres_book.db")
    c = conn.cursor()

    # query the data bas
    c.execute("SELECT * FROM addresses WHERE oid = "+record_id)
    records = c.fetchall()


    global f_name_editor
    global l_name_editor
    global adress_editor
    global city_editor
    global state_editor
    global zipcode_editor


    #creates Entery for information
    f_name_editor = Entry(editor, width=30)
    f_name_editor.grid(row=0, column=1, padx=20)
    l_name_editor = Entry(editor, width=30)
    l_name_editor.grid(row=1, column=1)
    adress_editor = Entry(editor, width=30)
    adress_editor.grid(row=2, column=1)
    city_editor = Entry(editor, width=30)
    city_editor.grid(row=3, column=1)
    state_editor = Entry(editor, width=30)
    state_editor.grid(row=4, column=1)
    zipcode_editor = Entry(editor, width=30)
    zipcode_editor.grid(row=5, column=1)

    # create text labels
    f_name_label_editor = Label(editor, text="First Name")
    f_name_label_editor.grid(row=0, column=0)
    l_name_label_editor = Label(editor, text="Last Name")
    l_name_label_editor.grid(row=1, column=0)
    adress_label_editor = Label(editor, text="Adress")
    adress_label_editor.grid(row=2, column=0)
    city_label_editor = Label(editor, text="City")
    city_label_editor.grid(row=3, column=0)
    state_label_editor = Label(editor, text="State")
    state_label_editor.grid(row=4, column=0)
    zipcode_label_editor = Label(editor, text="Zipcode")
    zipcode_label_editor.grid(row=5, column=0)

    save_btn_editor = Button(editor, text = "Save Record", command = update)
    save_btn_editor.grid(row = 6, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 144)

    for record in records:
        f_name_editor.insert(0, record[0])
        l_name_editor.insert(0, record[1])
        adress_editor.insert(0, record[2])
        city_editor.insert(0, record[3])
        state_editor.insert(0, record[4])
        zipcode_editor.insert(0, record[5])

    conn.commit()
    conn.close()



#create submbit function for data base
def submit():

    conn = sqlite3.connect("addres_book.db")
    c = conn.cursor()

    #insert into table
    c.execute("INSERT INTO addresses VALUES (:f_name, :l_name, :address, :city, :state, :zipcode)",
              {
                  "f_name": f_name.get(),
                  "l_name": l_name.get(),
                  "address": adress.get(),
                  "city": city.get(),
                  "state": state.get(),
                  "zipcode": zipcode.get()
              }
              )

    conn.commit()

    conn.close()

    # clear text boxes
    f_name.delete(0, END)
    l_name.delete(0, END)
    adress.delete(0, END)
    city.delete(0, END)
    state.delete(0, END)
    zipcode.delete(0, END)

def query():
    conn = sqlite3.connect("addres_book.db")
    c = conn.cursor()

    #query the data base
    c.execute("SELECT *, oid FROM addresses")
    records = c.fetchall()

    print_records = ""
    for record in records:
        print_records += str(record) + "\n"

    query_label = Label(root, text = print_records)
    query_label.grid(row = 12, column =0, columnspan = 2 )

    conn.commit()
    conn.close()

#create text boxes
f_name = Entry(root, width = 30)
f_name.grid(row = 0, column = 1, padx = 20 )
l_name = Entry(root, width = 30)
l_name.grid(row = 1, column = 1 )
adress = Entry(root, width = 30)
adress.grid(row = 2, column = 1 )
city = Entry(root, width = 30)
city.grid(row = 3, column = 1 )
state = Entry(root, width = 30)
state.grid(row = 4, column = 1 )
zipcode = Entry(root, width = 30)
zipcode.grid(row = 5, column = 1 )

select_box = Entry(root, width = 30)
select_box.grid(row = 9, column = 1)

#create text labels
f_name_label = Label(root, text = "First Name")
f_name_label.grid(row = 0, column = 0)
l_name_label = Label(root, text = "Last Name")
l_name_label.grid(row = 1, column = 0)
adress_label = Label(root, text = "Adress")
adress_label.grid(row = 2, column = 0)
city_label = Label(root, text = "City")
city_label.grid(row = 3, column = 0)
state_label = Label(root, text = "State")
state_label.grid(row = 4, column = 0)
zipcode_label = Label(root, text = "Zipcode")
zipcode_label.grid(row = 5, column = 0)

select_box_label = Label(root, text = "Select ID")
select_box_label.grid(row = 9, column = 0)

#create submit button

submit_btn = Button(root, text = "Add record to database", command = submit)
submit_btn.grid(row=6, column = 0, columnspan=2, pady=10, padx = 10, ipadx = 100)


#Create a query button
query_btn = Button(root, text = "Show Records", command = query)
query_btn.grid(row = 7, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 137)

#create delete record button
delete_btn = Button(root, text = "Delete Record", command = deleteRecord)
delete_btn.grid(row = 10, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 134)

edit_btn = Button(root, text = "Edit Record", command = editRecord)
edit_btn.grid(row = 11, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx = 145)


conn.commit()


conn.close()


root.mainloop()
