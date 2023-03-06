import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import serial
import datetime
import mysql.connector
import weather
from mysql.connector import Error

# Initierar värden och hämtar från tiden.
searchString='init value'
todays_date=datetime.date.today()
weather_temp=weather.current_temperature
date_string=todays_date.strftime('%Y-%m-%d')

# Hämtar väderstatusen från API och översätter till svenska
if weather.weather_status == "Clear":
    weather_status="Klart"
if weather.weather_status == "Clouds":
    weather_status="Moln"
if weather.weather_status == "Rain":
    weather_status="Regn"
if weather.weather_status == "Snow":
    weather_status="Snö"

# Initieraring av värden, flagga används för att ha koll på vilken knapp man tryckt på första skärmen
flagga=0
product_weight=0
product_name="testy"
read_success = 0

# Background color dark-green
bg_color="#3d6466"


# Initierar seriell uppkoppling till vågen
ser=serial.Serial(
     port='/dev/ttyUSB0',
     baudrate=9600,
     parity=serial.PARITY_NONE,
     stopbits=serial.STOPBITS_ONE,
     bytesize=serial.EIGHTBITS,
     timeout=None)

# Skapa en funktion som skickar en signal till vågen som läser nuvarande vikt från våg
def serial_write ():
    ser.write(b's')


# Skapa en funktion som läser in en rad från vågen och sparar den i en variabel
def serial_read ():
    x=ser.readline()
    return x


