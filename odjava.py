import tkinter
import sqlite3
from tkinter import messagebox
from subprocess import call
import subprocess
import sys
import socket
import threading

host = "127.0.0.1"
port = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


root = tkinter.Tk()
root.title("Odjava")
w = 600
h =100
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
font = ("Arial", 10, "bold")

bar_kod = tkinter.StringVar()

lbl1 = tkinter.Label(root, text="Očitajte vaš bar kod", font=font)
lbl1.grid(row = 0, column = 0, padx=(25,10), pady=(40, 10))

e1 = tkinter.Entry(root, width="40", textvariable=bar_kod)
e1.grid(row = 0, column = 1, padx=0, pady=(40, 10))

e1.focus_set()
flag = "ODJAVA"
def proveriBarkod():
    if len(e1.get()) == 0:
        messagebox.showerror(title="Greška", message="Niste uneli barcode!")
    elif len(e1.get()) > 1:
        conn = sqlite3.connect("zaposleni.db")
        cursor = conn.cursor()
        bar_kod = e1.get()
        upit = f"""
                        SELECT *
                        FROM zaposleni
                        WHERE id = '{bar_kod}' AND naPoslu = 'Da'
                """
        cursor.execute(upit)
        rezultat = cursor.fetchall()

        if rezultat:
            messagebox.showinfo(title="Uspešna odjava", message="Uspešno ste odjavili svoje radno vreme.")
            odjava()
            sys.exit()

        else:
            messagebox.showerror(title="Greška", message="Nije pronađen nijedan zaposlen ili niste prijavljeni!")

btn1 = tkinter.Button(root, text="Odjava", fg="white", bg="green", command=proveriBarkod, font=font, padx=50, pady=2)
btn1.grid(row = 0, column = 2, padx=(20, 0), pady=(25, 0), sticky=tkinter.E)

def odjava():
    #upit
    zahtev = e1.get() + " " + flag
    s.sendall(zahtev.encode())
    # conn = sqlite3.connect("zaposleni.db")
    # cursor = conn.cursor()
    # name = bar_kod.get()
    # upit = f"""UPDATE zaposleni SET naPoslu = "Ne"  WHERE id = {name}
    #
    #                         """
    # cursor.execute(upit)
    # conn.commit()
    # conn.close()
    #odgovor


def poveziSe():
    s.connect((host, port))
    print("Povezan na: ", host)
mainThread = threading.Thread(target=poveziSe, args=()).start()



root.mainloop()
