########################
# Nikola Rilak NRT - 73/18
# Diplomski rad
# Softver za identifikovanje zaposlenih
########################

# Biblioteke
from tkinter import *
import sqlite3
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image, ImageFilter
import shutil
import sys
import random


# conn = sqlite3.connect("zaposleni.db")
# cursor = conn.cursor()
# conn.execute("""
#
# CREATE TABLE zaposleni(
#     id text,
#     ime text,
#     prezime text,
#     datumRodjenja text,
#     pozicija text,
#     radniSati integer,
#     sekunde integer,
#     naPoslu text,
#     start_time integer,
#     slika text
# )
#
# """)
# conn.close()

class SecondWindow():
    def __init__(self):
        super().__init__()
        self.putanja = ""
        self.id = random.randint(0, 12345678910)
        print(self.id)
        def dodajFotografiju():
            button = Button(labelFrame, text="Prilozi fotografiju", command=fileDialog)
            button.grid(column=5, row=1)

        def fileDialog():
            imefajla = filedialog.askopenfilename(initialdir="/", title="Select A File", filetype=
            (("jpeg files", "*.jpg"), ("all files", "*.*")))
            label = Label(labelFrame, text="")
            label.grid(row = 5, column = 2)

            global putanja
            putanja = imefajla

            img = (Image.open(putanja))
            smanjena_slika = img.resize((180, 180), Image.ANTIALIAS)
            nova_slika = ImageTk.PhotoImage(smanjena_slika)

            label2 = Label(image=nova_slika, width = 150, height = 245)
            label2.image = nova_slika
            label2.grid(row = 5, column = 1)

        def postaviSliku():
            label = Label(labelFrame, text="")
            label.grid(row=5, column=2)

            img = (Image.open("default/unknown.jpg"))
            smanjena_slika = img.resize((180, 180), Image.ANTIALIAS)
            nova_slika = ImageTk.PhotoImage(smanjena_slika)

            label2 = Label(image=nova_slika, width=150, height=245)
            label2.image = nova_slika
            label2.grid(row=5, column=1)

        def dodajZaposlenog():
            global broj
            global putanja
            id = e1.get()
            ime = e2.get()
            prezime = e3.get()
            datumRodjenja = e4.get()
            pozicija = e5.get()
            radniSati = 0
            naPoslu = "Ne"
            izvor_putanje = r""+putanja
            destinacija_putanje = r"C:\Users\Rile\PycharmProjects\Diplomski\zaposleni"+ "\\" +ime + "-" + prezime + ".jpg"
            shutil.copy(izvor_putanje, destinacija_putanje)
            conn = sqlite3.connect("zaposleni.db")
            sekunde = 0
            conn.execute("insert into Zaposleni (id, ime, prezime, datumRodjenja, pozicija, radniSati, sekunde, naPoslu, slika) values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                         (id, ime, prezime, datumRodjenja, pozicija, radniSati, sekunde, naPoslu, destinacija_putanje))
            print("Uspesno upisivanje u bazu.")
            conn.commit()
            conn.close()
            messagebox.showinfo(title=None, message="Uspesno ste dodali radnika!")
            e1.insert(0, "")


        def ugasiProgram():
            sys.exit()

        # def promeni():
        #     lb_var.set('Changed it!')
        #
        # promeni()

        # Kontrole
        idLabel = Label(root, text="ID zaposlenog", font=8, justify=LEFT)
        idLabel.grid(row=0, column=1, sticky=W)

        e1 = Entry(root, width=25)
        e1.grid(row=0, column=2, padx=(13, 0))
        e1.insert(0, self.id)

        # e1.configure(state=tk.DISABLED)


        imeLabel = Label(root, text="Ime zaposlenog", font=8, justify=LEFT)
        imeLabel.grid(row=1, column=1, sticky=W)

        e2 = Entry(root, width=25)
        e2.grid(row=1, column=2, padx=(13, 0))


        prezimeLabel = Label(root, text="Prezime zaposlenog", font=8, justify=LEFT)
        prezimeLabel.grid(row=2, column=1, sticky=W)

        e3 = Entry(root, width=25)
        e3.grid(row=2, column=2, padx=(13, 0))

        godinaLabel = Label(root, text="Datum rodjenja", font=8, justify=LEFT)
        godinaLabel.grid(row=3, column=1, sticky=W)

        e4 = Entry(root, width=25)
        e4.grid(row=3, column=2, padx=(13, 0))


        pozicijaLabel = Label(root, text="Pozicija zaposlenog", font=8, justify=LEFT)
        pozicijaLabel.grid(row=4, column=1, sticky=W)

        e5 = Entry(root, width=25)
        e5.grid(row=4, column=2, padx=(13, 0))
        #
        # labelPrazna = Label(root, height = 10)
        # labelPrazna.grid(row = 2, column = 2)

        labelFrame = LabelFrame(root, text = "Fotografija")
        labelFrame.grid(row = 5, column = 2,padx=(10, 0) )

        img = (Image.open("default/unknown.jpg"))
        resized_image = img.resize((180, 180), Image.ANTIALIAS)
        new_image = ImageTk.PhotoImage(resized_image)

        label2 = Label(image=new_image, width = 150, height = 245)
        label2.grid(row = 5, column = 1)

        for i in range(18):  # pravimo prazna mesta zbog relativnosti grid sistema
            prazanLabel = Label(root)
            prazanLabel.grid(row=i, column=3)

        nazad = Button(root, padx=50, text="Nazad", bg="red", fg="white", command=ugasiProgram)
        nazad.grid(row=7, column=1)

        dodajZaposlenog = Button(root, padx=50, text="Dodaj", bg="green", fg="white", command=dodajZaposlenog)
        dodajZaposlenog.grid(row=7, column=2)
        ###############
        # Funkcije
        postaviSliku()
        dodajFotografiju()


if __name__ == '__main__':
    root = Tk()
    SecondWindow()
    root.title("Dodavanje zaposlenog")
    root.geometry("360x450")
    root.eval('tk::PlaceWindow . center')
    root.resizable(False, False)
    root.mainloop()


