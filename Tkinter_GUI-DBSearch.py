import tkinter as tk
import pyodbc

def get_databases():
    server_name = server_entry.get()
    connection = pyodbc.connect('DRIVER={SQL Server};SERVER='+server_name+';Trusted_Connection=yes;')
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sys.databases")
    global databases
    databases = cursor.fetchall()
    listbox.delete(0, tk.END)
    for database in databases:
        listbox.insert(tk.END, database[0])
        
def search_databases(event):
    global databases
    search_text = search_entry.get().lower()
    listbox.delete(0, tk.END)
    for database in databases:
        if database[0].lower().find(search_text) != -1:
            listbox.insert(tk.END, database[0])


root = tk.Tk()
root.title("SQL Server Database Explorer")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Get the window width and height
window_width = 500
window_height = 350

# Calculate the coordinates for centering the window
x_coord = (screen_width/2) - (window_width/2)
y_coord = (screen_height/2) - (window_height/2)

# Set the window geometry
root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coord, y_coord))

# configure the grid layout
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(3, weight=1)


server_label = tk.Label(root, text="Server Name:")
server_label.grid(row=0, column=0, sticky="W", padx=10, pady=10)

server_entry = tk.Entry(root)
server_entry.grid(row=0, column=1)

get_databases_button = tk.Button(root, text="Get Databases", command=get_databases)
get_databases_button.grid(row=0, column=2, pady=5)

# create the search entry
search_label = tk.Label(root, text="Search:")
search_label.grid(row=1, column=0, sticky="W", padx=10, pady=10)
search_entry = tk.Entry(root)
search_entry.grid(row=1, column=1, sticky="E", padx=10, pady=10)
search_entry.bind("<KeyRelease>", search_databases)

# create the listbox and scrollbar
listbox = tk.Listbox(root)
listbox.grid(row=3, column=0, columnspan=3, sticky="NSEW", padx=10, pady=10)

scrollbar = tk.Scrollbar(root, orient="vertical", command=listbox.yview)
scrollbar.grid(row=3, column=3, sticky="NS")
listbox.configure(yscrollcommand=scrollbar.set)

root.mainloop()