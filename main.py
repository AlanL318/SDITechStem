from tkinter import *
from pandas import *
import random

# setting tkinter window
window = Tk()
window.state("zoomed")
window.update_idletasks()
window.configure(bg="#485c34")
window.title("Typing Test")

# opens csv file and converts to ONE list for data management
data = read_csv("typingwords.csv")
words = data["instance"].tolist()
random.shuffle(words)
splicedwords = words[:150]

# define global variables that are used later
typedValue = []
totalWords = []
fontTuple = ("Courier New", 16, "bold")
color = "#485c34"
# displays the words

x1 = Label(window, text=splicedwords, wraplength=1100, fg="#dbd7a6")
x1.config(bg=color)
x1.config(font=fontTuple)
x1.pack(ipadx=500, ipady=200)


def on_space(e1):
    global wpm
    global accuracy
    x = splicedwords.pop(0)  # removes the word that was typed
    if e1.widget.get().lstrip() != x:   # checks if the word typed was equal to the word displayed
        totalWords.append(e1.widget.get())     # Whether word is correct or not, inputs into total words typed
        e1.widget.delete(0, "end")
        x1.config(text=splicedwords)
        pass
    else:
        typedValue.append(x)    # if word is accurate, appends the value of the typed word into a new list for counting
        totalWords.append(e1.widget.get())
        e1.widget.delete(0, "end")
        x1.config(text=splicedwords)

    wpm = len(typedValue)   # measures wpm on how many words were typed correctly
    accuracy = int((wpm / len(totalWords)) * 100)  # measures accuracy based on the correct words divided by total words


# Display Timer
sec = int(60)
time = str(f"00:{sec}")
c1 = Label(window, text=time, wraplength=500, fg="white")
c1.config(bg=color)
c1.config(font=fontTuple)
c1.pack()


def countdown(count):
    if count > 0:
        window.after(1000, countdown, count - 1)    # measures time based on every 1000 milliseconds
        c1.config(text=count)
    if count == 0:
        window.destroy()    # once timer reaches 0, a new window appears that displays wpm and accuracy
        root = Tk()
        root.geometry("500x500")
        r1 = Label(root, text=f"Your wpm is {wpm}!\nAccuracy: {accuracy}% !", wraplength=1100, fg="black")
        root.title("Stats")
        r1.config(font=fontTuple)
        r1.pack(ipadx=500, ipady=200)


# Displays and creates the function of the Entry window
e1 = Entry(window)
e1.config(font=fontTuple)
e1.bind("<space>", on_space)    # registers when a word is typed
e1.bind("<Button-1>", lambda event: countdown(60))  # On left click start timer
e1.place(x=500, y=310)
e1.pack()


window.mainloop()
