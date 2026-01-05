import sys
import os

#trova in che cartella si trova il file
cartella_corrente = os.path.dirname(__file__)

#torna indietro per trovare la cartella del progetto
cartella_progetto = os.path.join(cartella_corrente, '..')

#aggiunge la cartella del progetto alla lista dove python cerca i file
sys.path.append(cartella_progetto)

from decimal import Decimal
from gestione_dati.DataManager import DataManager
from gui.GestoreGrafici import GestoreGrafici 

def main():
    #istanzio i manager
    manager = DataManager()
    grafici = GestoreGrafici()
    
    #inserimento data su cui creare i grafici
    data_input = input("Inserisci la data (formato YYYY-MM-DD, es. 2025-11-26): ").replace(" ", "-")
    
    #costruiamo il percorso dove creare il file energie + la data inserita
    nome_file_input = f"file/giornate/{data_input}.txt"
    
    #input dove inserisci il valore del kw ora con una try except che copntrolla che il valore sia scritto con il punto se no usa
    #una replace per sostituire la virgola con il punto, se invece il valore non è valore (es. 'a') va in except e mette come
    #valore default 0.14256 che è il valore medio del kw ora alla scrittura del codice
    try:
        valore_input = input("Quanto costa 1 kw l'ora? (es. 0.14256): ").replace(',', '.')
        prezzo_kw_attuale = Decimal(valore_input)
    except:
        print("Valore non valido. Uso default 0.14256")
        prezzo_kw_attuale = Decimal("0.14256")

    #in modo sequenziale esegue gli step per far funzionare l'intero codice, dalla lettura ai calcoli e alla lavorazione dei grafici
    manager.step_1_lettura_dati(nome_file_input)
    manager.step_2_calcoli_e_scrittura(prezzo_kw_attuale)
    manager.step_3_grafici_watt()
    manager.step_4_grafici_prezzo()

    #output scritto nel terminale ma non nei grafici
    print("\n--- Elaborazione Completata ---")
    print(f"File creato: {manager.nome_file_output}")
    print(f"KW Consumati totali: {manager.kw_consumati}")
    print(f"Spesa Totale: {manager.totale_spesa}")

    #creazione grafici
    print("\nGenerazione grafici in corso...")
    
    #metodo per creazione completa grafici dove passiamo tutte le variabili necessarie
    grafici.mostra_dashboard_completa(
        lista_watt=manager.list_watt_ogni_ora, 
        lista_prezzo=manager.list_prezzo_ogni_ora, 
        prezzo_unitario=prezzo_kw_attuale,
        data_giorno=manager.data,
        kw_totali=manager.kw_consumati,
        spesa_totale=manager.totale_spesa
    )

if __name__ == "__main__":
    main()