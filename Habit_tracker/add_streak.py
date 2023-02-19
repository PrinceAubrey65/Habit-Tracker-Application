from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

from open_streak import *

def create_streak_boxes(root,streak_frame):
    #Create a database 
    conn = sqlite3.connect('streaker.db')

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
        counter_label = Label(streak_frame,text=count + 1)
        counter_label.grid(row=count,column=1,pady=10)
        
        #Put button on main screen
        streak_btn = Button(streak_frame, text=name_of_box,width=60, height=5, anchor="center", command=lambda name_of_box = name_of_box:openstreak(root,name_of_box))
        streak_btn.grid(row=count, column=2, pady=10, padx=10)

        count += 1

    #Commit changes
    conn.commit()

    #Close our connection
    conn.close()



def addStreak(root,streak_frame):
    global add_streak_page
    add_streak_page = Toplevel()
    add_streak_page.title("Add a Streak")
    add_streak_page.geometry("600x570")
    root.withdraw()

    add_streak_frame = Frame(add_streak_page)
    add_streak_frame.grid(row=0,column=0,pady=10,padx=5)

    #labels and entry boxes
    streak_name_label = Label(add_streak_frame,text="Name of Streak: ")
    streak_name_label.grid(row=0,column=0,pady=10)
    streak_name_entry = Entry(add_streak_frame)
    streak_name_entry.grid(row=0,column=1,pady=10)

    length_label = Label(add_streak_frame,text="Number of Days: ")
    length_label.grid(row=1,column=0,pady=10)
    length_entry = Entry(add_streak_frame)
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
        conn = sqlite3.connect('streaker.db')

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

        if int(Days) > 64 :
            messagebox.showinfo("ALERT", "Only Pro version can allow streaks longer than 64 days.\nContact Developer for more information.\nWhatsapp: 0778728406\nEmail:\nnuwagabaprinceaubrey@gmail.com")
            return

        if len(Days.replace(" ","")) < 1 or  len(StreakName.replace(" ","")) < 1: 
                messagebox.showinfo("ALERT!","Fill in all entry boxes!")
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
    create_streak_btn = Button(add_streak_frame, text="Create Streak", command=create_streak)
    create_streak_btn.grid(row=2, column=0)

    # Catch the WM_DELETE_WINDOW event
    add_streak_page.protocol("WM_DELETE_WINDOW", back)

    return