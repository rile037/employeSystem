import sqlite3
import tkinter
from PIL import ImageTk, Image, ImageFilter


def roll(): pass
def links(): pass
def create(): pass
root=tkinter.Tk() # objekat u koji smestamo glavni prozor tkinter biblioteke
root.title("Svi zaposleni")
root.geometry("475x520")
rows = 0

def azuriraj_scroll (event):
    photoCanvas.configure(scrollregion=photoCanvas.bbox("all")) # funkcija za azuriranje pozicije scrollbara

photoFrame = tkinter.Frame(root, bg="#EBEBEB", width="500", height="400")
photoFrame.grid()
photoFrame.rowconfigure(0, weight=1)
photoFrame.columnconfigure(0, weight=1)
# pravimo frejm I kanvas u koji smestamo taj frejm

photoCanvas = tkinter.Canvas(photoFrame, bg="#EBEBEB", height="500", width="450")
photoCanvas.grid(row=0, column=0, sticky="nsew")

canvasFrame = tkinter.Frame(photoCanvas, bg="#EBEBEB", width="500")
photoCanvas.create_window(0, 0, window=canvasFrame, anchor='nw')

def kreiraj_detaljan_frejm():  # funkcija za pravljenje frejma u koji se kasnije smestaju svi podaci zaposlenih

    conn = sqlite3.connect("zaposleni.db") # povezivanje sa bazom podataka
    cursor = conn.cursor() # pravimo objekat u koji smestamo kursor uz pomocu kojeg radimo upite

    global rows
    # pravimo upit na osnovu kojeg uzimamo samo korisnike koji su na poslu trenutno
    upit = f""" 
                   SELECT * 
                   FROM zaposleni
           """

    cursor.execute(upit) # izvrsavamo upit
    rezultat = cursor.fetchall()
    conn.close()


    for i in rezultat:
        step = tkinter.LabelFrame(canvasFrame,text="Detalji:", width="400")
        step.grid(row=rows, columnspan=7, sticky='W',padx=5, pady=5, ipadx=5, ipady=5)
        tkinter.Label(step,text="ID",font = "Arial 8 bold").grid(row=0,sticky='E', padx=5, pady=2)
        tkinter.Label(step,text="Ime",font = "Arial 8 bold").grid(row=1,sticky='E', padx=5, pady=2)
        tkinter.Label(step,text="Prezime",font = "Arial 8 bold").grid(row=2,sticky='E', padx=5, pady=2)
        tkinter.Label(step, text="Datum rodjenja", font="Arial 8 bold").grid(row=3, sticky='E', padx=5, pady=2)
        tkinter.Label(step, text="Pozicija", font="Arial 8 bold").grid(row=4, sticky='E', padx=5, pady=2)
        tkinter.Label(step, text="Radni satii", font="Arial 8 bold").grid(row=5, sticky='E', padx=5, pady=2)
        tkinter.Label(step, text="Na poslu", font="Arial 8 bold").grid(row=6, sticky='E', padx=5, pady=2)
        for x in range(13):
            tkinter.Label(step, text="", font="Arial 8 bold italic").grid(row=5, column=x, sticky='E', padx=5,pady=2)
        # img = (Image.open("default/unknown.jpg"))
        # resized_image = img.resize((50, 50), Image.ANTIALIAS)
        # new_image = ImageTk.PhotoImage(resized_image)
        # tkinter.Label(step, image=new_image, text="Fotografija", font="Arial 8 bold italic").grid(row=2, column=9, sticky='E', padx=5, pady=2)
        canvas = tkinter.Canvas(step, bg="red", height="100", width="100")
        canvas.grid(row=9, column=3, sticky='E', padx=0, pady=0)
        slika = f"{i[9]}"
        img = (Image.open("" + slika))
        resized_image = img.resize((150, 150), Image.ANTIALIAS)
        new_image = ImageTk.PhotoImage(resized_image)
        label2 = tkinter.Label(canvas, image=new_image)
        label2.image = new_image
        label2.grid()

        e1 = tkinter.Entry(step)
        e2 = tkinter.Entry(step)
        e3 = tkinter.Entry(step)
        e4 = tkinter.Entry(step)
        e5 = tkinter.Entry(step)
        e6 = tkinter.Entry(step)
        e7 = tkinter.Entry(step)
        e1.insert(0, f"{i[0]}")
        e2.insert(0, f"{i[1]}")
        e3.insert(0, f"{i[2]}")
        e4.insert(0, f"{i[3]}")
        e5.insert(0, f"{i[4]}")
        e6.insert(0, f"{i[5]}")
        e7.insert(0, f"{i[7]}")

        e1.grid(row=0,column=1,columnspan=7, sticky="WE")
        e2.grid(row=1,column=1,columnspan=7, sticky="WE")
        e3.grid(row=2,column=1,columnspan=7, sticky="WE")
        e4.grid(row=3, column=1, columnspan=7, sticky="WE")
        e5.grid(row=4, column=1, columnspan=7, sticky="WE")
        e6.grid(row=5, column=1, columnspan=7, sticky="WE")
        e7.grid(row=6, column=1, columnspan=7, sticky="WE")
        # tkinter.Button(step,text ="Search Words",width=10,font = "Arial 8 bold    italic",activebackground="red",command=roll).grid(row=3,column=0,sticky=tkinter.W,pady=4,padx=5)
        # tkinter.Button(step,text="Google Search",width=10,font = "Arial 8 bold italic",command=links).grid(row=3,column=2,sticky=tkinter.W,pady=4,padx=5)
        # tkinter.Button(step,text="Extraxt Text",width=10,font = "Arial 8 bold italic",command = create).grid(row=3,column=4,sticky=tkinter.W,pady=4,padx=5)
        rows += 1

photoScroll = tkinter.Scrollbar(photoFrame, orient=tkinter.VERTICAL)
photoScroll.config(command=photoCanvas.yview)
photoCanvas.config(yscrollcommand=photoScroll.set)
photoScroll.grid(row=0, column=1, sticky="ns")
canvasFrame.bind("<Configure>", azuriraj_scroll)

kreiraj_detaljan_frejm()

root.mainloop()