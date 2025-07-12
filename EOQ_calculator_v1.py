''' Questo programma calcola il Lotto Economico di Ordinazione (EOQ) e i
costi totali associati, sia da input manuale che da un file JSON.
'''
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import math
import json

# Costanti globali
VERSIONE = "1.0"
AUTORE = "Mirko Benenati"
PERCORSO_JSON = "dati.json"


class EOQCalculator:
    ''' Classe principale che racchiude la logica per il calcolo dell'EOQ 
    e dei vari costi '''

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

    def calculate_EOQ(self):
        # Questa funzione si occupa dei calcoli (EOQ e costi totali)

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

    def read_from_json(self, PERCORSO_JSON):
        ''' Questa funzione legge i dati appartenenti a diversi anni 
        da un file JSON e itera ad ogni anno per calcolare l'EOQ '''

        try:
            with open(PERCORSO_JSON, 'r') as file:
                data = json.load(file)
                results = []
                invalid_years = []  # Tiene traccia degli anni non validi
                
                for record in data:
                    # Estrazione e validazione dell'anno
                    year = record.get("anno", 0)
                    if year <= 1900:
                        invalid_years.append(year)
                        continue  # Salta il record con anno non valido
                    
                    # Estrazione e validazione degli altri campi
                    demand = record.get("domanda_annua", 0.0)
                    setup = record.get("costo_setup", 0.0)
                    holding = record.get("costo_mantenimento", 0.0)
                    
                    # Controllo che tutti i valori siano numeri positivi
                    if not all(
                        isinstance(val, (int, float)) and val > 0
                        for val in [demand, setup, holding]
                    ):
                        messagebox.showerror(
                            "ERRORE", 
                            f"Valori non validi per l'anno {year}. Devono essere numeri positivi."
                        )
                        continue
                    
                    # Assegnazione e calcolo
                    self.anno = year
                    self.domanda_annua = demand
                    self.costo_setup = setup
                    self.costo_mantenimento = holding
                    self.calculate_EOQ()
                    results.append(self.get_results_dict())
                
                # Mostra un avviso riepilogativo per gli anni non validi
                if invalid_years:
                    years_str = ", ".join(map(str, invalid_years))
                    messagebox.showwarning(
                        "Anni non validi",
                        f"Sono stati saltati {len(invalid_years)} record con anni non validi: {years_str}"
                    )
                
                return results, invalid_years

        except FileNotFoundError:
            return [{"error": f"ERRORE: Il file {PERCORSO_JSON} non è stato trovato."}]
        except json.JSONDecodeError:
            return [{"error": "ERRORE: Formato JSON non valido."}]
    
    def get_results_dict(self):
        """Restituisce i risultati come dizionario"""
        return {
            "Anno": int(self.anno),
            "Domanda Annua (pz)": int(round(self.domanda_annua)),
            "EOQ (pz)": int(round(self.eoq)),
            "Costo Ordini Annuo (€)": f"{self.costi_ordinazione:.2f}",
            "Costo Magazzino Annuo (€)": f"{self.costi_mantenimento:.2f}",
            "Costo Totale Annuo (€)": f"{self.costi_totali:.2f}",
            "Ordini/Anno": int(round(self.ordini_annui)),
            "Giorni tra ordini": int(round(self.tempo_tra_ordini))
        }


