import math as m
import matplotlib.pyplot as plt
from itertools import combinations
from random import randint, random
from pandas import read_excel
import time
import numpy as np

#--------------------# DONNÉES D'APPLICATION #--------------------#

excel = read_excel("TIPE/Partie_1/Maisons/Maisons.xlsx")
maisons = [(row['x'], row['y']) for _, row in excel.iterrows()]
generateur = (0, 0)

#--------------------# PARAMÈTRES #--------------------#

n_generations = 110
n_transformateurs_max = 3
liste_n_individus = [10, 25, 50, 75, 100]
n_échantillon = 200

#--------------------# FONCTIONS COMMUNES #--------------------#

def distance(x1, y1, x2, y2):
    return m.sqrt((x2 - x1)**2 + (y2 - y1)**2) * 500

def perte_cable_HT(d):
    return 0.2 * d

def perte_cable_BT(d):
    return 0.5 * d

def perte_transformateur():
    return 5

def evaluer_reseau(transformateurs):
    configuration = []
    perte_config = 0

    for transformateur in transformateurs:
        d_transformateur = distance(generateur[0], generateur[1], transformateur[0], transformateur[1])
        perte_transformateur_i = perte_cable_HT(d_transformateur) + perte_transformateur()
        configuration.append(('transformateur', transformateur))
        perte_config += perte_transformateur_i

    for maison in maisons:
        distances_transformateurs = [distance(maison[0], maison[1], transformateur[0], transformateur[1]) for transformateur in transformateurs]
        transformateur_proche = transformateurs[distances_transformateurs.index(min(distances_transformateurs))]
        d_maison = distance(maison[0], maison[1], transformateur_proche[0], transformateur_proche[1])
        perte_maison = perte_cable_BT(d_maison)
        configuration.append(('maison', maison))
        perte_config += perte_maison

    return configuration, perte_config

#--------------------# ALGORITHME BRUTEFORCE #--------------------#

def optimiser_reseau_bruteforce():
    start_time = time.time()
    pertes_totales = float('inf')
    meilleure_configuration = None
    meilleurs_transformateurs = []

    x_min = min(maison[0] for maison in maisons)
    x_max = max(maison[0] for maison in maisons)
    y_min = min(maison[1] for maison in maisons)
    y_max = max(maison[1] for maison in maisons)

    positions_transformateurs = [(x, y) for x in range(x_min, x_max + 1) for y in range(y_min, y_max + 1) if (x, y) not in maisons]

    configurations_testees = 0
    for i in range(1, n_transformateurs_max + 1):
        for transformateurs in combinations(positions_transformateurs, i):
            configurations_testees += 1
            configuration, perte_config = evaluer_reseau(transformateurs)

            if perte_config < pertes_totales:
                pertes_totales = perte_config
                meilleure_configuration = configuration
                meilleurs_transformateurs = transformateurs
    
    execution_time = time.time() - start_time
    return meilleure_configuration, pertes_totales, meilleurs_transformateurs, execution_time, configurations_testees

perte_bf, temps_bf = optimiser_reseau_bruteforce()[1], optimiser_reseau_bruteforce()[3]

#--------------------# GÉNÉTIQUE AVEC HISTORIQUE #--------------------#

def creer_individu(positions_transformateurs, n_transformateurs):
    individu = []
    positions_disponibles = positions_transformateurs[:]
    
    for _ in range(n_transformateurs):

        index = randint(0, len(positions_disponibles) - 1)
        transformateur = positions_disponibles.pop(index)
        individu.append(transformateur)

    return individu

def creer_population(positions, n_individus, n_transformateurs_max):
    return [creer_individu(positions, n_transformateurs_max) for _ in range(n_individus)]

def evaluer_individu(individu):
    configuration, perte = evaluer_reseau(individu)
    return perte

