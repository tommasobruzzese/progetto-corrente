#classe necessaria per lavorare sui file
#utilizziamo dei metodi che ci permettono di aprire in lettura o scrittura
class FileHandler:
    #costruttore non necessario in quanto non stiamo istanziando un oggetto ma bensi questo classe serve
    #solo per i metodi da utilizzare sui file
    def __init__(self):
        pass

    #metodo che ci permette di leggere tutte le righe di un file e ritornare una lista con tutto il contenuto
    def leggi_righe(self, percorso):
        file = open(percorso, "r")
        contenuto = file.readlines()
        file.close()
        return contenuto

    #metodo che ci permette di aprire un file in scrittura (w=write)
    def apri_file_scrittura(self, percorso):
        return open(percorso, "w")

    #metodo che ci permette di aprire un file in lettura (r=read)
    def apri_file_lettura(self, percorso):
        # Questo serve per l'ultimo passaggio del tuo codice dove rileggi il file output
        return open(percorso, "r")