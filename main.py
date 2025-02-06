#This project will serve as a database for local SMMEs and potential client/client information for Techmerce.
#It will use tkInter for GUI and will initially use a simple local SQL database, then we will move towards firebase
#for cloud services.

import sqlite3
import tkinter as tk
from tkinter import messagebox

#Setting up the Database
def init_db():
    conn = sqlite3.connect("clients.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT)''')

    conn.commit()
    conn.close()

#Add Client
def add_client():
    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()

    if not name:
        messagebox.showerror("Error", "Name is required")
        return

    conn = sqlite3.connect("clients.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clients (name, email, phone) VALUES (?, ?, ?)", (name,email,phone))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success","Client Added Successfully")
    name_entry.delete(0,tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)


#GUI Setup
root = tk.Tk()
root.title('Client Database')
root.geometry("400x300")

tk.Label(root, text="Name:").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Email:").pack()
email_entry = tk.Entry(root)
email_entry.pack()

tk.Label(root, text="Phone:").pack()
phone_entry = tk.Entry(root)
phone_entry.pack()

tk.Button(root,text="Add Client", ).pack

init_db()

root.mainloop()



