import math
import os
import json
import pytest

from EOQ_calculator_beta4 import EOQ_calculator

def test_eoq_calculate_basic():
    calc = EOQ_calculator()
    calc.anno = 2024
    calc.domanda_annua = 1000
    calc.costo_setup = 50
    calc.costo_mantenimento = 2
    calc.calculate()
    # EOQ = sqrt((2*1000*50)/2) = sqrt(50000) = 223.606...
    assert math.isclose(calc.eoq, math.sqrt(50000), rel_tol=1e-6)
    # Costi ordinazione = (1000/EOQ)*50
    assert math.isclose(calc.costi_ordinazione, (1000/calc.eoq)*50, rel_tol=1e-6)
    # Costi mantenimento = (EOQ/2)*2
    assert math.isclose(calc.costi_mantenimento, (calc.eoq/2)*2, rel_tol=1e-6)
    # Costi totali = somma
    assert math.isclose(calc.costi_totali, calc.costi_ordinazione + calc.costi_mantenimento, rel_tol=1e-6)
    # Ordini annui = 1000/EOQ
    assert math.isclose(calc.ordini_annui, 1000/calc.eoq, rel_tol=1e-6)
    # Tempo tra ordini = 365/ordini_annui
    assert math.isclose(calc.tempo_tra_ordini, 365/calc.ordini_annui, rel_tol=1e-6)

def test_get_results_dict_format():
    calc = EOQ_calculator()
    calc.anno = 2023
    calc.domanda_annua = 500
    calc.costo_setup = 20
    calc.costo_mantenimento = 1
    calc.calculate()
    result = calc.get_results_dict()
    assert result["Anno"] == 2023
    assert isinstance(result["EOQ (pz)"], int)
    assert isinstance(result["Costo Ordini (€)"], str)
    assert isinstance(result["Costo Magazzino (€)"], str)
    assert isinstance(result["Costo Totale (€)"], str)
    assert isinstance(result["Ordini/Anno"], int)
    assert isinstance(result["Giorni tra ordini"], int)

def test_calcolate_from_json_valid(tmp_path):
    # Prepare a valid JSON file
    data = [
        {"anno": 2022, "domanda_annua": 1000, "costo_setup": 40, "costo_mantenimento": 2},
        {"anno": 2023, "domanda_annua": 2000, "costo_setup": 50, "costo_mantenimento": 4}
    ]
    json_file = tmp_path / "test_dati.json"
    with open(json_file, "w") as f:
        json.dump(data, f)
    calc = EOQ_calculator()
    results = calc.calcolate_from_json(str(json_file))
    assert isinstance(results, list)
    assert len(results) == 2
    assert results[0]["Anno"] == 2022
    assert results[1]["Anno"] == 2023
    assert "EOQ (pz)" in results[0]
    assert "Costo Totale (€)" in results[1]

def test_calcolate_from_json_invalid_file():
    calc = EOQ_calculator()
    results = calc.calcolate_from_json("nonexistent_file.json")
    assert isinstance(results, list)
    assert "error" in results[0]
    assert "non è stato trovato" in results[0]["error"]

def test_calcolate_from_json_invalid_json(tmp_path):
    # Prepare an invalid JSON file
    json_file = tmp_path / "invalid.json"
    with open(json_file, "w") as f:
        f.write("{invalid json}")
    calc = EOQ_calculator()
    results = calc.calcolate_from_json(str(json_file))
    assert isinstance(results, list)
    assert "error" in results[0]
    assert "Formato JSON non valido" in results[0]["error"]

def test_calcolate_from_json_with_invalid_values(tmp_path):
    # Some records have invalid (zero or negative) values
    data = [
        {"anno": 2020, "domanda_annua": 0, "costo_setup": 10, "costo_mantenimento": 1},
        {"anno": 2021, "domanda_annua": 100, "costo_setup": -5, "costo_mantenimento": 1},
        {"anno": 2022, "domanda_annua": 100, "costo_setup": 10, "costo_mantenimento": 1}
    ]
    json_file = tmp_path / "test_invalid_values.json"
    with open(json_file, "w") as f:
        json.dump(data, f)
    calc = EOQ_calculator()
    results = calc.calcolate_from_json(str(json_file))
    # Only the last record is valid
    assert len(results) == 1
    assert results[0]["Anno"] == 2022

if __name__ == "__main__":
    pytest.main()