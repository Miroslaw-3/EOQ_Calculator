# EOQ Calculator by Mirko Benenati

-----

## Analisi del Programma EOQ Calculator

### Panoramica

Questo programma calcola il **Lotto Economico di Ordinazione (EOQ)** e i costi associati alla gestione delle scorte, sia tramite input manuale che attraverso la lettura da file JSON. L'EOQ è un modello fondamentale nella gestione dell'inventario che determina la quantità ottimale da ordinare per minimizzare i costi totali.

### Funzionalità Principali

1.  **Calcolo completo dell'EOQ**:

      * Lotto economico di ordinazione
      * Costi totali di gestione scorte
      * Costi di ordinazione
      * Costi di mantenimento
      * Numero di ordini annui
      * Tempo tra gli ordini (in giorni)

2.  **Modalità di input**:

      * Input manuale tramite interfaccia grafica
      * Lettura da file JSON con validazione dei dati
      * Supporto per separatori decimali (punto e virgola)

3.  **Gestione dei risultati**:

      * Visualizzazione tabellare ordinabile
      * Pulsante per pulizia risultati
      * Status bar operativa

4.  **Gestione degli errori**:

      * Validazione degli input
      * Gestione file mancanti o corrotti
      * Warning per anni non validi
      * Messaggi di errore descrittivi

-----

### Requisiti di Sistema

  * Python 3.13.15
  * Librerie: tkinter, math, json

-----

### Formato File JSON

Il programma legge dati da `dati.json` con questo formato:

```json
[
  {
    "anno": 2023,
    "domanda_annua": 10000,
    "costo_setup": 50,
    "costo_mantenimento": 2
  },
  {
    "anno": 2024,
    "domanda_annua": 15000,
    "costo_setup": 60,
    "costo_mantenimento": 2.5
  }
]
```

-----

### Regole di Validazione

1.  **Anno**:

      * Deve essere \> 1900
      * Valori non validi vengono scartati con warning

2.  **Valori numerici**:

      * Devono essere numeri positivi
      * Accetta sia punto che virgola come separatore decimale
      * Valori non validi generano errori specifici

3.  **File JSON**:

      * Deve esistere nel percorso specificato
      * Deve seguire la struttura corretta
      * Errori di parsing vengono segnalati

-----

### Istruzioni per l'Uso

1.  **Calcolo Manuale**:

      * Cliccare "Calcolo Manuale"
      * Inserire anno, domanda annua, costo setup e mantenimento
      * Cliccare "Calcola" per vedere i risultati nella tabella

2.  **Calcolo da JSON**:

      * Preparare un file `dati.json` nella stessa directory
      * Cliccare "Calcola da JSON"
      * I risultati validi appariranno nella tabella

3.  **Gestione Risultati**:

      * Ordinamento automatico per anno
      * "Pulisci Risultati" rimuove tutti i dati
      * Anni duplicati nei JSON sovrascrivono i precedenti

-----

### Limitazioni Note

  * Versione corrente: Beta 5
  * Percorso file JSON hardcoded (`dati.json`)
  * Ordinamento supportato solo per anno
  * Nessuna funzionalità di esportazione risultati

-----

### Sviluppi Futuri

da definire
