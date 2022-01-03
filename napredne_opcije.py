import tkinter as tk
from subprocess import call
import sqlite3
import datetime
import sys
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image, ImageFilter
class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.lblvar = tk.StringVar()
        self.rezultat = ""

        def pronadjiZaposlenog():
            if len(e2.get()) == 0: # Mala provera entry polja da ne bi doslo do provere praznog polja.
                messagebox.showerror(title="Greska", message="Niste uneli barcode!")
            elif len(e2.get()) > 1: # Ponovna provera da li je polje prazno.
                # Ocekivano je da nije, iz tog razloga funkcija nastavlja

                conn = sqlite3.connect("zaposleni.db") # Otvaranje konekcije sa bazom
                cursor = conn.cursor()
                bar_kod = e2.get()
                # Pravljenje upita
                upit = f"""
                                SELECT *
                                FROM zaposleni
                                WHERE id = '{bar_kod}'
                        """
                cursor.execute(upit)
                global rezultat
                rezultat = cursor.fetchall()


                if rezultat:
                    rezultatWindow()

                else:
                    messagebox.showerror(title="Greska", message="Nije pronadjen nijedan zaposlen pod tim ID-om!")

        def validacijaZaBrisanje():
            if len(e3.get()) == 0:
                messagebox.showerror(title="Greska", message="Niste uneli barcode!")
            elif len(e3.get()) > 1:
                conn = sqlite3.connect("zaposleni.db")
                cursor = conn.cursor()
                bar_kod = e3.get()
                upit = f"""
                                SELECT *
                                FROM zaposleni
                                WHERE id = '{bar_kod}'
                        """
                cursor.execute(upit)
                global rezultat
                rezultat = cursor.fetchall()
                if rezultat:
                    id = rezultat[0][0]
                    ime = rezultat[0][1]
                    prezime = rezultat[0][2]
                    datumRodjenja = rezultat[0][3]
                    pozicija = rezultat[0][4]
                    msg = messagebox.askquestion(title="Potvrda", message="Sledeci zaposleni ce biti izbrisan iz baze: \t\n\n"
                                                                 "ID: " + id + "\n" +
                                                                 "Ime: " + ime + "\n" +
                                                                 "Prezime: " + prezime + "\n" +
                                                                "Datum rodjenja " + datumRodjenja + "\n" +
                                                                "Pozicija: " + pozicija + "\n")
                    if msg == 'yes':
                        print("Uspesno")
                        upit = f"""
                                       DELETE FROM zaposleni
                                       WHERE id = {id}
                               """
                        cursor.execute(upit)
                        conn.commit()
                        messagebox.showinfo("Uspesno brisanje!", message=id + " je izbrisan!")


                else:
                    messagebox.showerror(title="Greska", message="Nije pronadjen nijedan zaposlen pod tim ID-om!")

        def ugasiProgram():
            sys.exit()

        def dodajZaposlene():
            call(["python", "dodaj_zaposlenog.py"])

        def prikaziRezultat():
            call(["python", "prikaz.py"])

        for i in range(19):  # pravimo prazna mesta zbog relativnosti grid sistema
            prazanLabel = tk.Label(self)
            prazanLabel.grid(row=i, column=1)

        label1 = tk.Label(self, fg="white", bg="navy", width=70, font="15", height=2)
        label1.grid(row=0, column=0, sticky=tk.W)

        praznaLabel = tk.Label(self) # pravimo prazna mesta zbog relativnosti grid sistema
        praznaLabel.grid(row=1, column=0)

        label2 = tk.Label(self, textvariable=self.lblvar, font="10")
        label2.grid(row=2, column=0, sticky=tk.W, padx=(7, 0))

        label3 = tk.Label(self, font="10", text="Dodavanje novog zaposlenog")
        label3.grid(row = 2, column = 0, sticky=tk.W, padx=(5, 50))

        dodajZaposlenogButton = tk.Button(self, padx=15, width="17", text="Dodaj zaposlenog", bg="green", fg="white", command=dodajZaposlene)
        dodajZaposlenogButton.grid(row=2, column=0, padx=(80, 50))

        label4 = tk.Label(self, font="10", text="Spisak zaposlenih radnika")
        label4.grid(row=4, column=0, sticky=tk.W, padx=(5, 50))

        pogledajSveZaposlene = tk.Button(self, padx=15, width="17", text="Pogledaj sve zaposlene", bg="green", fg="white",
                                          command=prikaziRezultat)
        pogledajSveZaposlene.grid(row=4, column=0, padx=(80, 50))

        e3 = tk.Entry(self, width=38)
        e3.grid(row=6, column=0, sticky=tk.W, padx=(10, 50))

        izbrisiZaposlenog = tk.Button(self, padx=15, width="17", text="Izbrisi zaposlenog", bg="green",
                                         fg="white", command=validacijaZaBrisanje)
        izbrisiZaposlenog.grid(row=6, column=0, padx=(80, 50))

        label6 = tk.Label(self, text="* Brisanje se vrsi po barcodu")
        label6.grid(row=7, column=0, sticky=tk.W, padx=(10, 50))

        e2 = tk.Entry(self, width=38)
        e2.grid(row=8, column=0, padx=(10, 50), sticky=tk.W)

        label6 = tk.Label(self, text="* Pretraga se vrsi po barcodu")
        label6.grid(row=9, column=0, sticky=tk.W, padx=(10, 50))

        pronadjiZaposlenog = tk.Button(self, padx=15, width="17", text="Pronadji zaposlenog", bg="green",
                                      fg="white", command=pronadjiZaposlenog)
        pronadjiZaposlenog.grid(row=8, column=0, padx=(80, 50))

        nazad = tk.Button(self, padx=50, text="Izadji", bg="red", fg="white", command=ugasiProgram, font="10")
        nazad.grid(row=14, column=0, sticky=tk.W, padx=(10, 0))

        w = 500  # width for the Tk root
        h = 400  # height for the Tk root

        # get screen width and height
        ws = self.winfo_screenwidth()  # width of the screen
        hs = self.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        # set the dimensions of the screen
        # and where it is placed
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.title("Sistem za identifikaciju zaposlenih")
        self.eval('tk::PlaceWindow . center')
        self.resizable(False, False)

