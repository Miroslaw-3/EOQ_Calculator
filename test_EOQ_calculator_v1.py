import math
import os
import json
import tempfile
import pytest
from EOQ_calculator_v1 import EOQCalculator
import EOQ_calculator_v1

def test_calculate_EOQ_basic():
    """Test del calcolo base dell'EOQ (Economic Order Quantity) e dei costi associati"""
    calc = EOQCalculator()
    calc.anno = 2024
    calc.domanda_annua = 1000
    calc.costo_setup = 50
    calc.costo_mantenimento = 2
    calc.calculate_EOQ()
    
    # Verifica che l'EOQ calcolato sia corretto secondo la formula: sqrt((2*demanda*costo_setup)/costo_mantenimento)
    assert math.isclose(calc.eoq, math.sqrt(50000), rel_tol=1e-6)
    
    # Verifica che i costi di ordinazione siano calcolati correttamente: (domanda_annua/EOQ)*costo_setup
    assert math.isclose(calc.costi_ordinazione, (1000/calc.eoq)*50, rel_tol=1e-6)
    
    # Verifica che i costi di mantenimento siano calcolati correttamente: (EOQ/2)*costo_mantenimento
    assert math.isclose(calc.costi_mantenimento, (calc.eoq/2)*2, rel_tol=1e-6)
    
    # Verifica che i costi totali siano la somma dei costi di ordinazione e mantenimento
    assert math.isclose(calc.costi_totali, calc.costi_ordinazione + calc.costi_mantenimento, rel_tol=1e-6)
    
    # Verifica che il numero di ordini annuali sia calcolato correttamente: domanda_annua/EOQ
    assert math.isclose(calc.ordini_annui, 1000/calc.eoq, rel_tol=1e-6)
    
    # Verifica che il tempo tra ordini sia calcolato correttamente: 365 giorni/ordini_annui
    assert math.isclose(calc.tempo_tra_ordini, 365/calc.ordini_annui, rel_tol=1e-6)

def test_get_results_dict_format():
    """Test del formato del dizionario restituito dal metodo get_results_dict"""
    calc = EOQCalculator()
    calc.anno = 2023
    calc.domanda_annua = 500
    calc.costo_setup = 20
    calc.costo_mantenimento = 1
    calc.calculate_EOQ()
    results = calc.get_results_dict()
    
    # Verifica che il dizionario contenga tutti i campi con i tipi di dati corretti
    assert results["Anno"] == 2023
    assert isinstance(results["Domanda Annua (pz)"], int)
    assert isinstance(results["EOQ (pz)"], int)
    assert isinstance(results["Costo Ordini Annuo (€)"], str)
    assert isinstance(results["Costo Magazzino Annuo (€)"], str)
    assert isinstance(results["Costo Totale Annuo (€)"], str)
    assert isinstance(results["Ordini/Anno"], int)
    assert isinstance(results["Giorni tra ordini"], int)

def test_read_from_json_valid(tmp_path):
    """Test della lettura da file JSON con dati validi"""
    # Crea un file JSON temporaneo con dati di test validi
    data = [
        {"anno": 2022, "domanda_annua": 1200, "costo_setup": 30, "costo_mantenimento": 3},
        {"anno": 2023, "domanda_annua": 1500, "costo_setup": 40, "costo_mantenimento": 4}
    ]
    json_file = tmp_path / "test.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f)
    
    # Verifica che tutti i record validi vengano elaborati correttamente
    calc = EOQCalculator()
    results, invalid_years = calc.read_from_json(str(json_file))
    assert len(results) == 2
    assert invalid_years == []
    assert results[0]["Anno"] == 2022
    assert results[1]["Anno"] == 2023

def test_read_from_json_invalid_year(tmp_path):
    """Test della lettura da file JSON contenente anni non validi"""
    # Crea un file JSON temporaneo con un anno non valido (prima del 1900)
    data = [
        {"anno": 1899, "domanda_annua": 1000, "costo_setup": 10, "costo_mantenimento": 1},
        {"anno": 2020, "domanda_annua": 1000, "costo_setup": 10, "costo_mantenimento": 1}
    ]
    json_file = tmp_path / "test_invalid_year.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f)
    
    # Verifica che solo i record con anni validi vengano elaborati
    calc = EOQCalculator()
    results, invalid_years = calc.read_from_json(str(json_file))
    assert len(results) == 1
    assert results[0]["Anno"] == 2020
    assert invalid_years == [1899]

def test_read_from_json_invalid_values(tmp_path, monkeypatch):
    """Test della lettura da file JSON contenente valori non validi"""
    # Patch per evitare la visualizzazione di messaggi di errore GUI durante il test
    monkeypatch.setattr(EOQ_calculator_v1, "messagebox", type("dummy", (), {"showerror": lambda *a, **k: None, "showwarning": lambda *a, **k: None})())
    
    # Crea un file JSON temporaneo con valori non validi (domanda negativa e costo setup zero)
    data = [
        {"anno": 2021, "domanda_annua": -100, "costo_setup": 10, "costo_mantenimento": 1},
        {"anno": 2022, "domanda_annua": 1000, "costo_setup": 0, "costo_mantenimento": 1},
        {"anno": 2023, "domanda_annua": 1000, "costo_setup": 10, "costo_mantenimento": 1}
    ]
    json_file = tmp_path / "test_invalid_values.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f)
    
    # Verifica che solo i record con valori validi vengano elaborati
    calc = EOQCalculator()
    results, invalid_years = calc.read_from_json(str(json_file))
    assert len(results) == 1
    assert results[0]["Anno"] == 2023

def test_read_from_json_file_not_found():
    """Test della gestione dell'errore quando il file JSON non esiste"""
    calc = EOQCalculator()
    results = calc.read_from_json("non_existent_file.json")
    
    # Verifica che venga restituito un messaggio di errore appropriato
    assert isinstance(results, list)
    assert "error" in results[0]
    assert "non_existent_file.json" in results[0]["error"]

def test_read_from_json_invalid_json(tmp_path):
    """Test della gestione dell'errore quando il file JSON non è valido"""
    # Crea un file JSON temporaneo con sintassi non valida
    json_file = tmp_path / "invalid.json"
    with open(json_file, "w", encoding="utf-8") as f:
        f.write("{ invalid json }")
    
    # Verifica che venga restituito un messaggio di errore per JSON non valido
    calc = EOQCalculator()
    results = calc.read_from_json(str(json_file))
    assert isinstance(results, list)
    assert "error" in results[0]
    assert "Formato JSON non valido" in results[0]["error"]


if __name__ == "__main__":
    # Esegui i test con output verboso
    pytest.main([__file__, "-v", "-s"])