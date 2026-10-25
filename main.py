from pprint import pprint
import csv
import json
#import sys

analyses = [
    {"nom": "glycemie", "min": 0.70, "max": 1.10, "unite": "g/L"},
    {"nom": "creatinine", "min": 50, "max": 100, "unite": "µmol/L"},
    {"nom": "uree", "min": 2.5, "max": 7.5, "unite": "mmol/L"},
    {"nom": "ldh", "min": 100, "max": 250, "unite": "U/L"}
]

def read_file (file_to_read):
    with open(file_to_read, mode="r", newline='') as csvfile:
        data = csv.DictReader(csvfile)
        list_of_data = list(data)

        for patient in list_of_data:
            for test, result in patient.items():
                if test != 'id':
                    if len(result.strip()) > 0:
                        patient[test] = float(result)
                    else:
                        patient[test] = None
    return list_of_data

def calculate_stats(patients, analyse):
    values = []
    for patient in patients:
        if patient[analyse] is not None:
            values.append(patient[analyse])
   
    if len(values) > 0:
        average = sum(values) / len(values)
        min_value = min(values)
        max_value = max(values)
    else: 
        return None

    analyse_stats = dict(moyenne=average, minimale=min_value, maximale=max_value)
    
    return analyse_stats


def detect_outliers(patients, analyse, lower_limit, upper_limit):
    outliers = []
    for patient in patients:
        if patient[analyse] is not None:
            if patient[analyse] < lower_limit or patient[analyse] > upper_limit:
                outliers.append({
                    "id": patient["id"],
                    analyse: patient[analyse]
                })
    return outliers


def generate_report(analyse, patients, stats, outliners):
    num_patients = len(patients)
    for patient in patients:
        if patient[analyse] is None:
            num_patients -= 1
    final_report = dict(
        analyse=analyse, 
        nombre_patients=num_patients,
        statistiques=stats,
        patients_hors_bornes=outliners
    )
    return final_report


patients = read_file("patients_data.csv")
pprint(patients, sort_dicts=False)
print('\n')
print('--------------------------------------------')
print('\n')

############################################
reports = []
for analyse in analyses:
    test_stats = calculate_stats(patients, analyse["nom"])
    test_outliers = detect_outliers(patients, analyse["nom"], analyse["min"], analyse["max"])
    test_report = generate_report(analyse["nom"], patients, test_stats, test_outliers)
    reports.append(test_report)
    print(f"Rapport de données concernant l'analyse {analyse['nom']} : ({analyse['unite']})")
    pprint(test_report, sort_dicts=False)
    print('\n')
    print('--------------------------------------------')
    print('\n')

print(reports)

with open("rapports.json", mode="w", encoding="utf-8") as file:
    json.dump(reports, file, ensure_ascii=False, indent=4)