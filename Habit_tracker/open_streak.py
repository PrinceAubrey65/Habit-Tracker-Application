from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import os
import shutil
import platform

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





def openstreak(root, streak_name):
        btns = []
        def crosser(btn_number):
                text_on_btn = day_btn["text"]

                btns[btn_number -1].configure(text="X")

                Xed_storer(btn_number,Xed_btns)


        def Xed_storer(counting,Xed_btns):
                try:
                        #Create a database 
                        conn = sqlite3.connect(db_path)
                        #Create a cursor instance
                        c = conn.cursor()
                        
                        c.execute(F"INSERT INTO {Xed_btns} VALUES(:btn)",
                        {
                        'btn' : counting
                        }
                        )
                        #Commit changes
                        conn.commit()
                        #Close our connection
                        conn.close()

                        btns[counting -1].configure(text="X")

                except UnboundLocalError:
                        pass


        global open_streak_page
        open_streak_page = Toplevel()
        open_streak_page.title("Add a Streak")
        open_streak_page.geometry("700x570")
        root.withdraw()

        # ---------------functions----------------
        # this function takes you to the previuos page 
        def back():
                # Close the new window
                open_streak_page.destroy()
                # Show the parent window again
                root.deiconify()

        #Create a database 
        conn = sqlite3.connect(db_path)

        #Create a cursor instance
        c = conn.cursor()

        # Create table 
        c.execute("CREATE TABLE IF NOT EXISTS STREAKS (name TEXT, days INTEGER)")

        # Create table name for Xed buttons
        Xed_btns = streak_name + "Details"
        # Create table for Xed buttons
        c.execute(f"CREATE TABLE IF NOT EXISTS {Xed_btns} (buttons INTEGER)")

        c.execute(f"SELECT * FROM {Xed_btns}")
        already_Xed = c.fetchall()


        no_of_Xed = len(already_Xed)

        indexer = 0

        Xed_list = []
        while True:
                if indexer >= no_of_Xed:
                        break
                else:
                        resoz = already_Xed[indexer][0]
                        
                        Xed_list.append(resoz)

                indexer += 1

        #Create Table for recipes
        c.execute("SELECT rowid, * FROM STREAKS WHERE name = ?", (streak_name,))
        results = c.fetchall()
        days = results[0][2]
        
        #Use the days to create boxes
        counter = 1
        row_break = 0
        col_restart = 0
        
        while True:              
                if counter  == days + 1:
                        break

                #Put button on main screen
                day_btn = Button(open_streak_page, text="{}".format(counter),command=lambda counter = counter:crosser(counter))
                day_btn.grid(row=row_break, column=col_restart, padx=10, pady=10, ipadx=10, ipady=10)

                btns.append(day_btn)

                if counter in Xed_list:
                        Xed_storer(counter,Xed_btns)
                

                col_restart += 1

                if counter % 8 == 0:
                        row_break += 1
                        col_restart = 0

                counter += 1

        #Commit changes
        conn.commit()

        #Close our connection
        conn.close()

        # Catch the WM_DELETE_WINDOW event
        open_streak_page.protocol("WM_DELETE_WINDOW", back)
        return