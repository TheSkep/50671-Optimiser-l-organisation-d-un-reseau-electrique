import math as m
import pandas as pd

excel = pd.read_excel("TIPE/Partie_2/Bilan.xlsx")
excel.columns = ["Colonne1", "Colonne2", "Colonne3"]
Département = {row["Colonne1"]: [row["Colonne2"], row["Colonne3"]] for _, row in excel.iterrows()}
# { "Département" : [vitesse_vent_moyen (m/s), efficacité_solaire (kWh/(kWc*an))]

#--------------------# ESTIMATION DES DIMENSIONS DES SOURCES LOCALES PAR FOYER #--------------------#

Conso_Foyer = 6000 # kWh/an

def estimer_eolienne(vitesse_vent):
    rayon = m.sqrt((2 * Conso_Foyer * 1000) / (1.23 * m.pi * vitesse_vent**3 * 8766))
    return rayon

def estimer_panneaux(intensite_solaire):
    panneau_solaire_500Wc = 0.5 # kWc
    nombre_cellules = Conso_Foyer / (panneau_solaire_500Wc * intensite_solaire)
    return nombre_cellules

#--------------------# ESTIMATION DU COUT D'INSTALLATION DES SOURCES LOCALES #--------------------#

Cout_eolienne_diametre = {
    '2m': 3600,     '3m': 4500,     '4m': 5700,     '5m': 7300, 
    '6m': 9000,     '7m': 12100,    '8m': 14000,    '9m': 16700, 
    '10m': 19300    
}
Cout_solaire_unite = 1400 # €

def estimer_cout_eolien(rayon):
    diametre_arrondi = m.ceil(rayon * 2)
    if f"{diametre_arrondi}m" in Cout_eolienne_diametre:
        cout_eolien = Cout_eolienne_diametre[f"{diametre_arrondi}m"]
    else:
        cout_eolien = float('inf')
    return cout_eolien # €

def estimer_cout_solaire(nombre_cellules):
    nombre_arrondi = m.ceil(nombre_cellules)
    cout_solaire = nombre_arrondi * Cout_solaire_unite
    return cout_solaire # €

#--------------------# CHOIX DE LA SOURCE LOCALE LA PLUS RENTABLE PAR REGION #--------------------#

def comparer_couts_par_departement(Départements):
    couts_par_region = {}
    
    for Département in Départements:
        valeurs = Départements[Département]
        vitesse_vent, efficacite_solaire = valeurs
        
        rayon_eolienne = estimer_eolienne(vitesse_vent)
        cout_eolien = estimer_cout_eolien(rayon_eolienne)
        
        nombre_panneaux = estimer_panneaux(efficacite_solaire)
        cout_solaire = estimer_cout_solaire(nombre_panneaux)

        if cout_eolien < cout_solaire:
            couts_par_region[Département] = ('eolien', cout_eolien)
        else:
            couts_par_region[Département] = ('solaire', cout_solaire)
    
    return couts_par_region

#--------------------# CALCUL DE LA DISTANCE DE RENTABILITE SUR 10 ANS #--------------------#

def couts_pertes_reseau(distance):
    heures_10ans = 365.25 * 24 * 10
    return 2.35*10**-4 * distance * heures_10ans * 1000 * 0.25 # €/10ans

def determiner_distance(departements):
    cout_local_par_departement = comparer_couts_par_departement(departements)
    distance_par_region = {}
    
    for departement in departements:
        type_energie, cout_local = cout_local_par_departement[departement]
        distance = 0
        
        while True:
            cout_pertes = couts_pertes_reseau(distance)
            if cout_pertes >= cout_local:
                distance_par_region[departement] = distance
                break
            distance += 0.01
            distance = m.ceil(distance*100)/100

    return distance_par_region

#--------------------# AFFICHAGE DES RESULTATS PAR REGION #--------------------#

conclusion = {}

def afficher_valeurs_par_region(Départements):
    cout_local_par_region = comparer_couts_par_departement(Départements)
    distance_par_region = determiner_distance(Départements)
    
    for Département in Départements:
        type_energie, cout_local = cout_local_par_region[Département]
        distance = distance_par_region[Département] * 1000       
        conclusion[f"{Département}"]=distance,type_energie,cout_local
    return conclusion

print(afficher_valeurs_par_region(Département))