class EOQ_GUI:
    # Classe principale che gestisce la GUI

    def __init__(self, master):
        self.master = master
        master.title(f"EOQ Calculator {VERSIONE}")
        master.geometry("1200x650")
        master.minsize(width=1200, height=650) # stabilisce la dimnensione minima della finestra
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
            text=f"VERSIONE {VERSIONE} - by {AUTORE}",
            font=("Arial", 9)
        ).pack(side=tk.RIGHT, padx=10)
        
        # Pulsanti
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.manual_btn = ttk.Button(
            button_frame,
            text="Calcolo Manuale",
            command=self.user_input_window,
            style="TButton"
        )
        self.manual_btn.pack(side=tk.LEFT, padx=5)
        
        self.json_btn = ttk.Button(
            button_frame,
            text="Calcola da JSON",
            command=self.calculate_from_json,
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
        columns = ("Anno", "Domanda Annua (pz)", "EOQ (pz)", "Costo Ordini Annuo (€)",
                   "Costo Magazzino Annuo (€)", "Costo Totale Annuo (€)", "Ordini per Anno",
                   "Giorni tra ordini")
        
        self.results_tree = ttk.Treeview(
            results_frame, 
            columns=columns, 
            show="headings",
            style="Result.Treeview",
            selectmode="browse"
        )
        
        # Configurazione colonne
        col_widths = [80, 150, 100, 170, 190, 170, 120, 120]
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
    
    def user_input_window(self):
        # Apre la finestra per l'inserimento manuale

        manual_window = tk.Toplevel(self.master)
        manual_window.title("Calcolo Manuale")
        manual_window.geometry("450x250")
        manual_window.resizable(False, False)
        manual_window.grab_set()
        
        # Frame principale
        input_frame = ttk.Frame(manual_window, padding=20)
        input_frame.pack(fill=tk.BOTH, expand=True)
        
        # Variabili
        year_var = tk.StringVar()
        demand_var = tk.StringVar()
        setup_var = tk.StringVar()
        holding_var = tk.StringVar()
        
        # Etichette e campi input
        ttk.Label(input_frame, text="Anno di riferimento:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=year_var).grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(input_frame, text="Domanda annua:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=demand_var).grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(input_frame, text="Costo di setup per ordine:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=setup_var).grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(input_frame, text="Costo di mantenimento per unità per anno:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=holding_var).grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW)
        
        # Pulsanti
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=15)
        
        ttk.Button(
            btn_frame, 
            text="Calcola", 
            command=lambda: self.user_input_calculation(
                year_var.get(),
                demand_var.get(),
                setup_var.get(),
                holding_var.get(),
                manual_window
            ),
            width=10
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            btn_frame, 
            text="Annulla", 
            command=manual_window.destroy,
            width=10
        ).pack(side=tk.RIGHT, padx=10)
    
    def user_input_calculation(self, year, demand, setup, holding, window):
        # Esegue il calcolo per l'input manuale
        try:
            # Valido l'input per permettere all'utente di usare sia il punto che la virgola come separatore decimale
            year = int(year)
            if year <= 1900:
                raise ValueError("L'anno deve essere maggiore o uguale a 1900")
            
            demand = float(demand.replace(',', '.'))
            setup = float(setup.replace(',', '.'))
            holding = float(holding.replace(',', '.'))
            
            if any(val <= 0 for val in [demand, setup, holding]):
                raise ValueError("Tutti i valori devono essere positivi")
            
            # Calcolo
            calculator = EOQCalculator()
            calculator.anno = year
            calculator.domanda_annua = demand
            calculator.costo_setup = setup
            calculator.costo_mantenimento = holding
            calculator.calculate_EOQ()
            
            # Aggiungi risultati alla tabella e ordina
            self.add_to_table(calculator.get_results_dict())
            self.status_var.set("Calcolo manuale completato con successo")
            window.destroy()
            
        except ValueError as e:
            messagebox.showerror("Errore di input", f"Dati non validi: {str(e)}")
        except Exception as e:
            messagebox.showerror("Errore", f"Si è verificato un errore: {str(e)}")
    
    def calculate_from_json(self):
        try:
            calculator = EOQCalculator()
            results, invalid_years = calculator.read_from_json(PERCORSO_JSON)

            if not results:
                self.status_var.set("Nessun dato da elaborare")
                return
                
            if "error" in results[0]:
                messagebox.showerror("Errore", results[0]["error"])
                return

            # Crea un set con i dati presenti nel file json per la rimozione
            json_years = set()
            for result in results:
                if "Anno" in result:
                    json_years.add(str(result["Anno"]))
            
            # Rimuove i record esistenti con gli stessi anni
            for item in self.results_tree.get_children():
                values = self.results_tree.item(item, 'values')
                if values:
                    year_in_table = values[0]
                    if year_in_table in json_years:
                        self.results_tree.delete(item)
            
            # Ordina i risultati per anno prima di aggiungerli alla tabella
            sorted_results = sorted(results, key=lambda x: int(x.get("Anno", 0)))

            # Aggiorna i nuovi risultati
            for result in sorted_results:
                self.add_to_table(result, sort_after_add=False) # Non ordinare dopo ogni singola aggiunta qui

            self.sort_table_by_year() # Ordina una sola volta alla fine
            self.status_var.set(
                f"Calcolo da JSON completato: {len(results)}/{len(invalid_years)+len(results)} record calcolati"
                )
            
        except Exception as e:
            messagebox.showerror("Errore", f"Si è verificato un errore: {str(e)}")

    def add_to_table(self, result, sort_after_add=True):
        # Aggiunge una riga alla tabella dei risultati
        values = (
            result.get("Anno", ""),
            result.get("Domanda Annua (pz)", ""),
            result.get("EOQ (pz)", ""),
            result.get("Costo Ordini Annuo (€)", ""),
            result.get("Costo Magazzino Annuo (€)", ""),
            result.get("Costo Totale Annuo (€)", ""),
            result.get("Ordini/Anno", ""),
            result.get("Giorni tra ordini", "")
        )
        self.results_tree.insert("", tk.END, values=values)
        if sort_after_add:
            self.sort_table_by_year()
    
    def sort_table_by_year(self):
        # Raccogli tutti gli elementi dalla treeview
        items = self.results_tree.get_children()

        # Prepara i dati per l'ordinamento: (anno, item_id)
        # item_id è necessario per poter riordinare gli elementi nella treeview
        data_to_sort = []
        for item_id in items:
            values = self.results_tree.item(item_id, 'values')
            if values and values[0] != "":
                try:
                    year = int(values[0])
                    data_to_sort.append((year, item_id, values)) # Include anche i valori originali per reinserirli
                except ValueError:
                    # Ignora o gestisci righe con anno non numerico
                    pass

        # Ordina i dati in base all'anno
        data_to_sort.sort(key=lambda x: x[0])

        # Rimuovi tutti gli elementi esistenti dalla treeview
        for item_id in items:
            self.results_tree.delete(item_id)

        # Reinserisci gli elementi ordinati
        for year, item_id, values in data_to_sort:
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