# Skapa en funktion som upprättar en koppling till databasen samt som kallas på när man ska spara värde till databasen
def write_to_database (
        datum=todays_date,
        temperature=weather_temp,
        weather_status=weather_status):
    print(datum)
    print(temperature)
    print(weather_status)
    try:
        connection=mysql.connector.connect(host='172.20.10.3',
                                           database='products',
                                           user='user0',
                                           password='hejsan00')
        cursor=connection.cursor()

        name=product_name
        weight=product_weight

        # Query skriven i SQL som skapar en ny tabell för produkten som matas in om den ej existerar
        mySql_insert_query="""CREATE TABLE IF NOT EXISTS """ + name + """( 
                                    date DATE NOT NULL,
                                    amount FLOAT NOT NULL,
                                    PRIMARY KEY(date, amount)
                                    );"""
       # Query skriven i SQL som matar in datum samt vägt värde till tabell för produkten
        mySql_insert_query2="""
                                INSERT INTO """ + name + """(date, amount) 
                                   VALUES (%s, %s); """
        # Query skriven i SQL som matar in vädret i databasen, ignorerar nya inmatningen om den redan är gjort på det datumet
        mySql_insert_query3="""
                                INSERT IGNORE INTO Väder(Datum, Temperatur, Väder_Status)
                                    VALUES (%s,%s,%s);"""

        value2=(date_string, weight)
        value3=(date_string, temperature, weather_status)
        cursor.execute(mySql_insert_query)
        cursor.execute(mySql_insert_query2, value2)
        cursor.execute(mySql_insert_query3, value3)

        connection.commit()
        tk.messagebox.showinfo("Success!","Värdet sparat i databasen!")


    except mysql.connector.Error as error:
        tk.messagebox.showinfo("Fel","Kunde ej spara värdet i databasen {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


# Skapa en funktion som tar in en sökning från tangentbordet och returnerar alla objekt från databasen i den tabellen
def read_from_database ():
    try:
        connection=mysql.connector.connect(host='172.20.10.3',
                                           database='products',
                                           user='user0',
                                           password='hejsan00')
        cursor=connection.cursor()

        name=product_name

        # Query skriven i SQL Som visar insparade vikten samt vädret för de datumen det finns sparade värden
        mySql_get_query="""SELECT """ + name + """.date, """ + name + """.amount,
         väder.temperatur, väder.väder_status 
        FROM """ + name + \
        """JOIN väder ON väder.datum = """  + name + """.date;"""

        cursor.execute(mySql_get_query)
        entries=cursor.fetchall()

        print("Record read successfully from " + product_name + " table")
        #Sätter flaggan så rätt Frame visas om lyckad vägning
        global read_success
        read_success = 1
        connection.commit()


    except mysql.connector.Error as error:
        print("Kunde inte läsa värdet från databasen {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            return entries


# Skapa en funktion som rensar skärmen för att förbereda inför nästa Frame
def clear_widgets ():
    for frame in (main, search, scale, stats):
        # Select all frame widgets and delete them
        for widget in frame.winfo_children():
            widget.destroy()


# Dödar applikationen
def close ():
    root.destroy()
    root.quit()


# Skapa en funktion som kallas på när man trycker på "ny sökning" på hemskärmen, sätter flaggan till 1 och laddar sökskärmen
def ny_sökning ():
    global flagga
    flagga=1
    load_search()


# Skapa en funktion som kallas på när man trycker på "se statistik" på hemskärmen, sätter flaggan till 0 och laddar sökskärmen

def se_statistik ():
    global flagga
    flagga=0
    load_search()


# Ladda start-sidan
def load_main ():
    clear_widgets()
    # Stacka mainframen längst fram
    main.tkraise()
    # Hindra widgets från att ändra storleken på applikationen
    main.pack_propagate(False)

    # Skapa en label för rubrik på sidan
    tk.Label(
        main,
        text="Smart Scale",
        bg=bg_color,
        fg="white",
        font=("Ubuntu",30)
    ).pack(pady=20)

    # Skapa en button som leder till vägnings-skärmen
    tk.Button(
        main,
        text="Väg produkt",
        width=50,
        height=9,
        command=lambda:ny_sökning()
    ).pack(pady=20)

    # Skapa en button som kallar på close funktionen
    tk.Button(main, text="Kill App", command=close).grid(row=0, column=1, columnspan=5, padx=5, pady=5)

    # Skapa en button som leder till statistik-skärmen
    tk.Button(
        main,
        text="Tidigare vägningar",
        width=50,
        height=9,
        command=lambda:se_statistik()
    ).pack(pady=20)


# Skapa en frame för inmatning av strängar
def load_search (searchString=searchString):
    clear_widgets()
    search.tkraise()
    main.pack_propagate(False)

    # Rubrik label
    tk.Label(
        search,
        text="Sök efter önskad produkt",
        bg=bg_color,
        fg="white",
        font=("Ubuntu", 20)
    ).grid(row=0, column=1, columnspan=15)

    # Button widget som leder till föregående skärm
    tk.Button(
        search,
        text="BACK",
        font=("Ubuntu", 18),
        bg="#28393a",
        fg="black",
        command=lambda:load_main()
    ).grid(row=0, column=0)

    # Skapa en button som kallar på close funktionen
    tk.Button(search, text="Kill App", command=close).grid(row=1, column=0)

    # Skapar en textbox som visar inmatning
    textArea=tk.Text(search,
                     height=2,
                     width=20,
                     font=("Ubuntu",30)
                     )
    textArea.grid(row=1, column=1, columnspan=15,pady=5)

    # Funktion som styr logiken bakom det egenskapade tangentbordet
    def select (value, textArea=textArea, searchString=searchString):
        # Kolla om inmatningsvärdet är "space"
        if value == 'Space':
            textArea.insert(INSERT, ' ')
        # Ladda nästa skärm utefter vad flaggan blev satt till i tidigare funktioner
        elif value == 'Enter':
            global product_name
            product_name=load_search.searchString
            print("product name: " + product_name)
            print("Search string: " + load_search.searchString)
            if flagga:
                load_scale()
            elif not flagga:
                load_stats()
        # Ta bort senaste inmatade tecknet
        elif value == '←':
            i=textArea.get(1.0, END)
            j=i[ :-2 ]
            textArea.delete(1.0, END)
            textArea.insert(INSERT, j)
        # Aktivera CAPS LOCK och byter till stora bokstäver på tangentbordet
        elif value == 'Caps':
            capsButtons=[ 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'Å', '←',
                          'CAPS', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ö', 'Ä', 'Enter',
                          '', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '_',
                          'Space' ]

            varRow=2
            varColumn=1
            # Logik för visande av tangentbord på skärm
            for button in capsButtons:
                command=lambda x=button:select(x)
                if button != 'Enter' and button != 'Space' and button != '':
                    tk.Button(search, text=button, width=2, height=4, command=command).grid(row=varRow,
                                                                                            column=varColumn)
                if button == 'Space':
                    tk.Button(search, text=button, width=50, height=4, command=command).grid(row=5, column=1,
                                                                                             columnspan=25)
                if button == 'Enter':
                    tk.Button(search, text=button, width=3, height=5, command=command).grid(row=3, column=12)
                if button == '':
                    tk.Button(search)

                varColumn+=1
                if varRow == 2 and varColumn > 12:
                    varColumn=0
                    varRow+=1
                elif varRow == 3 and varColumn > 12:
                    varColumn=1
                    varRow+=1
                elif varRow == 4 and varColumn > 11:
                    varColumn=1
                    varRow+=1

        # Ändra från stora till små bokstäver
        elif value == 'CAPS':
            varRow=2
            varColumn=1

            buttons=[ 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'å', '←',
                      'Caps', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ö', 'ä', 'Enter',
                      '', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '_',
                      'Space' ]

            for button in buttons:
                command=lambda x=button:select(x)
                if button != 'Enter' and button != 'Space' and button != '':
                    tk.Button(search, text=button, width=2, height=4, command=command).grid(row=varRow,
                                                                                            column=varColumn)
                if button == 'Space':
                    tk.Button(search, text=button, width=50, height=4, command=command).grid(row=5, column=1,
                                                                                             columnspan=25)
                if button == 'Enter':
                    tk.Button(search, text=button, width=3, height=5, command=command).grid(row=3, column=12)
                if button == '':
                    tk.Button(search)

                varColumn+=1
                if varRow == 2 and varColumn > 12:
                    varColumn=0
                    varRow+=1
                elif varRow == 3 and varColumn > 12:
                    varColumn=1
                    varRow+=1
                elif varRow == 4 and varColumn > 11:
                    varColumn=1
                    varRow+=1

        # Spara inmatad knapp till söksträng
        else:
            textArea.insert(INSERT, value)
            load_search.searchString=textArea.get(1.0, END)

    varRow=2
    varColumn=1

    buttons=[ 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'å', '←',
              'Caps', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ö', 'ä', 'Enter',
              '', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '_',
              'Space' ]
    # Logik för att visa tangentbord på skärm
    for button in buttons:
        command=lambda x=button:select(x)
        if button != 'Enter' and button != 'Space' and button != '':
            tk.Button(search, text=button, width=2, height=4, command=command).grid(row=varRow, column=varColumn)
        if button == 'Space':
            tk.Button(search, text=button, width=50, height=4, command=command).grid(row=5, column=1, columnspan=25)
        if button == 'Enter':
            tk.Button(search, text=button, width=3, height=5, command=command).grid(row=3, column=12)
        if button == '':
            tk.Button(search)

        varColumn+=1
        if varRow == 2 and varColumn > 12:
            varColumn=0
            varRow+=1
        elif varRow == 3 and varColumn > 12:
            varColumn=1
            varRow+=1
        elif varRow == 4 and varColumn > 11:
            varColumn=1
            varRow+=1


# Ladda frame där man väger produkten
def load_scale ():
    clear_widgets()
    scale.tkraise()
    scale.pack_propagate(False)
    output=None
    global product_weight

    # Skapa en knapp som dödar applikationen
    tk.Button(scale, text="Kill App", command=close).grid(row=0, column=2, pady=2, padx=2)

    # Skapa en knapp som tar en tillbaka till föregående frame
    tk.Button(scale, text="BACK", command=lambda:load_search()).grid(row=0, column=0)

    def update_vvalue():
        vvalue.set(serial_read())
        root.after(2000, update_vvalue())

    # Funktion för att skicka signal till våg och läsa returnerade svar vid vägning
    def reWeigh ():
        serial_write()
        output=serial_read()
        # Kontrollerar ifall koppling till vågen är etablerad och ett värde utläses
        if output is None:
            messagebox.askretrycancel("Värde ej inläst", "Ingen signal från våg")
        # Om koppling finns så sparas värdet och skrivs sedan till databasen
        else:
            product_weight=output
            vvalue.set(product_weight)
            update_vvalue()

    # Label med produktens namn
    tk.Label(scale,
             text=product_name,
             width=16,
             bg=bg_color,
             fg='white',
             font=('Ubuntu', 30, 'bold')
             ).grid(row=0, column=1)
    # Knapp för att väga, kallar på reWeigh() funktionen när den blir nedtryckt
    tk.Button(scale,
              text="VÄG",
              command=lambda:reWeigh()
              ).grid(row=2, column=1, pady=20, ipadx=5, ipady=5)
    # Initiellt värde på variabel som syns i textrutan där vikten senare syns
    vvalue=tk.StringVar(scale, value="Ställ din produkt på vågen och tryck på 'VÄG' ")

    # Label som sparar den inlästa vikten
    tk.Label(scale,
             textvariable=vvalue,
             height=5,
             width=50,
             font=("Arial", 12)
             ).grid(row=1, column=0, columnspan=3, padx=20, pady=10)

    reWeigh()
    tk.Button(scale, text="Spara vikt", command=write_to_database).grid(row=2,column=2)

    # Label är rubrik som visas ovanför dagens datum
    tk.Label(scale,
             text="Dagens Datum",
             height=5,
             width=20,
             font=('Arial', 10, 'bold')
             ).grid(row=3, column=0, padx=5)
    # Label som visar dagens datum på skärmen
    tk.Label(scale,
             text=todays_date,
             height=3,
             width=10
             ).grid(row=4, column=0, pady=5)

    # Label är rubrik som visas ovanför dagens temperatur
    tk.Label(scale,
             text="Temperatur (°C)",
             height=5,
             width=20,
             font=('Arial', 10, 'bold')
             ).grid(row=3, column=1, padx=5)

    # Label som visar dagens temperatur
    tk.Label(scale,
             text=weather_temp,
             height=3,
             width=10
             ).grid(row=4, column=1, pady=5)

    # Label är rubrik som visas ovanför dagens väderstatus
    tk.Label(scale,
             text="Väder",
             height=5,
             width=20,
             font=('Arial', 10, 'bold')
             ).grid(row=3, column=2, padx=20)

    # Label som visar dagens väderstatus i textform för den inställda staden
    tk.Label(scale,
             text=weather_status,
             height=3,
             width=10
             ).grid(row=4, column=2, pady=10)


# Skapa en frame som visar upp inläst statistik från databasen, datum och förbrukad vikt per dag för specifik produkt
def load_stats ():
    clear_widgets()
    stats.tkraise()
    stats.pack_propagate(False)
    global read_success

    tk.Button(stats, text="Kill App", command=close).grid(row=0, column=0, pady=2, padx=2)
    tk.Label(
        stats,
        text="Ingen produkt hittad, var god försök igen",
        bg=bg_color,
        fg="white",
        font=("Ubuntu", 30)
    ).grid(row=0, column=1, padx=20, pady=20)

    # Skapa en knapp som leder tillbaka till föregående skärm
    tk.Button(stats, text="Tillbaka",
              command=lambda:load_search()
              ,width=20,
              height=5).grid(row=1, column=1)

    read_from_db=read_from_database()
    if read_success == 1:
        clear_widgets()

        # Kalla på funktion som läser från databasen för inmatad produkt och sparar det till variabel
        # Sätte längden på antalet rader som skall returneras till antalet rader i tabellen som utläses från databasen
        total_rows=len(read_from_db)
        tk.Button(stats, text="BACK", command=lambda:load_search()).grid(row=0, column=0)
        tk.Button(stats, text="Kill App", command=close).grid(row=0, column=2)

        # Label för rubrik som säger vad sidan visar för produkt
        tk.Label(stats,
                 text="REGISTRERADE VÄGNINGAR AV: " + product_name,
                 bg=bg_color,
                 fg='white',
                 font=('Ubuntu', 20, 'bold')
                 ).grid(row=0, column=1, padx=100, pady=20)

        tree_frame = Frame(stats)
        tree_frame.pack(pady=80)

        # Skapa scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y,expand=5)

        # Konfigurering av Treeview som visar informationen
        style=ttk.Style()
        style.configure("Treeview",
                        background="silver",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="silver"
                        )

        # Skapa en Treeview som skall hålla informationen
        my_tree=ttk.Treeview(tree_frame)

        my_tree.configure(yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=my_tree.yview)

        # Initiera de kolumner som skall finnas i Treeviewen och namnsätter dem
        my_tree[ 'columns' ]=("Datum", "Vikt","Temp","Väder")

        # Formatera kolumner, sätter deras bredd och centrering
        my_tree.column("#0", width=80)
        my_tree.column("Datum", anchor=W, width=150)
        my_tree.column("Vikt", anchor=W, width=100)
        my_tree.column("Temp", anchor=W, width=100)
        my_tree.column("Väder", anchor=W, width=100)



        # Sätt rubriker på kolumnerna
        my_tree.heading("#0", text="Produkt", anchor=W)
        my_tree.heading("Datum", text="Datum", anchor=W)
        my_tree.heading("Vikt", text="Vikt(g)", anchor=W)
        my_tree.heading("Temp", text="Temperatur(C)", anchor=W)
        my_tree.heading("Väder", text="Väder", anchor=W)


        # Logik för att göra varannan rad grå för enklare läsning
        my_tree.tag_configure("oddrow", background="white")
        my_tree.tag_configure("evenrow", background="grey95")

        # Logik för att skriva ut de inlästa värdena från databasen på skärmen
        count=0
        for i in range(total_rows):
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text=product_name,
                               values=(read_from_db[ i ][ 0 ], read_from_db[ i ][ 1 ],round(read_from_db[ i ][ 2 ],0),read_from_db[ i ][ 3 ]),
                               tags=('evenrow'))
            else:
                my_tree.insert(parent='', index='end', iid=count, text=product_name,
                               values=(read_from_db[ i ][ 0 ], read_from_db[ i ][ 1 ],round(read_from_db[ i ][ 2 ],0),read_from_db[ i ][ 3 ]),
                               tags=('oddrow'))
            count+=1

        my_tree.pack()




# Initialisera applikationen
root=tk.Tk()
root.attributes('-fullscreen',True)
# Sätter rubrik och storlek på applikationen
root.title("Smart Scale")
root.geometry("800x480")

root.resizable(False, False)

# Skapa alla frames som används
main=tk.Frame(root, width=800, height=480, bg=bg_color)
search=tk.Frame(root, width=800, height=480, bg=bg_color)
scale=tk.Frame(root, width=800, height=480, bg=bg_color)
stats=tk.Frame(root, width=800, height=480, bg=bg_color)

# Sortera alla frames i root-fönster
for frame in (main, search, scale, stats):
    frame.grid(row=0, column=0, sticky="nesw")

# Ladda startsidan
load_main()
# Starta applikationen
root.mainloop()
