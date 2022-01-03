import tkinter as tk
import tkinter
import datetime
from subprocess import call
import sqlite3
from tkinter import filedialog, messagebox, END
from PIL import ImageTk, Image, ImageFilter
import shutil
import sys
import random
import socket
import threading
import time

brojZaposlenih = ""

root = tk.Tk()  # root objekat u koji smestamo glavni prozor tkinter biblioteke

root.geometry("1300x400")  # geometrija

root.title("Softver za identifikaciju zaposlenih")
root.resizable(False, False)  # postavljamo mogucnost sirenja prozora na false


def verzijaPrograma():  # mala funkcija za prikaz verzije programa ugradjena u glavni meni prozora
    messagebox.showinfo(title="Verzija", message="v0.1")

    main_menu = tk.Menu(root)
    root.config(menu=main_menu)
    main_menu.add_command(label='Verzija programa', command=verzijaPrograma)

    root.var = tk.StringVar()  # promenljiva u kojoj se smesta vrednost labele za prikaz broja zaposlenih


def vratiBrojZaposlenih():
    global brojZaposlenih
    conn = sqlite3.connect('zaposleni.db')
    cursor = conn.cursor()
    rezultat = cursor.execute("select count(*) from zaposleni")  # vraca rezultat
    rows = cursor.fetchall()[0]
    rowsCut = str(rows).split("(", 1)  # kratimo string pre broja
    preString = rowsCut[1]
    posleString = preString.split(",", 1)  # kratimo string posle broja
    brojZaposlenih = posleString[0]  # rezultat kao ceo broj

    conn.close()
    root.var.set("Broj zaposlenih u bazi: " + brojZaposlenih)

def proveriPrisutnost():
    call(["python", "prisutni.py"])

def koJeTu():
    call(["python", "ko-je-tu.py"])
def promeniVreme():
    trenutnoVreme = datetime.datetime.now().strftime("%d" + "/" + "%m" + "/" + "%Y - %H:%M:%S")
    label1['text'] = trenutnoVreme
    label1.after(1, promeniVreme)

def ugasiProgram():
    sys.exit()


def napredneOpcije():
    call(["python", "napredne_opcije.py"])

root.var = tk.StringVar() # promenljiva u kojoj se smesta vrednost labele za prikaz broja zaposlenih

#kontrole
label1 = tk.Label(root, text="Vreme", fg="white", bg="navy", width=70, font="15", height=2)
label1.grid(row=0, column=0, sticky=tkinter.N)

label2 = tk.Label(root,textvariable=root.var, font="10")
label2.grid(row=0, column=0, sticky=tkinter.NW, pady=70, padx=(20, 0))

koJePrisutan = tk.Button(root, padx=15, width="15", text="Proveri prisutnost", bg="blue", fg="white", command=koJeTu, font="2")
koJePrisutan.grid(row=0, column=0, sticky=tkinter.NE, pady=70, padx=(0, 20))

nazad = tk.Button(root, padx=50, text="Izadji", bg="red", fg="white", command=ugasiProgram, font="10")
nazad.grid(row=0, column=0, sticky=tk.NW, pady=(350, 0), padx=(20, 0))

napredneOpcijeDugme = tk.Button(root, padx=15, text="Napredne opcije", bg="green", fg="white", command=napredneOpcije, justify=tk.LEFT, anchor="w", font="10")
napredneOpcijeDugme.grid(row=0, column=0, sticky=tkinter.NE, pady=(350, 0), padx=(0, 20))

text1 = tkinter.Text(root, width="70")
text1.grid(row=0, column=1)

promeniVreme()
vratiBrojZaposlenih()


local_pc = "" # ip adresu odnosno host postavljamo na prazno zato sto server sam uzima svoju ip adresu
port = 12345 # uzimamo port 12345 pod pretpostavkom da je slobodan

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # kreiramo objekat s u koji smestamo dve glavne stavke,
# prva oznacava ipv4 adresu dok druga oznacava da je u pitanju tcp protokol

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # postavljamo mogucnost ponovnog koriscenja iste adrese

