import sqlite3
import tkinter as tk
from tkinter import messagebox

medicines=[]  # list of dictionaries
conn=sqlite3.connect("medicines.db")
cursor = conn.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS medicines (name TEXT PRIMARY KEY,quantity INTEGER)")
conn.commit()


def load_medicines():
    medicines.clear()
    cursor.execute("SELECT name,quantity FROM medicines")
    rows=cursor.fetchall()
    for name,qty in rows:
        medicines.append({"name":name,"quantity":qty})


def add_medi():
    name=name_entry.get()
    qty=qty_entry.get()

    if name=="" or qty=="":
        messagebox.showerror("Errorrrrrrrrr","all fields required")
        return

    if not qty.isdigit():
        messagebox.showerror("Errorrrr!!","Quantity must be a number")
        return

    try:
        cursor.execute("INSERT INTO medicines (name, quantity) VALUES (?, ?)",(name, int(qty)),)
        conn.commit()
        messagebox.showinfo("Success", "Medicine Added")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Medicine already exists")

    name_entry.delete(0, tk.END)
    qty_entry.delete(0, tk.END)


# bubble sortt
def sort_medicines():
    n = len(medicines)
    for i in range(n):
        for j in range(0,n-i-1):
            if medicines[j]["name"].lower()>medicines[j+1]["name"].lower():
                medicines[j],medicines[j+1]=medicines[j+1],medicines[j]


#binary search
def binary_search_medicine(target):
    low=0
    high=len(medicines)-1

    while low<=high:
        mid=(low+high)//2
        mid_name=medicines[mid]["name"].lower()

        if mid_name==target.lower():
            return mid
        elif mid_name<target.lower():
            low=mid+1
        else:
            high=mid-1

    return -1


def view_medicines():
    display.delete(1.0, tk.END)

    cursor.execute("SELECT * FROM medicines")
    rows = cursor.fetchall()

    if not rows:
        display.insert(tk.END, "No medicines available\n")
        return

    for name, qty in rows:
        display.insert(tk.END, f"Name: {name} | Qty: {qty}\n")


def distribute_medicine():
    name = dist_entry.get()
    qty = dist_qty_entry.get()

    if name == "" or qty == "":
        messagebox.showerror("Error", "Both fields required")
        return

    if not qty.isdigit():
        messagebox.showerror("Error", "Quantity must be a number")
        return

    qty = int(qty)
    load_medicines()
    sort_medicines()

    index = binary_search_medicine(name)

    if index == -1:
        messagebox.showerror("Error", "Medicine not found")
        return

    cursor.execute(
        "SELECT quantity FROM medicines WHERE name = ?", (name,)
    )
    result = cursor.fetchone()

    if result:
        current_qty = result[0]
        if current_qty >= qty:
            cursor.execute(
                "UPDATE medicines SET quantity = ? WHERE name = ?",
                (current_qty - qty, name),
            )
            conn.commit()
            messagebox.showinfo("Success", "Medicine Distributed")
            view_medicines()
        else:
            messagebox.showwarning(
                "Insufficient Stock",
                f"Only {current_qty} units available",
            )


# ui
root = tk.Tk()
root.title("Medicine Distribution System")
root.geometry("400x500")

tk.Label(
    root,
    text="Medicine Distribution System",
    font=("Arial", 14, "bold"),
).pack(pady=10)

tk.Label(root, text="Medicine Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Quantity").pack()
qty_entry = tk.Entry(root)
qty_entry.pack()

tk.Button(root, text="Add Medicine", command=add_medi).pack(pady=5)

tk.Button(root, text="View Medicines", command=view_medicines).pack(pady=5)

tk.Label(root, text="Distribute Medicine (Enter Name)").pack(pady=5)
dist_entry = tk.Entry(root)
dist_entry.pack()

tk.Label(root, text="Quantity to Distribute").pack(pady=2)
dist_qty_entry = tk.Entry(root)
dist_qty_entry.pack()

tk.Button(
    root,
    text="Distribute",
    command=distribute_medicine,
).pack(pady=5)

display = tk.Text(root, height=12, width=45)
display.pack(pady=10)

root.mainloop()
