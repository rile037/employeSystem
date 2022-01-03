import tkinter
import sqlite3
from tkinter import messagebox
from subprocess import call
import subprocess
import sys
import socket
import threading
from pygame import *


host = "127.0.0.1" #koristimo ip adresu lokalnog hosta
port = 12345 #uzimamo port 12345 pod pretpostavkom da je otvoren
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



root = tkinter.Tk()
root.title("Prijava")
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
flag = "PRIJAVA"
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
                        WHERE id = '{bar_kod}' AND naPoslu = 'Ne'
                """
        cursor.execute(upit)
        rezultat = cursor.fetchall()
        conn.close()
        if rezultat:
            # mixer.init()
            # mixer.music.load("audio/prijavljen.ogg")
            # mixer.music.play()
            messagebox.showinfo(title="Uspešna prijava", message="Uspešno ste se prijavili za svoje radno vreme.")
            prijava()

            sys.exit()

        else:
            messagebox.showerror(title="Greška", message="Nije pronađen nijedan zaposlen ili ste već prijavljeni!")

btn1 = tkinter.Button(root, text="Prijava", fg="white", bg="green", command=proveriBarkod, font=font, padx=50, pady=2)
btn1.grid(row = 0, column = 2, padx=(20, 0), pady=(25, 0), sticky=tkinter.E)


def prijava():  # Saljemo podatke server sa flagom “PRIJAVA” kako bi server znao da se klijent prijavljuje
    # upit
    radniSati = "START"
    zahtev = e1.get() + " " + flag + " " + radniSati
    s.sendall(zahtev.encode())
# FORMAT ---- > 11/11/2021 - 22:03:36: zaposleni 6449716892 se PRIJAVIO.


def poveziSe(): #funkcija za povezivanje na server
    s.connect((host, port)) # kreiramo objekat s u koji smestamo dve glavne stavke,
    # prva  oznacava ipv4 adresu dok druga oznacava da je u pitanju tcp protokol
    print("Povezan na: ", host)
mainThread = threading.Thread(target=poveziSe, args=()).start() #smestanje funkcije u nit

root.mainloop()
