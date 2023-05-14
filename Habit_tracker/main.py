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
    appdata_path = os.environ['APPDATA', 'Habit_Tracker_Database']

    # Construct the path to the database file
    db_path = os.path.join(appdata_path, db_filename)

    # Create the directory if it doesn't exist
    if not os.path.exists(appdata_path):
        os.makedirs(appdata_path)

    # Connect to the database and create the necessary tables
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Create table 
    c.execute("CREATE TABLE IF NOT EXISTS STREAKS (name TEXT, days INTEGER)")
    conn.commit()
    conn.close()

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




# import add_streak
from add_streak import *
from del_streak import *
from open_streak import *

root = customtkinter.CTk()
root.title('Habbit Tracker')
root.geometry('700x570')
root.resizable(False, False)

#Create a  frame
main_frame = customtkinter.CTkFrame(master=root)
main_frame.grid(row=0,column=0,pady=10)

# frame for streaks 
#!Add a scrollbar to go through the created streaks if they don't fit on the screen
# customtkinter.CTkFrame(master=main_frame)
streak_frame = customtkinter.CTkFrame(master=main_frame)
streak_frame.grid(row=1,column=0,pady=10,columnspan=6,ipadx=80,sticky="nsew")



def create_streak_boxes():
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

        #get no of days in a streak
        c.execute("SELECT rowid, * FROM STREAKS WHERE name = ?", (name_of_box,))
        resoz = c.fetchall()
        days = resoz[0][2]
        print("Days: ")
        print(days)

        # Create table name for Xed buttons
        Xed_btns = name_of_box + "Details"
        c.execute(f"SELECT * FROM {Xed_btns}")
        already_Xed = c.fetchall()
        print("List of Xed: ")
        print(already_Xed) #create a list of non repeated days from this
        no_of_Xed = len(already_Xed)
        print("No of Xed: ")
        print(no_of_Xed)

        counter_label = customtkinter.CTkLabel(master=streak_frame, text=count + 1)
        counter_label.grid(row=count,column=1,pady=10)

        percentage_label = customtkinter.CTkLabel(master=streak_frame, text=" ")
        counter_label.grid(row=count,column=3,pady=10)
        
        #Put button on main screen
        streak_btn = customtkinter.CTkButton(master=streak_frame, text=name_of_box, width=500, height=100, anchor="center", command=lambda name_of_box = name_of_box:openstreak(root,name_of_box))

        streak_btn.grid(row=count, column=2, pady=10, padx=10, columnspan=3)

        count += 1

    #Commit changes
    conn.commit()

    #Close our connection
    conn.close()

create_streak_boxes()

# top of main screen
title = customtkinter.CTkLabel(master=main_frame, text="Streaks", font=('monospace', 60))
title.grid(row=0, column=0)

# buttons 
add_streak = customtkinter.CTkButton(master=main_frame,fg_color="#38761d", hover_color="#739F60", text="Add Streak", command=lambda:addStreak(root, streak_frame))
add_streak.grid(row=0, column=1, padx=70)

del_streak = customtkinter.CTkButton(master=main_frame, fg_color="#38761d", hover_color="#739F60", text="Delete Streak", command=lambda:delStreak(root,streak_frame))
del_streak.grid(row=0, column=2)

root.mainloop()
