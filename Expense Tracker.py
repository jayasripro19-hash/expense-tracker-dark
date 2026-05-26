import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ---------------- DATABASE ----------------
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    amount REAL,
    category TEXT
)
""")
conn.commit()

# ---------------- FUNCTIONS ----------------
def add_expense():
    name = entry_name.get()
    amount = entry_amount.get()
    category = combo_category.get()

    if name == "" or amount == "" or category == "":
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        amount = float(amount)
    except:
        messagebox.showerror("Error", "Amount must be a number!")
        return

    cursor.execute("INSERT INTO expenses (name, amount, category) VALUES (?, ?, ?)",
                   (name, amount, category))
    conn.commit()

    entry_name.delete(0, tk.END)
    entry_amount.delete(0, tk.END)

    load_expenses()


def load_expenses():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    total = 0

    for row in rows:
        tree.insert("", tk.END, values=row)
        total += row[2]

    label_total.config(text=f"Total Expense: ₹{total:.2f}")


def delete_expense():
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "Select an item to delete")
        return

    values = tree.item(selected, "values")
    expense_id = values[0]

    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()

    load_expenses()

# ---------------- UI ----------------
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("700x500")
root.configure(bg="#121212")

style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview",
                background="#1E1E1E",
                foreground="white",
                fieldbackground="#1E1E1E")

style.configure("Treeview.Heading",
                background="#2C2C2C",
                foreground="white")

# Title
title = tk.Label(root, text="💸 Expense Tracker", font=("Arial", 20, "bold"),
                 bg="#121212", fg="white")
title.pack(pady=10)

# Input Frame
frame = tk.Frame(root, bg="#121212")
frame.pack(pady=10)

tk.Label(frame, text="Name", bg="#121212", fg="white").grid(row=0, column=0)
entry_name = tk.Entry(frame, bg="#1E1E1E", fg="white", insertbackground="white")
entry_name.grid(row=0, column=1, padx=10)

tk.Label(frame, text="Amount", bg="#121212", fg="white").grid(row=0, column=2)
entry_amount = tk.Entry(frame, bg="#1E1E1E", fg="white", insertbackground="white")
entry_amount.grid(row=0, column=3, padx=10)

tk.Label(frame, text="Category", bg="#121212", fg="white").grid(row=0, column=4)
combo_category = ttk.Combobox(frame, values=["Food", "Travel", "Bills", "Shopping", "Other"])
combo_category.grid(row=0, column=5, padx=10)

# Buttons
btn_add = tk.Button(root, text="Add Expense", command=add_expense,
                    bg="#00E5FF", fg="black")
btn_add.pack(pady=5)

btn_delete = tk.Button(root, text="Delete Selected", command=delete_expense,
                       bg="#FF5252", fg="white")
btn_delete.pack(pady=5)

# Table
tree = ttk.Treeview(root, columns=("ID", "Name", "Amount", "Category"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Amount", text="Amount")
tree.heading("Category", text="Category")

tree.column("ID", width=50)
tree.column("Name", width=200)
tree.column("Amount", width=100)
tree.column("Category", width=150)

tree.pack(pady=20, fill="both", expand=True)

# Total label
label_total = tk.Label(root, text="Total Expense: ₹0", font=("Arial", 14),
                       bg="#121212", fg="#00E5FF")
label_total.pack()

load_expenses()

root.mainloop()
