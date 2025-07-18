import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

FILE_NAME = "contacts.json"

# Load existing contacts
def load_contacts():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return []

# Save contacts to file
def save_contacts():
    with open(FILE_NAME, "w") as file:
        json.dump(contacts, file, indent=4)

# Add new contact
def add_contact():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()

    if name == "" or phone == "" or email == "":
        messagebox.showwarning("Input Error", "All fields are required.")
        return

    contacts.append({"name": name, "phone": phone, "email": email})
    save_contacts()
    update_listbox()
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

# Update the contact listbox
def update_listbox():
    contact_listbox.delete(0, tk.END)
    for idx, contact in enumerate(contacts):
        contact_listbox.insert(tk.END, f"{idx+1}. {contact['name']}")

# View selected contact
def view_contact():
    try:
        index = contact_listbox.curselection()[0]
        contact = contacts[index]
        messagebox.showinfo("Contact Details",
                            f"Name: {contact['name']}\nPhone: {contact['phone']}\nEmail: {contact['email']}")
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a contact to view.")

# Edit selected contact
def edit_contact():
    try:
        index = contact_listbox.curselection()[0]
        contact = contacts[index]
        new_name = simpledialog.askstring("Edit Name", "Enter new name:", initialvalue=contact['name'])
        new_phone = simpledialog.askstring("Edit Phone", "Enter new phone number:", initialvalue=contact['phone'])
        new_email = simpledialog.askstring("Edit Email", "Enter new email:", initialvalue=contact['email'])

        if new_name and new_phone and new_email:
            contacts[index] = {"name": new_name, "phone": new_phone, "email": new_email}
            save_contacts()
            update_listbox()
        else:
            messagebox.showwarning("Edit Cancelled", "All fields must be filled.")
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a contact to edit.")

# Delete selected contact
def delete_contact():
    try:
        index = contact_listbox.curselection()[0]
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this contact?")
        if confirm:
            contacts.pop(index)
            save_contacts()
            update_listbox()
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a contact to delete.")

# ---------------- GUI Setup ---------------- #
contacts = load_contacts()

root = tk.Tk()
root.title("📒 Contact Management System")

# Input fields
tk.Label(root, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
tk.Label(root, text="Phone:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
tk.Label(root, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky='e')

name_entry = tk.Entry(root)
phone_entry = tk.Entry(root)
email_entry = tk.Entry(root)

name_entry.grid(row=0, column=1, padx=5, pady=5)
phone_entry.grid(row=1, column=1, padx=5, pady=5)
email_entry.grid(row=2, column=1, padx=5, pady=5)

# Buttons
tk.Button(root, text="Add Contact", command=add_contact).grid(row=3, column=0, columnspan=2, pady=10)

contact_listbox = tk.Listbox(root, width=40)
contact_listbox.grid(row=0, column=2, rowspan=6, padx=10, pady=5)

tk.Button(root, text="View Contact", command=view_contact).grid(row=4, column=0, columnspan=2, pady=5)
tk.Button(root, text="Edit Contact", command=edit_contact).grid(row=5, column=0, columnspan=2, pady=5)
tk.Button(root, text="Delete Contact", command=delete_contact).grid(row=6, column=0, columnspan=2, pady=5)

update_listbox()
root.mainloop()