def selection(population):
    evaluations = [(individu, evaluer_individu(individu)) for individu in population]
    evaluations.sort(key=lambda x: x[1])
    parents = [individu for individu, _ in evaluations[:len(population)//2]]
    return parents

def croisement(parent1, parent2):
    if len(parent1) == 1:
        return parent1[:], parent2[:]

    point_croisement = randint(1, len(parent1) - 1)

    enfant1 = parent1[:point_croisement] + [x for x in parent2[point_croisement:] if x not in parent1[:point_croisement]]
    enfant2 = parent2[:point_croisement] + [x for x in parent1[point_croisement:] if x not in parent2[:point_croisement]]

    return enfant1, enfant2

def mutation(individu, positions_transformateurs):
    index = randint(0, len(individu) - 1)
    positions_disponibles = positions_transformateurs

    nouvelle_position = positions_disponibles[randint(0, len(positions_transformateurs) - 1)]
    individu[index] = nouvelle_position

    return individu

def optimiser_reseau_genetique(n_individus):
    x_min = min(maison[0] for maison in maisons)
    x_max = max(maison[0] for maison in maisons)
    y_min = min(maison[1] for maison in maisons)
    y_max = max(maison[1] for maison in maisons)
    positions_transformateurs = [(x, y) for x in range(x_min, x_max + 1) for y in range(y_min, y_max + 1) if (x, y) not in maisons]

    population = creer_population(positions_transformateurs, n_individus, n_transformateurs_max)
    meilleur_score = float('inf')
    meilleur_individu = None

    Historique_Pertes = []
    Historique_Temps = []
    start_all = time.time()

    for _ in range(n_generations):
        parents = selection(population)

        for individu in parents:
            score = evaluer_individu(individu)
            if score < meilleur_score:
                meilleur_score = score
                meilleur_individu = individu[:]
        
        Historique_Pertes.append(meilleur_score)
        Historique_Temps.append(time.time() - start_all)

        enfants = []
        for j in range(0, len(parents) - 1, 2):
            parent1, parent2 = parents[j], parents[j+1]
            enfant1, enfant2 = croisement(parent1, parent2)
            
            if random() < 0.2:
                enfant1 = mutation(enfant1, positions_transformateurs)
            if random() < 0.2:
                enfant2 = mutation(enfant2, positions_transformateurs)
                
            enfants.extend([enfant1, enfant2])

        population = parents + enfants

    total_time = time.time() - start_all
    return Historique_Pertes, Historique_Temps, total_time

#--------------------# TRACÉS #--------------------#

int_moy_glis = 8

donnees_moyennes_pertes = {}
donnees_moyennes_temps = {}

for n_individus_config in liste_n_individus:
    accumulateur_historique_pertes = []
    accumulateur_historique_temps = []
    for _ in range(n_échantillon):
        Historique_Pertes_run, Historique_Temps_run, _ = optimiser_reseau_genetique(n_individus_config)
        accumulateur_historique_pertes.append(Historique_Pertes_run)
        accumulateur_historique_temps.append(Historique_Temps_run)
    
    donnees_moyennes_pertes[n_individus_config] = np.mean(accumulateur_historique_pertes, axis=0)
    donnees_moyennes_temps[n_individus_config] = np.mean(accumulateur_historique_temps, axis=0)

# --- Graphique 1 : Fiabilité --- #
fig1, ax1 = plt.subplots(figsize=(7, 7))
for n_individus in liste_n_individus:
    Historique_Pertes_Moyen = donnees_moyennes_pertes[n_individus]
    Fiabilité = [perte_bf / Pertes_Moyen_Gen * 100 for Pertes_Moyen_Gen in Historique_Pertes_Moyen]
    Fiabilité_Lissée = np.convolve(Fiabilité, np.ones(int_moy_glis)/int_moy_glis, mode='same')

    Précision = [100 - valeur for valeur in Fiabilité_Lissée]
    ax1.plot(range(1, n_generations+1), Précision, label=f"n={n_individus}")

ax1.set_ylim(0, 105)
ax1.set_xlim(0, 105)
ax1.grid(True)
ax1.legend()
plt.show()

# --- Graphique 2 : Temps d’exécution --- #
fig2, ax2 = plt.subplots(figsize=(7, 7))
for n_individus in liste_n_individus:
    Historique_Temps_Moyen = donnees_moyennes_temps[n_individus]
    Temps = [t / temps_bf * 100 for t in Historique_Temps_Moyen]
    Temps_Lissé = np.convolve(Temps, np.ones(int_moy_glis)/int_moy_glis, mode='same')
    ax2.plot(range(1, n_generations+1), Temps_Lissé, label=f"n={n_individus}")

ax2.set_ylim(0, 105)
ax2.set_xlim(0, 105)
ax2.grid(True)
ax2.legend()
plt.show()