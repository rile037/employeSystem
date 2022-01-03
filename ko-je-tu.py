import sqlite3
import tkinter as tk
from tkinter import messagebox
import random
from PIL import ImageTk, Image, ImageFilter

class DynamicGrid(tk.Frame):# U ovom slucaju smo koristili klasu zbog lakse dinamike prikazivanja podataka

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        frame = tk.Frame(self, width=300, height=300) # objekat frame koji vec kao roditelja tkinter root prozor

        frame.pack(expand=True, fill=tk.BOTH)  # .grid(row=0,column=0)
        canvas = tk.Canvas(frame, bg='#FFFFFF', width=300, height=300, scrollregion=(0, 0, 500, 500))
        hbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        hbar.pack(side=tk.BOTTOM, fill=tk.X) # dodajemo scrollbar
        hbar.config(command=canvas.xview)
        # vbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        # vbar.pack(side=tk.RIGHT, fill=tk.Y)
        # vbar.config(command=canvas.yview)
        canvas.config(width=300, height=300)
        canvas.config(xscrollcommand=hbar.set)
        canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.text = tk.Text(canvas, wrap="char", borderwidth=0, highlightthickness=0,
                            state="disabled", cursor="arrow")

        self.text.pack(fill="both", expand=True)
        self.boxes = []



    def add_box(self, color=None): # funkcija pravljenje frejma odnosno “kutije”

        conn = sqlite3.connect("zaposleni.db")
        cursor = conn.cursor()

        upit = f"""
                          SELECT * 
                          FROM zaposleni
                  """

        cursor.execute(upit)
        rezultat = cursor.fetchall()
        conn.close()

        for i in rezultat:
            box = tk.Frame(self.text, bd=1, relief="sunken",
                           width=25, height=25)
            bar_kod = f"{i[0]}"
            naPoslu = f"{i[7]}"
            slika = f"{i[9]}"

            img = (Image.open("" + slika))
            if("Ne" in naPoslu):
                resized_image = img.resize((150, 150), Image.ANTIALIAS).convert('L')
            else:
                resized_image = img.resize((150, 150), Image.ANTIALIAS)
            new_image = ImageTk.PhotoImage(resized_image)
            label2 = tk.Label(box, image=new_image)
            label2.image = new_image
            label2.grid()

            btn = tk.Button(box, text=bar_kod, cursor="hand2")
            btn.grid()
            self.boxes.append(box)
            self.text.configure(state="normal")
            self.text.window_create("end", window=box)
            self.text.configure(state="disabled")



class Example(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ko je prisutan?")
        self.dg = DynamicGrid(self.root, width=500, height=200)
        self.dg.pack(side="top", fill="both", expand=True)

        # add a few boxes to start

    def start(self):
        self.dg.add_box()
        self.root.mainloop()

Example().start()
