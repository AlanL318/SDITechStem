from tkinter import *
import random
import sys
from pandas import *

window = Tk()

# setting tkinter window size
window.state("zoomed")
window.update_idletasks()
window.configure(bg="gray")
window.title("Typing Test")

# opens csv file and converts to ONE list for data management
data = read_csv("typingwords.csv")
words = data["instance"].tolist()
random.shuffle(words)
splicedwords = words[:150]

# displays the words
fontTuple = ("Playfair Display", 16, "bold")
x1 = Label(window, text=splicedwords, wraplength=1100, fg="white")
x1.config(bg="gray")
x1.config(font=fontTuple)
x1.pack(ipadx=500, ipady=20)


# global variables that are used later
typedValue = []


def on_space(e1):
    global typedValue
    global wpm
    x = splicedwords.pop(0)  # removes the word that was typed
    if e1.widget.get().lstrip() != x:   # checks if the word typed was equal to the word displayed
        e1.widget.delete(0, "end")
        x1.config(text=splicedwords)
        pass
    else:
        typedValue.append(x)    # if word is accurate, appends the value of the typed word into a new list for counting
        e1.widget.delete(0, "end")
        x1.config(text=splicedwords)
    wpm = len(typedValue)


# Display Timer
sec = int(60)
time = str(f"00:{sec}")
c1 = Label(window, text=time, wraplength=500, fg="white")
c1.config(bg="gray")
c1.config(font=fontTuple)
c1.pack(ipadx=500, ipady=200)


# code for the timer
def countdown(count):
    if count > 0:
        window.after(1000, countdown, count - 1)
        c1.config(text=count)
    if count == 0:
        sys.exit(f"Time's Up! Your words per minute is {wpm}")


# Displays and creates the function of the Entry window
fontTuple = ("Playfair Display", 16, "bold")
e1 = Entry(window)
e1.config(font=fontTuple)
e1.bind("<space>", on_space)    # registers when a word is typed
e1.bind("<Button-1>", lambda event: countdown(60))  # On left click start timer
e1.pack()


window.mainloop()
