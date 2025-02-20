#This project will serve as a database for local SMMEs and potential client/client information for Techmerce.
#It will use tkInter for GUI and will initially use a simple local SQL database, then we will move towards firebase
#for cloud services.

import sqlite3
import tkinter as tk
from msilib import type_key
from tkinter import messagebox
from tkinter import ttk


#import required modules for firebase functionality
import firebase_admin
import requests
from firebase_admin import db, credentials,firestore



cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred, {"databaseURL":"https://tm-client-database-default-rtdb.europe-west1.firebasedatabase.app/"})
database = firestore.client()


#creating reference to root node - cursor
ref = db.reference("/")

#test code, remove later
print(ref.get())


#Setting up the Database
def init_db():
    conn = sqlite3.connect("clients.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS clients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT,
                        phone TEXT,
                        job TEXT)''')

    conn.commit()
    conn.close()

#Add Client
def add_client():
    client_data = {}
    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    job = job_entry.get()

    conn = sqlite3.connect("clients.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clients (name, email, phone, job) VALUES (?, ?, ?, ?)", (name, email, phone, job))
    conn.commit()
    messagebox.showinfo("Success", "Client Added Successfully")
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    job_entry.delete(0, tk.END)

    client_data = {
        'name' : name,
        'email':email,
        'phone':phone,
        'job':job
    }
    populate_table()

    if is_connected():
        try:
            # database.collection('/clients').add(client_data)
            db.reference("/clients").push().set(client_data)
            print("Added to firebase!")
        except Exception as e:
            print(f"Error syncing with Firebase: {e}")

    if not name:
        messagebox.showerror("Error", "Name is required")
        return

def populate_table():
    for row in tree.get_children(): #get_children returns a list of children in the root:
        tree.delete(row)
        #we open the database connection first
    conn = sqlite3.connect("clients.db")
    cursor = conn.cursor()
    #The read all SQL command is below
    cursor.execute("SELECT * FROM clients")
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        tree.insert("", tk.END, values=row)

#Delete Client Window - obselete
def open_delete_window():
    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Client")
    delete_window.geometry("300x150")

    tk.Label(delete_window, text="Client ID to Delete: ").pack()
    id_entry = tk.Entry(delete_window)
    id_entry.pack()



    tk.Button(delete_window, text="Delete", command=delete_client).pack()

#Delete Client will now not only delete the SQL record in the local db but also the firebase record.
def delete_client():
        curItem = tree.focus()
        print(tree.item(curItem).get('values')[0])
        table_index = tree.item(curItem).get('values')[0]

        client_id = table_index
        conn = sqlite3.connect("clients.db")
        cursor = conn.cursor()


        cursor.execute("SELECT * FROM clients WHERE id=?", (client_id,))
        result = cursor.fetchone()

        if result:
            confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete Client ID {client_id}?")
            if confirm:
                # Important code below: Executes the SQL command on the database
                cursor.execute("DELETE FROM clients WHERE (id) = (?)", (client_id,))
                conn.commit()
                messagebox.showinfo("Success", "Client Deleted Successfully")
                populate_table()
            else:
                messagebox.showinfo("Canceled", "Deletion Canceled")
        else:
            messagebox.showinfo("Error", "Client ID Not Found")
        conn.close()

def is_connected(test_url = "http://www.google.com/", timeout=5):
    """
        Returns True if the connection to the test_url is successful, else False.
        """
    try:
        requests.get(test_url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False

#function that'll help me select table item
def selected_item(a):
    curItem = tree.focus()
    print(tree.item(curItem).get('values')[0])
    table_index = tree.item(curItem).get('values')[0]
    return int(table_index)


#GUI Setup
root = tk.Tk()
root.title('Client Database')
root.geometry(f"900x600")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Name:").grid(row=0, column=0)
name_entry = tk.Entry(frame)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Email:").grid(row=1, column=0)
email_entry = tk.Entry(frame)
email_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Phone:").grid(row=2, column=0)
phone_entry = tk.Entry(frame)
phone_entry.grid(row=2, column=1,padx=5, pady=5)

tk.Label(frame, text="Job:").grid(row=3, column=0)
job_entry = tk.Entry(frame)
job_entry.grid(row=3, column=1,padx=5, pady=5)

tk.Button(frame,text="Add Client", command=add_client).grid(row=4, column=0,columnspan=2, pady=10)
tk.Button(frame,text="Delete Client", command=delete_client).grid(row=5, column=0,columnspan=2, pady=10)

tree_frame = tk.Frame(root)
tree_frame.pack(pady=10)

#Create Table
tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Email", "Phone","Job"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Email", text="Email")
tree.heading("Phone", text="Phone")
tree.heading("Job", text="Job")
tree.pack()

#Select Item function call

tree.bind('<ButtonRelease-1>', selected_item)
t_index = selected_item


# Initialize DB and Populate Table
init_db()
populate_table()
root.mainloop()