def rezultatWindow():
    global rezultat

    id = rezultat[0][0]
    ime = rezultat[0][1]
    prezime = rezultat[0][2]
    datumRodjenja = rezultat[0][3]
    pozicija = rezultat[0][4]
    radniSati = rezultat[0][5]
    naPoslu = rezultat[0][7]
    slika = rezultat[0][9]

    master = tk.Toplevel()
    master.title("Rezultat")
    master.geometry("360x450")
    master.resizable(False, False)

    idLabel = tk.Label(master, text="ID zaposlenog", font=8, justify=tk.LEFT)
    idLabel.grid(row=0, column=1, sticky=tk.W)
    #
    e1 = tk.Entry(master, width=25)
    e1.grid(row=0, column=2, padx=(13, 0))
    e1.insert(0, id)
    e1.configure(state=tk.DISABLED)

    #
    imeLabel = tk.Label(master, text="Ime zaposlenog", font=8, justify=tk.LEFT)
    imeLabel.grid(row=1, column=1, sticky=tk.W)
    #
    e2 = tk.Entry(master, width=25)
    e2.grid(row=1, column=2, padx=(13, 0))
    e2.insert(0, ime)
    #
    prezimeLabel = tk.Label(master, text="Prezime zaposlenog", font=8, justify=tk.LEFT)
    prezimeLabel.grid(row=2, column=1, sticky=tk.W)
    #
    e3 = tk.Entry(master, width=25)
    e3.grid(row=2, column=2, padx=(13, 0))
    e3.insert(0, prezime)
    #
    godinaLabel = tk.Label(master, text="Datum rodjenja", font=8, justify=tk.LEFT)
    godinaLabel.grid(row=3, column=1, sticky=tk.W)
    #
    e4 = tk.Entry(master, width=25)
    e4.grid(row=3, column=2, padx=(13, 0))
    e4.insert(0, datumRodjenja)
    #
    pozicijaLabel = tk.Label(master, text="Pozicija zaposlenog", font=8, justify=tk.LEFT)
    pozicijaLabel.grid(row=4, column=1, sticky=tk.W)
    #
    e5 = tk.Entry(master, width=25)
    e5.grid(row=4, column=2, padx=(13, 0))
    e5.insert(0, pozicija)

    radniSatiLabel = tk.Label(master, text="Radni sati", font=8, justify=tk.LEFT)
    radniSatiLabel.grid(row=5, column=1, sticky=tk.W)
    #
    e6 = tk.Entry(master, width=25)
    e6.grid(row=5, column=2, padx=(13, 0))
    e6.insert(0, radniSati)

    naPosluLabel = tk.Label(master, text="Na poslu:", font=8, justify=tk.LEFT)
    naPosluLabel.grid(row=6, column=1, sticky=tk.W)
    #
    e7 = tk.Entry(master, width=25)
    e7.grid(row=6, column=2, padx=(13, 0))
    e7.insert(0, naPoslu)
    #
    # labelPrazna = tk.Label(master, height=10)
    # labelPrazna.grid(row = 5, column = 2)
    #
    label = tk.Label(master, text="")
    label.grid(row=7, column=2)

    img = (Image.open("" + slika))
    smanjena_slika = img.resize((180, 180), Image.ANTIALIAS)
    nova_slika = ImageTk.PhotoImage(smanjena_slika)

    label2 = tk.Label(master, image=nova_slika, width=150, height=245)
    label2.image = nova_slika
    label2.grid(row=7, column=1)

if __name__ == "__main__":
    MainWindow().mainloop()
