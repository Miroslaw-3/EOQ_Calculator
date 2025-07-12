''' EOQ Calculator - Questo programma permette di calcolare 
il Lotto Economico di Ordinazione'''

import math
import tkinter as tk


class EOQ_calculator:
    # Classe principale che racchiude la logica per il calcolo dell'EOQ.
    def __init__(self):
        self.domanda_annua = 0.0
        self.costo_setup = 0.0
        self.costo_mantenimento = 0.0
        self.eoq = 0.0
        self.costi_totali = 0.0
        self.costi_ordinazione = 0.0
        self.costi_mantenimento = 0.0
        self.ordini_annui = 0.0
        self.tempo_tra_ordini = 0.0

    def get_input(self):
        # gestisce gli input inseriti dall'utente
        try:
            self.domanda_annua = float(
                input("Inserisci la domanda annua: ")
            )
            self.costo_setup = float(
                input("Costo di setup per singolo ordine: ")
            )
            self.costo_mantenimento = float(
                input("Costo di mantenimento scorte annuo: ")
            )
            
            # Verifica che tutti i valori inseriti siano positivi
            valori = [
                self.domanda_annua,
                self.costo_setup,
                self.costo_mantenimento
            ]
            if any(val <= 0 for val in valori):
                raise ValueError("Tutti i valori devono essere positivi")
                
        except ValueError as e:
            print(f"\nERRORE: {str(e)}")
            print("Per favore inserisci valori numerici positivi.")
            return False
        return True
    
    def calculate(self):
        # questa funzione si occupa dei calcoli (EOQ e costi totali)

        # Calcolo del Lotto Economico di Ordinazione (EOQ)
        self.eoq = math.sqrt(
            (2 * self.domanda_annua * self.costo_setup) /
            self.costo_mantenimento
        )
        
        # Calcolo dei costi totali (di ordinazione e di mantenimento)
        self.costi_ordinazione = (
            (self.domanda_annua / self.eoq) * self.costo_setup
        )

        self.costi_mantenimento = (
            (self.eoq / 2) * self.costo_mantenimento
        )

        self.costi_totali = (
            self.costi_ordinazione + self.costi_mantenimento
        )

        # Calcolo del numero di ordini annui
        self.ordini_annui = (
            self.domanda_annua / self.eoq
        )

        # Calcolo del tempo tra ordini (in giorni)
        self.tempo_tra_ordini = (
            365 / self.ordini_annui
        )

    def show_results(self):
        # questa funzione mostra i risultati all'utente
        print("-----------------------------------------")
        print("| {:<22} | {:<12} |".format("PARAMETRO", "VALORE"))
        print("-----------------------------------------")
        print(
            "| {:<22} | {:<12} |".format(
            "EOQ (Quantità)", f"~ {int(round(self.eoq))} pz"
            )
        )
        print(
            "| {:<22} | {:<12} |".format(
            "Costo Ordini/Anno", f"{self.costi_ordinazione:.2f} €"
            )
        )
        print(
            "| {:<22} | {:<12} |".format(
            "Costo Magazzino/Anno", f"{self.costi_mantenimento:.2f} €"
            )
        )
        print(
            "| {:<22} | {:<12} |".format(
            "COSTO TOTALE", f"{self.costi_totali:.2f} €"
            )
        )
        print(
            "| {:<22} | {:<12} |".format(
            "Ordini/Anno", f"~ {int(round(self.ordini_annui))}"
            )
        )
        print(
            "| {:<22} | {:<12} |".format(
            "Ogni Quanto Ordinare?",
            f"~ {int(round(self.tempo_tra_ordini))} giorni"
            )
        )
        print("-----------------------------------------")


class EOQ_application:
    '''Classe che gestisce l'interazione con l'utente e 
    il flusso dell'applicazione'''

    def __init__(self):
        self.calculator = EOQ_calculator()
    
    def run(self):
        """Gestisce il flusso principale dell'applicazione"""
        while True:
            if self.calculator.get_input():
                self.calculator.calculate()
                self.calculator.show_results()
            
            continua = input("\nVuoi fare un altro calcolo? (s/n): ").lower()
            if continua != 's':
                break
        
        print("Programma terminato.")


if __name__ == "__main__":
    app = EOQ_application()
    app.run()