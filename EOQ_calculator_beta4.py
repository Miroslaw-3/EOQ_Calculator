''' Questo programma calcola il Lotto Economico di Ordinazione (EOQ) e i
costi totali associati, sia da input manuale che da un file JSON.
'''

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import math
import json

# Costanti
VERSION = "Beta 4"
AUTHOR = "Mirko Benenati"
json_file_path = "dati.json"

class EOQ_calculator:
    # Classe principale che racchiude la logica per il calcolo dell'EOQ.
    def __init__(self):
        self.anno = 0
        self.domanda_annua = 0.0
        self.costo_setup = 0.0
        self.costo_mantenimento = 0.0
        self.eoq = 0.0
        self.costi_totali = 0.0
        self.costi_ordinazione = 0.0
        self.costi_mantenimento = 0.0
        self.ordini_annui = 0.0
        self.tempo_tra_ordini = 0.0

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

    def calcolate_from_json(self, json_file_path):
        ''' questa funzione legge i dati appartenenti a diversi anni 
        da un file JSON e itera ad ogni anno per calcolare l'EOQ '''

        try:
            with open(json_file_path, 'r') as file:
                dati = json.load(file)
                results = []
                for record in dati:
                    self.anno = record.get("anno", 0)
                    self.domanda_annua = record.get("domanda_annua", 0.0)
                    self.costo_setup = record.get("costo_setup", 0.0)
                    self.costo_mantenimento = record.get("costo_mantenimento", 0.0)

                    if not all(
                        isinstance(value, (int, float)) and value > 0
                        for value in [
                            self.domanda_annua,
                            self.costo_setup,
                            self.costo_mantenimento
                        ]
                    ):
                        print(f"ERRORE: Valori non validi per l'anno {self.anno}.")
                        continue
                    
                    self.calculate()
                    results.append(self.get_results_dict())
                return results

        except FileNotFoundError:
            return [{"error": f"ERRORE: Il file {json_file_path} non è stato trovato."}]
        except json.JSONDecodeError:
            return [{"error": "ERRORE: Formato JSON non valido."}]
    
    def get_results_dict(self):
        """Restituisce i risultati come dizionario"""
        return {
            "Anno": int(self.anno),
            "EOQ (pz)": int(round(self.eoq)),
            "Costo Ordini (€)": f"{self.costi_ordinazione:.2f}",
            "Costo Magazzino (€)": f"{self.costi_mantenimento:.2f}",
            "Costo Totale (€)": f"{self.costi_totali:.2f}",
            "Ordini/Anno": int(round(self.ordini_annui)),
            "Giorni tra ordini": int(round(self.tempo_tra_ordini))
        }


