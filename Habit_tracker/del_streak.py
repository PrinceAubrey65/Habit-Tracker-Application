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





# import add_streak
from add_streak import *
from open_streak import *


def Streaker_the_second(root):
    global Streaker_the_second_page
    Streaker_the_second_page = Tk()
    Streaker_the_second_page.title("Habit Tracker")
    Streaker_the_second_page.geometry("700x570")

    #Create a  frame
    main_frame = Frame(Streaker_the_second_page)
    main_frame.grid(row=0,column=0,pady=10)

    # frame for streaks 
    #!Add a scrollbar to go through the created streaks if they don't fit on the screen
    second_streak_frame = LabelFrame(main_frame,text="")
    second_streak_frame.grid(row=1,column=0,pady=10,columnspan=3,ipadx=80,sticky="nsew")

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

                #counter
                counter_label = Label(second_streak_frame,text=count + 1)
                counter_label.grid(row=count,column=1,pady=10)
                
                #Put button on main screen
                streak_btn = Button(second_streak_frame, text=name_of_box,width=60, height=5, anchor="center", command=lambda name_of_box = name_of_box:openstreak(Streaker_the_second_page,name_of_box))
                streak_btn.grid(row=count, column=2, pady=10, padx=10)

                count += 1

            #Commit changes
            conn.commit()

            #Close our connection
            conn.close()

    create_streak_boxes()

    def back():
        root.destroy()
        Streaker_the_second_page.destroy()

    # top of main screen
    title = Label(main_frame, text="Streaks", font=('monospace', 30))
    title.grid(row=0, column=0)
    add_streak = Button(main_frame, text="Add Streak", command=lambda:addStreak(Streaker_the_second_page, second_streak_frame))
    add_streak.grid(row=0, column=1, padx=70)
    del_streak = Button(main_frame, text="Delete Streak", command=lambda:delStreak(Streaker_the_second_page,second_streak_frame))
    del_streak.grid(row=0, column=2)

    # Catch the WM_DELETE_WINDOW event
    Streaker_the_second_page.protocol("WM_DELETE_WINDOW", back)


def delStreak(root, streak_frame):
    global delStreak_page
    delStreak_page = Toplevel()
    delStreak_page.title("Delete Streak")
    delStreak_page.geometry("600x570")
    root.withdraw()

    delStreak_frame = Frame(delStreak_page)
    delStreak_frame.grid(row=0,column=0,pady=10,padx=5)

    #labels and entry boxes
    streak_name_label = Label(delStreak_frame,text="Enter name of Streak: ")
    streak_name_label.grid(row=0,column=0,pady=10)
    streak_name_entry = Entry(delStreak_frame)
    streak_name_entry.grid(row=0,column=1,pady=10)

    # --------------------------functions-----------------

    def Drop_it():
        #Create a database 
        conn = sqlite3.connect(db_path)

        #Create a cursor instance
        c = conn.cursor()

        c.execute("SELECT name, COUNT(*) FROM STREAKS WHERE name = ?", (streak_name_entry.get(),))
        duplicates = c.fetchall()
        name_of_streak = duplicates[0][0]

        table_details = streak_name_entry.get() + "Details"

        if name_of_streak == None:
            messagebox.showerror("Error!","Please enter exact name of streak")
            return
        else:
            # Delete streak
            c.execute("DELETE FROM STREAKS WHERE name = ?",(streak_name_entry.get(),))

            #Delete table keeping streak details
            c.execute(f"DROP TABLE IF EXISTS {table_details}")


        #Commit changes
        conn.commit()

        #Close our connection
        conn.close()

        # close screen
        back()

    def back():
        # Close the new window
        delStreak_page.destroy()

        # create_streak_boxes(root,streak_frame)
        Streaker_the_second(root)


    # --------------------Buttons-------------------------
    del_streak_btn = Button(delStreak_frame, text="Delete Streak", command=Drop_it)
    del_streak_btn.grid(row=2, column=0)

    # Catch the WM_DELETE_WINDOW event
    delStreak_page.protocol("WM_DELETE_WINDOW", back)