from decimal import Decimal
from .FileHandler import FileHandler

class DataManager:
    #necessario per lavorare sui file
    def __init__(self):
        self.file_handler = FileHandler()
        
        #liste e variabili utili per lavorare con i file
        self.list_giornata = []
        self.list_energie_istantanea = []
        self.data = ''
        self.nome_file_output = ''
        
        #liste per grafici
        self.list_watt_ogni_ora = []
        self.list_prezzo_ogni_ora = []
        
        #variabili necessarie per statistiche finali
        self.kw_consumati = 0
        self.watt_medio_ora_consumato = 0
        self.totale_spesa = 0

    def step_1_lettura_dati(self, nome_file):
        #contenuto contenente tutte le righe del file
        contenuto = self.file_handler.leggi_righe(nome_file)

        #for che splitta tutte le righe togliendo gli spazi e dividendo dove c'è una virgola
        for linea in contenuto:
            riga_split = linea.strip().split(',')
            data_ora = riga_split[0]
            energia_istantanea = riga_split[1]

            data_split = data_ora.split(' ')
            self.data = data_split[0]
            
            self.list_energie_istantanea.append(energia_istantanea)

            #dizionario in cui salviamo la data_ora e le energie riguardanti quella data_ora
            dict_minuto = {'data_ora':data_ora, 'energia_istantanea':energia_istantanea}
            self.list_giornata.append(dict_minuto)

    def step_2_calcoli_e_scrittura(self, prezzo_kw_attuale):
        #preparazione file output dove grazie alle graffe con il .format inseriamo nel nome del file la variabile che passiamo come parametro
        self.nome_file_output = "file/energie/energie_{}.txt".format(self.data)
        file_output = self.file_handler.apri_file_scrittura(self.nome_file_output)

        #variabili utili per scrivere successivamente sui grafici
        prezzo_fine_giornata = 0
        watt_consumati = 0

        #for che cicla la lista delle energie in un dato momento e calcola il consumo in kwmin
        for energia in self.list_energie_istantanea:
            trasformazione_kwMin = (Decimal(energia) / 1000)/60
            #utilizziamo un round che ci fa lavorare con massimo 9 decimali per essere più ordinati
            trasformazione_kwMin = round(trasformazione_kwMin, 9)

            prezzo_minuto = Decimal(trasformazione_kwMin * prezzo_kw_attuale)
            prezzo_minuto = round(prezzo_minuto, 9)

            prezzo_fine_giornata += prezzo_minuto

            watt_consumati += Decimal(energia)

            file_output.write(energia + ',' + str(trasformazione_kwMin) + ',' + str(prezzo_minuto) + "\n")
            
        file_output.close()

        #salviamo il totale della spesa giornaliera
        self.totale_spesa = round(prezzo_fine_giornata, 2)

        #dati per statistiche
        self.kw_consumati = round(watt_consumati / 60000, 2)
        self.watt_medio_ora_consumato = round(self.kw_consumati / 24, 2)

    def step_3_grafici_watt(self):
        somma_watt = 0
        contatore = 0

        #for che ci permette di riempire le liste con i dati di ogni ora
        for energia in self.list_energie_istantanea:
            somma_watt += Decimal(energia)

            contatore += 1

            if contatore == 60:
                kw_ogni_ora = round(somma_watt / 60000, 8)
                self.list_watt_ogni_ora.append(kw_ogni_ora)
                somma_watt = 0
                contatore = 0

    def step_4_grafici_prezzo(self):
        contatore = 0
        prezzo = 0

        #rileggiamo il contenuto del file energie
        file_output = self.file_handler.apri_file_lettura(self.nome_file_output)
        contenuto = file_output.readlines()

        for linea in contenuto:
            riga_split = linea.strip().split(',')

            prezzo += Decimal(riga_split[2])

            contatore += 1

            if contatore == 60:
                self.list_prezzo_ogni_ora.append(prezzo)
                prezzo = 0
                contatore = 0

        file_output.close()