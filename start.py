import tkinter
import tkinter.font as TkFont
from subprocess import call
import datetime
import subprocess
import sys

root = tkinter.Tk()
root.title("Sistem za identifikaciju zaposlenog")
root.geometry("1208x565")
root.resizable(False, False)

font = ("Helvetica", 20, "bold")
font2 = ("Arial", 12, "bold")

def promeniVreme():
    trenutnoVreme = datetime.datetime.now().strftime("%d" + "/" + "%m" + "/" + "%Y - %H:%M:%S")
    label1['text'] = trenutnoVreme
    label1.after(1, promeniVreme)

def spawn_program_and_die(program, exit_code=0):
    """
    Start an external program and exit the script
    with the specified return code.

    Takes the parameter program, which is a list
    that corresponds to the argv of your command.
    """
    # Start the external program
    subprocess.Popen(program)
    # We have started the program, and can suspend this interpreter
    sys.exit(exit_code)


def prijava():
    call(["python", "prijava.py"])
def odjava():
    call(["python", "odjava.py"])

label1 = tkinter.Label(root, text="Vreme", fg="white", bg="navy", width=110, font="15", height=2)
label1.grid(row=0, column=0)

btn1 = tkinter.Button(root, text="Prijava", fg="green", command=prijava, font=font, padx="260", pady="200")
btn1.grid(row = 1, column = 0, sticky=tkinter.W)

btn2 = tkinter.Button(root, text="Odjava", fg="red", command=odjava, font=font, padx="240", pady="200")
btn2.grid(row = 1, column = 0, sticky=tkinter.E)

label2 = tkinter.Label(root, text="Skenirajte bar kod karticu odabirom opcije iznad", fg="white", bg="#856ff8", width=110, font="15", height=2)
label2.grid(row=2, column=0)


promeniVreme()
root.mainloop()
