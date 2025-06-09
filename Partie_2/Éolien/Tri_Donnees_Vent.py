import csv
import gzip
from collections import defaultdict
from datetime import datetime
import os
import openpyxl

def Un_Fichier_csv(Fichier):
    with gzip.open(Fichier, 'rt', encoding='utf-8') as f:
        contenu = f.read()

        f.seek(0)
        dialect = csv.Sniffer().sniff(contenu[:1024])
        f.seek(0)
        
        reader = csv.DictReader(f, dialect=dialect)
        données = [row for row in reader if 'FFM' in row and row['FFM'].strip()]
        
        if not données:
            print(f"Aucune donnée dans {Fichier}")
            return None
        
        stations = defaultdict(list)
        for ligne in données:
            try:
                nom_usuel = ligne['NOM_USUEL']
                ffm = float(ligne['FFM'])
                stations[nom_usuel].append(ffm)
            except (ValueError, KeyError):
                continue
        
        if not stations:
            print(f"Aucune station valide dans {Fichier}")
            return None
        
        moyennes_par_station = []
        for ffms in stations.values():
            if ffms:
                moyennes_par_station.append(sum(ffms) / len(ffms))
        
        if not moyennes_par_station:
            print(f"Aucune moyenne station dans {Fichier}")
            return None
        
        moyenne_ffm = sum(moyennes_par_station) / len(moyennes_par_station)
        return moyenne_ffm

def Tous_les_fichiers():
    doc = openpyxl.Workbook()
    colonne = doc.active
    colonne['A1'] = "Département"
    colonne['B1'] = "Moyenne FFM"

    ligne = 2
    fichiers = sorted(os.listdir("TIPE/Partie_2/Éolien/Données"))
    for fichier in fichiers:
        if fichier.startswith("MENSQ_") and fichier.endswith("_previous-1950-2022.csv.gz"):
            fichier_input = os.path.join("TIPE/Partie_2/Éolien/Données", fichier)
            moyenne_ffm = Un_Fichier_csv(fichier_input)
            colonne[f'A{ligne}'] = fichier
            if moyenne_ffm is not None:
                colonne[f'B{ligne}'] = round(moyenne_ffm, 2)
            ligne += 1

    doc.save("TIPE/Partie_2/Éolien/output.xlsx")

Tous_les_fichiers()