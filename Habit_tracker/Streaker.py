from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3


# import add_streak
from add_streak import *
from del_streak import *
from open_streak import *

root = Tk()
root.title('Habbit Tracker')
root.geometry('700x570')
root.resizable(False, False)

#Create a  frame
main_frame = Frame(root)
main_frame.grid(row=0,column=0,pady=10)

# frame for streaks 
#!Add a scrollbar to go through the created streaks if they don't fit on the screen
streak_frame = LabelFrame(main_frame,text="")
streak_frame.grid(row=1,column=0,pady=10,columnspan=3,ipadx=80,sticky="nsew")


def create_streak_boxes():
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
    print(total_iterations)

    count = 0
    

    while True:
        if total_iterations == count:
            break
    

        name_of_box = results[count][1]
        
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

create_streak_boxes()

# top of main screen
title = Label(main_frame, text="Streaks", font=('monospace', 30))
title.grid(row=0, column=0)

add_streak = Button(main_frame, text="Add Streak", command=lambda:addStreak(root, streak_frame))
add_streak.grid(row=0, column=1, padx=70)

del_streak = Button(main_frame, text="Delete Streak", command=lambda:delStreak(root,streak_frame))
del_streak.grid(row=0, column=2)

root.mainloop()