def slusajKonekcije(): # funkcija za slusanje svih konekcija, koja se kasnije smesta u nit
    s.bind((local_pc, port)) #  postavljanje prethodno definisane ip adrese I porta u nas objekat odnosno socket
    s.listen() # postavljamo objekat u stanje slusanja novih konekcija
    connection = sqlite3.connect("zaposleni.db") #  povezivanje sa bazom podataka
    cursor = connection.cursor() #  pravljenje objekta uz pomoc kojeg rukovodimo bazom
    print("Slusam...")
    global start_time
    while True: #  petlja koja regulise uspesno povezivanje klijenta
        conn, addr = s.accept() # dva najvaznija objekta uz pomocu kojih mozemo da vidimo sadrzaj poruke
        # i adresu sa koje je poslata poruka

        print("Nadolazeca konekcija: ", addr)
        try:
            while True:
                data = conn.recv(1024) #  objekat koji sadrzi primljenu poruku sa baferom velicine 1024 bajta
                zahtev = data.decode()

                if("PRIJAVA" in zahtev): # pravimo upite da bi razgranicili sta je prijava a sta odjava u poruci
                    trenutnoVreme = datetime.datetime.now().strftime("%d" + "/" + "%m" + "/" + "%Y - %H:%M:%S")
                    name = zahtev.split(" ")[0]
                    text1.insert(END, trenutnoVreme + ": zaposleni " + name + " se PRIJAVIO. \n")

                    f = open("log.txt", "a")
                    f.write(trenutnoVreme + ": zaposleni " + name + " se PRIJAVIO. \n")
                    f.close()
                    start_time = time.time()
                    start_time_baza = (int(start_time))
                    # upit = f"""UPDATE zaposleni
                    #            SET naPoslu = 'Da'
                    #            SET start_time = {start_time_baza}
                    #            WHERE id = {name}
                    #
                    # """
                    cursor.execute("UPDATE zaposleni SET naPoslu=?, start_time=? WHERE id=? ",
                                   ('Da', start_time_baza, name))

                    connection.commit()

                if("ODJAVA" in zahtev):
                    trenutnoVreme = datetime.datetime.now().strftime("%d" + "/" + "%m" + "/" + "%Y - %H:%M:%S")
                    name = zahtev.split(" ")[0]
                    text1.insert(END, trenutnoVreme + ": zaposleni " + name + " se ODJAVIO. \n")

                    upit1 = f"""
                                SELECT sekunde
                                FROM zaposleni
                                WHERE id={name}
                                                                                                    """

                    cursor.execute(upit1)
                    sekunde = cursor.fetchall()[0]
                    rowsCut1 = str(sekunde).split('(', 1)  # kratimo string pre broja
                    preString1 = rowsCut1[1]
                    posleString1 = preString1.split(",", 1)  # kratimo string posle broja
                    brojSekundi = posleString1[0]  # rezultat kao ceo broj
                    print(brojSekundi)

                    upit2 = f"""
                                                    SELECT start_time
                                                    FROM zaposleni
                                                    WHERE id={name}
                                                                                                                        """

                    cursor.execute(upit2)
                    start = cursor.fetchall()[0]
                    row = str(start).split('(', 1)  # kratimo string pre broja
                    pre = row[1]
                    posle = pre.split(",", 1)  # kratimo string posle broja
                    broj_start = posle[0]  # rezultat kao ceo broj

                    f = open("log.txt", "a")
                    f.write(trenutnoVreme + ": zaposleni " + name + " se ODJAVIO. \n")
                    f.close()
                    e = int(time.time() - float(broj_start))
                    print(e)
                    e2 = int(brojSekundi)
                    e3 = e + e2
                    print(e3)
                    hour = ('{:02d}:{:02d}'.format(e3 // 3600, (e3 % 3600 // 60)))
                    print(hour)
                    cursor.execute("UPDATE zaposleni SET naPoslu=?, radniSati=?, sekunde=? WHERE id=? ", ('Ne', hour, e3, name))
                    connection.commit()
                break
        except:
            print("---")

tk1 = threading.Thread(target=slusajKonekcije, args=()).start()
# Stavljanje funkcije pod nit da bi mogla uvek da prima konekcije, bez obzira da li se dešavaju neke radnje ili ne

t2 = threading.Thread(target=root.mainloop(), args="").start()