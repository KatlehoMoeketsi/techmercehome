#This project will serve as a database for local SMMEs and potential client/client information for Techmerce.
#It will use tkInter for GUI and will initially use a simple local SQL database, then we will move towards firebase
#for cloud services.

import sqlite3
import tkinter as tk
from idlelib.debugger_r import restart_subprocess_debugger
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


#Delete Client Window
def open_delete_window():
    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Client")
    delete_window.geometry("300x150")

    tk.Label(delete_window, text="Client ID to Delete: ").pack()
    id_entry = tk.Entry(delete_window)
    id_entry.pack()


    def delete_client():
        # Get the id from the input
        client_id = id_entry.get()
        if not client_id.isdigit():
            messagebox.showerror("Error", "Please enter a valid numeric ID")
            return

        conn = sqlite3.connect("clients.db")
        cursor = conn.cursor()

        # check if client exists
        cursor.execute("SELECT * FROM clients WHERE id=?", (client_id))
        result = cursor.fetchone();

        if result:
            confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete Client ID {client_id}?")
            if confirm:
                # Important code below: Executes the SQL command on the database
                cursor.execute("DELETE FROM clients WHERE (id) = (?)", (client_id,))
                conn.commit()
                messagebox.showinfo("Success", "Client Deleted Successfully")
            else:
                messagebox.showinfo("Canceled", "Deletion Canceled")
        else:
            messagebox.showinfo("Error", "Client ID Not Found")
        conn.close()
        id_entry.delete(0, tk.END)  # Clear the input

    tk.Button(delete_window, text="Delete", command=delete_client).pack()

#GUI Setup
root = tk.Tk()
root.title('Client Database')
root.geometry("400x300")

tk.Label(root, text="Name:").grid(row=0, column=1)
name_entry = tk.Entry(root)
name_entry.grid(row=1, column=1)

tk.Label(root, text="Email:").grid(row=2, column=1)
email_entry = tk.Entry(root)
email_entry.grid(row=3, column=1)

tk.Label(root, text="Phone:").grid(row=4, column=1)
phone_entry = tk.Entry(root)
phone_entry.grid(row=5, column=1)



tk.Button(root,text="Add Client", command=add_client).grid(row=6, column=1, padx= 5, pady= 8)
tk.Button(root,text="Delete Client", command=open_delete_window).grid(row=7, column=1, padx= 5, pady= 8)

init_db()

root.mainloop()