class EOQ_GUI:
    # Classe princche gestisce la GUI
    
    def __init__(self, master):
        self.master = master
        master.title(f"EOQ Calculator {VERSION}")
        master.geometry("900x600")
        master.minsize(width=900, height=600) # stabilisce la dimnensione minima della finestra
        master.configure(bg="#f0f0f0")
        
        # Stile per i widget
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", font=("Arial", 10, "bold"), padding=6)
        self.style.configure("Header.TLabel", font=("Arial", 14, "bold"), background="#e0e0e0")
        self.style.configure("Result.Treeview", font=("Arial", 10))
        self.style.configure("Result.Treeview.Heading", font=("Arial", 10, "bold"))
        
        # Frame principale
        main_frame = ttk.Frame(master)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Intestazione
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(
            header_frame, 
            text="EOQ Calculator", 
            style="Header.TLabel"
        ).pack(side=tk.LEFT, padx=10, pady=10)
        
        ttk.Label(
            header_frame, 
            text=f"Versione {VERSION} - by {AUTHOR}",
            font=("Arial", 9)
        ).pack(side=tk.RIGHT, padx=10)
        
        # Pulsanti
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.manual_btn = ttk.Button(
            button_frame,
            text="Calcolo Manuale",
            command=self.open_manual_window,
            style="TButton"
        )
        self.manual_btn.pack(side=tk.LEFT, padx=5)
        
        self.json_btn = ttk.Button(
            button_frame,
            text="Calcola da JSON",
            command=self.calcola_da_json,
            style="TButton"
        )
        self.json_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(
            button_frame,
            text="Pulisci Risultati",
            command=self.clear_results,
            style="TButton"
        )
        self.clear_btn.pack(side=tk.RIGHT, padx=5)
        
        # Tabella risultati
        results_frame = ttk.LabelFrame(main_frame, text="Risultati")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Treeview
        columns = ("Anno", "EOQ (pz)", "Costo Ordini (€)", "Costo Magazzino (€)", 
                   "Costo Totale (€)", "Ordini per Anno", "Giorni tra ordini")
        
        self.results_tree = ttk.Treeview(
            results_frame, 
            columns=columns, 
            show="headings",
            style="Result.Treeview",
            selectmode="browse"
        )
        
        # Configurazione colonne
        col_widths = [80, 80, 120, 130, 120, 100, 120]
        for col, width in zip(columns, col_widths):
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=width, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            results_frame, 
            orient=tk.VERTICAL, 
            command=self.results_tree.yview
        )
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        # Layout
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto")
        status_bar = ttk.Label(master, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def open_manual_window(self):
        # Apre la finestra per l'inserimento manuale

        manual_win = tk.Toplevel(self.master)
        manual_win.title("Calcolo Manuale")
        manual_win.geometry("400x300")
        manual_win.resizable(False, False)
        manual_win.grab_set()
        
        # Frame principale
        input_frame = ttk.Frame(manual_win, padding=20)
        input_frame.pack(fill=tk.BOTH, expand=True)
        
        # Variabili
        anno_var = tk.StringVar()
        domanda_var = tk.StringVar()
        setup_var = tk.StringVar()
        mantenimento_var = tk.StringVar()
        
        # Etichette e campi input
        ttk.Label(input_frame, text="Anno di riferimento:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=anno_var).grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(input_frame, text="Domanda annua:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=domanda_var).grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(input_frame, text="Costo di setup:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=setup_var).grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(input_frame, text="Costo di mantenimento:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=mantenimento_var).grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW)
        
        # Pulsanti
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=15)
        
        ttk.Button(
            btn_frame, 
            text="Calcola", 
            command=lambda: self.calcola_manuale(
                anno_var.get(),
                domanda_var.get(),
                setup_var.get(),
                mantenimento_var.get(),
                manual_win
            ),
            width=10
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            btn_frame, 
            text="Annulla", 
            command=manual_win.destroy,
            width=10
        ).pack(side=tk.RIGHT, padx=10)
    
    def calcola_manuale(self, anno, domanda, setup, mantenimento, window):
        # Esegue il calcolo per l'input manuale
        try:
            # Valido l'input per permettere all'utente di usare sia il punto che la virgola come separatore decimale
            anno = int(anno.replace(',', '.'))
            domanda = float(domanda.replace(',', '.'))
            setup = float(setup.replace(',', '.'))
            mantenimento = float(mantenimento.replace(',', '.'))
            
            if any(val <= 0 for val in [domanda, setup, mantenimento]):
                raise ValueError("Tutti i valori devono essere positivi")
            
            # Calcolo
            calc = EOQ_calculator()
            calc.anno = anno
            calc.domanda_annua = domanda
            calc.costo_setup = setup
            calc.costo_mantenimento = mantenimento
            calc.calculate()
            
            # Aggiungi risultati alla tabella
            self.add_to_table(calc.get_results_dict())
            self.status_var.set("Calcolo manuale completato con successo")
            window.destroy()
            
        except ValueError as e:
            messagebox.showerror("Errore di input", f"Dati non validi: {str(e)}")
        except Exception as e:
            messagebox.showerror("Errore", f"Si è verificato un errore: {str(e)}")
    
    def calcola_da_json(self):
        # Esegue il calcolo dai dati nel file JSON
        try:
            calc = EOQ_calculator()
            results = calc.calcolate_from_json(json_file_path)
            
            if results and "error" in results[0]:
                messagebox.showerror("Errore", results[0]["error"])
                return
            
            # Aggiungi nuovi risultati
            for result in results:
                self.add_to_table(result)
            
            self.status_var.set(f"Calcolo da JSON completato: {len(results)} record elaborati")
            
        except Exception as e:
            messagebox.showerror("Errore", f"Si è verificato un errore: {str(e)}")
    
    def add_to_table(self, result):
        # Aggiunge una riga alla tabella dei risultati
        values = (
            result.get("Anno", ""),
            result.get("EOQ (pz)", ""),
            result.get("Costo Ordini (€)", ""),
            result.get("Costo Magazzino (€)", ""),
            result.get("Costo Totale (€)", ""),
            result.get("Ordini/Anno", ""),
            result.get("Giorni tra ordini", "")
        )
        self.results_tree.insert("", tk.END, values=values)
    
    def clear_results(self):
        # Pulisce la tabella dei risultati
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        self.status_var.set("Record eliminati")


if __name__ == "__main__":
    root = tk.Tk()
    app = EOQ_GUI(root)
    root.mainloop()