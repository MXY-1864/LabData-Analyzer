

glycemies = [0.65, 0.92, 1.15, 0.78, 1.32, 0.88]

def calculate_average(valeurs):
    average = round(sum(valeurs) / len(valeurs), 2)
    return average

def filter_values(valeurs, seuil):
    valeurs_elevees = []
    for valeur in valeurs:
        if valeur > seuil:
            valeurs_elevees.append(valeur)
    return valeurs_elevees


def create_report(moyenne, valeurs_elevees):
    report = dict(
        moyenne=moyenne,
        nombre_valeurs_elevees=len(valeurs_elevees),
        valeurs_elevees=valeurs_elevees
    )
    return report

average_glycemies = calculate_average(glycemies)
valeurs_elevees_glycemie = filter_values(glycemies, 1.10)
glycemie_report = create_report(average_glycemies, valeurs_elevees_glycemie)
print(glycemie_report)