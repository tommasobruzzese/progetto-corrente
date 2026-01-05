import matplotlib.pyplot as plt
import seaborn as sns

class GestoreGrafici:
    def __init__(self):
        #tema grafico
        sns.set_theme(style="whitegrid")

    def _converti_in_float(self, lista_decimal):
        #metodo per convertire i Decimal in float
        lista_convertita = []

        for elemento in lista_decimal:
            valore_float = float(elemento)
            
            lista_convertita.append(valore_float)

        return lista_convertita

    def mostra_dashboard_completa(self, lista_watt, lista_prezzo, prezzo_unitario, data_giorno, kw_totali, spesa_totale):
        """
        Mostra dashboard con:
        - Titolo con Data
        - Grafici (0-23 ore forzate)
        - Riepilogo finale in basso
        """
        watt_float = self._converti_in_float(lista_watt)
        prezzo_float = self._converti_in_float(lista_prezzo)
        
        # Creiamo l'asse X basato sui dati
        ore_dati = list(range(len(watt_float)))

        # Creazione figura con spazio extra sopra (top) e sotto (bottom) per i testi
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 11))
        
        # --- TITOLO SUPERIORE (DATA) ---
        fig.suptitle(f"Analisi Energetica del Giorno: {data_giorno}", fontsize=20, fontweight='bold', color='#2c3e50')

        # --- GRAFICO 1: CONSUMI ---
        sns.lineplot(x=ore_dati, y=watt_float, ax=ax1, linewidth=3, color="blue", marker="o")
        ax1.set_title("Consumo Energetico (KW)", fontsize=14, fontweight='bold')
        ax1.set_ylabel("KW")
        ax1.fill_between(ore_dati, watt_float, color="blue", alpha=0.1)
        
        # FORZATURA ASSE X (0-23)
        ax1.set_xticks(range(24)) # Mette tutte le tacchette da 0 a 23
        ax1.set_xlim(0, 23)       # Blocca la vista tra 0 e 23 esatti

        # --- GRAFICO 2: PREZZI ---
        # Hue=ore_dati serve per evitare warning, legend=False nasconde la legenda
        sns.barplot(x=ore_dati, y=prezzo_float, ax=ax2, palette="flare", hue=ore_dati, legend=False)
        
        titolo_costi = f"Costo Orario (€) - Tariffa: {prezzo_unitario} €/kW"
        ax2.set_title(titolo_costi, fontsize=14, fontweight='bold', color="darkred")
        ax2.set_ylabel("Euro")
        

        # --- RIEPILOGO IN BASSO ---
        testo_riepilogo = (
            f"RIEPILOGO GIORNALIERO\n"
            f"⚡ Energia Totale: {kw_totali} kW    |    "
            f"💰 Spesa Totale: {spesa_totale} €"
        )
        
        # Aggiungiamo un box decorativo in fondo alla pagina
        fig.text(0.5, 0.05, testo_riepilogo, ha='center', fontsize=14, 
                bbox=dict(facecolor='#f8f9fa', edgecolor='black', boxstyle='round,pad=1'))

        # Aggiusta layout per far stare tutto senza sovrapposizioni
        plt.subplots_adjust(top=0.92, bottom=0.15, hspace=0.3)
        
        plt.show()