# Software Name: Orologio Mondiale con Sveglia
# Autore: Bocaletto Luca
# Licenza: GPLv3

import tkinter as tk
from tkinter import ttk, messagebox
import pytz
from datetime import datetime
import threading
import winsound

# Funzione per visualizzare l'orario nel fuso orario selezionato
def mostra_orario_selezionato():
    selezione = combobox_paesi.get()
    if selezione:
        try:
            # Ottieni il fuso orario selezionato e l'orario corrente in quel fuso orario
            fuso_orario = pytz.timezone(selezione)
            orario_corrente = datetime.now(fuso_orario)
            
            # Aggiorna l'etichetta con l'orario corrente nel fuso orario selezionato
            etichetta_orario.config(text=f"Orario in {selezione}: {orario_corrente.strftime('%H:%M:%S')}")
        except pytz.exceptions.UnknownTimeZoneError:
            # Visualizza un messaggio di errore se il fuso orario è sconosciuto
            etichetta_orario.config(text=f"Fuso orario sconosciuto per {selezione}")
    
    # Esegue nuovamente la funzione dopo 1 secondo
    app.after(1000, mostra_orario_selezionato)

# Funzione per impostare una sveglia
def imposta_sveglia():
    orario_sveglia_input = entry_orario_sveglia.get()
    if not orario_sveglia_input:
        return

    # Ottieni l'orario corrente
    orario_corrente = datetime.now()

    # Estrai ora e minuti dall'orario inserito per la sveglia
    ora_sveglia, minuti_sveglia = map(int, orario_sveglia_input.split(":"))

    # Crea un oggetto datetime per l'orario della sveglia
    orario_sveglia = orario_corrente.replace(hour=ora_sveglia, minute=minuti_sveglia, second=0, microsecond=0)

    selezione = combobox_paesi.get()
    if selezione:
        try:
            # Ottieni il fuso orario selezionato
            fuso_orario = pytz.timezone(selezione)

            # Localizza l'orario della sveglia nel fuso orario selezionato
            orario_sveglia_localizzato = fuso_orario.localize(orario_sveglia)

            # Calcola la differenza di tempo tra l'orario della sveglia e l'orario corrente
            differenza = orario_sveglia_localizzato - datetime.now(fuso_orario)

            if differenza.total_seconds() > 0:
                # Funzione da eseguire quando la sveglia scatta
                def suona_sveglia():
                    winsound.Beep(500, 1000)
                    messagebox.showinfo("Sveglia", f"Sveglia impostata per {orario_sveglia_input} in {selezione}")

                # Programma l'esecuzione della funzione della sveglia dopo la differenza di tempo
                threading.Timer(differenza.total_seconds(), suona_sveglia).start()

                # Visualizza un messaggio di successo con testo verde
                etichetta_stato_sveglia.config(text=f"Sveglia impostata per {orario_sveglia_input} in {selezione}", fg="green")
            else:
                # Visualizza un messaggio in rosso se l'orario selezionato è già trascorso
                etichetta_stato_sveglia.config(text="L'orario selezionato è già passato.", fg="red")
        except pytz.exceptions.UnknownTimeZoneError:
            # Visualizza un messaggio di errore per un fuso orario sconosciuto
            etichetta_stato_sveglia.config(text=f"Fuso orario sconosciuto per {selezione}", fg="red")
    else:
        # Visualizza un messaggio in rosso se non è stato selezionato un fuso orario
        etichetta_stato_sveglia.config(text="Seleziona un fuso orario", fg="red")

# Creazione della finestra principale dell'applicazione
app = tk.Tk()
app.title("Orologio Mondiale con Sveglia")

# Creazione e configurazione degli elementi dell'interfaccia utente
etichetta_titolo = tk.Label(app, text="Orologio Mondiale con Sveglia", font=("Helvetica", 16))
etichetta_titolo.pack(pady=10)

etichetta_paesi = tk.Label(app, text="Seleziona un paese:")
etichetta_paesi.pack()

# Popola la combobox dei fusi orari con i fusi orari disponibili
paesi = pytz.all_timezones
combobox_paesi = ttk.Combobox(app, values=paesi)
combobox_paesi.pack()

pulsante_mostra_orario = tk.Button(app, text="Mostra Orario", command=mostra_orario_selezionato)
pulsante_mostra_orario.pack()

etichetta_orario = tk.Label(app, text="")
etichetta_orario.pack()

pulsante_imposta_sveglia = tk.Button(app, text="Imposta Sveglia", command=imposta_sveglia)
pulsante_imposta_sveglia.pack()

etichetta_orario_sveglia = tk.Label(app, text="Inserisci l'orario della sveglia (HH:MM):")
etichetta_orario_sveglia.pack()

entry_orario_sveglia = tk.Entry(app)
entry_orario_sveglia.pack()

etichetta_stato_sveglia = tk.Label(app, text="")
etichetta_stato_sveglia.pack()

# Aggiorna periodicamente l'orario visualizzato
app.after(1000, mostra_orario_selezionato)

# Avvia il ciclo principale degli eventi dell'interfaccia grafica
app.mainloop()
