from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import os
import shutil
import platform
import customtkinter

customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_appearance_mode("dark")

if platform.system() == 'Windows':
    # Run code specific to Windows operating system

    # Replace 'mydatabase.db' with your desired filename
    db_filename = 'streaker.db'

    # Construct the path to the AppData folder
    appdata_path = os.environ['Habit_Tracker_Database']

    # Construct the path to the database file
    db_path = os.path.join(appdata_path, db_filename)


    # Move the database file to the AppData folder
    shutil.move(db_filename, db_path)

else:
    # Run code for linux

    # Get home dir
    home_dir = os.path.expanduser("~")

    # Path to the folder where the database file will be created
    folder_name = 'Habit_Tracker_Database'
    folder_path = os.path.join(home_dir, folder_name)

    # If the folder doesn't exist, create it
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Path to the database file
    db_path = os.path.join(folder_path, 'streaker.db')





from open_streak import *

def create_streak_boxes(root,streak_frame):
    #Create a database 
    conn = sqlite3.connect(db_path)

    #Create a cursor instance
    c = conn.cursor()

    # Create table 
    c.execute("CREATE TABLE IF NOT EXISTS STREAKS (name TEXT, days INTEGER)")

    #Create Table for recipes
    c.execute("SELECT rowid, * FROM STREAKS")
    results = c.fetchall()

    total_iterations = len(results)

    count = 0

    while True:
        if total_iterations == count:
            break
    
        name_of_box = results[count][1]

        #counter
        counter_label = customtkinter.CTkLabel(master=streak_frame, text=count + 1)
        counter_label.grid(row=count,column=1,pady=10)
        
        #Put button on main screen
        streak_btn = customtkinter.CTkButton(master=streak_frame, text=name_of_box, width=500, height=100, anchor="center", command=lambda name_of_box = name_of_box:openstreak(root,name_of_box))
        streak_btn.grid(row=count, column=2, pady=10, padx=10, columnspan=3)

        count += 1

    #Commit changes
    conn.commit()

    #Close our connection
    conn.close()



def addStreak(root,streak_frame):
    global add_streak_page
    add_streak_page = Toplevel()
    add_streak_page.config(bg="#252525")
    add_streak_page.title("Add a Streak")
    add_streak_page.geometry("600x570")
    root.withdraw()

    add_streak_frame = customtkinter.CTkFrame(master=add_streak_page)
    add_streak_frame.grid(row=0,column=0,pady=10,padx=5)

    #labels and entry boxes
    streak_name_label = customtkinter.CTkLabel(master=add_streak_frame, text="Name of Streak: ")
    streak_name_label.grid(row=0,column=0,pady=10)
    streak_name_entry = customtkinter.CTkEntry(master=add_streak_frame, placeholder_text="Enter the Name of your Streak", width=300, height=40)
    streak_name_entry.grid(row=0,column=1,pady=10)

    length_label = customtkinter.CTkLabel(master=add_streak_frame, text="Number of Days: ")
    length_label.grid(row=1,column=0,pady=10)
    length_entry = customtkinter.CTkEntry(master=add_streak_frame, placeholder_text="Enter Number of Days", width=300, height=40)
    length_entry.grid(row=1,column=1,pady=10)

    #-----------------------functions ------------------
    # this function takes you to the previuos page 
    def back():
        create_streak_boxes(root,streak_frame)

        # Close the new window
        add_streak_page.destroy()
        # Show the parent window again
        root.deiconify()

    def create_streak():
        #Create a database 
        conn = sqlite3.connect(db_path)

        #Create a cursor instance
        c = conn.cursor()

        #Check if 4 streaks
        c.execute("SELECT rowid, * FROM STREAKS")
        results = c.fetchall()

        total_iterations = len(results)

        if total_iterations >= 4:
            messagebox.showinfo("ALERT!","Download Pro Version to get more than 4 streaks.\n   \n \nDeveloper Contacts\nWhatsapp: 0778728406\nTelegram: @iam_Aub\nEmail: nuwagabaprinceaubrey@gmail.com")
            return

        # Streak Name
        StreakName = streak_name_entry.get()
        # Number of Days
        Days = length_entry.get()

        

        if len(Days.replace(" ","")) < 1 or  len(StreakName.replace(" ","")) < 1: 
                messagebox.showinfo("ALERT!","Fill in all entry boxes!")
                return
        if int(Days) > 64 :
            messagebox.showinfo("ALERT", "Only Pro version can allow streaks longer than 64 days.\nContact Developer for more information.\nWhatsapp: 0778728406\nEmail:\nnuwagabaprinceaubrey@gmail.com")
            return

        #Create table for streak names
        c.execute("CREATE TABLE IF NOT EXISTS STREAKS (name TEXT, days INTEGER)")

        
        #Insert ingredients into specific table
        c.execute("INSERT INTO STREAKS VALUES(:name, :days)",
        {
            'name' : StreakName.replace(" ","_"),
            'days' : Days
        }
        )

        #Commit changes
        conn.commit()

        #Close our connection
        conn.close()

        #close screen
        back()

        return

    # buttons
    create_streak_btn = customtkinter.CTkButton(master=add_streak_frame, text="Create Streak",fg_color="#38761d", hover_color="#739F60", command=create_streak)
    create_streak_btn.grid(row=2, column=0)

    # Catch the WM_DELETE_WINDOW event
    add_streak_page.protocol("WM_DELETE_WINDOW", back)

    return
