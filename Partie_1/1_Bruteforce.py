import math as m
import matplotlib.pyplot as plt
from itertools import combinations
from pandas import read_excel

#--------------------# DONNEES D'APPLICATION #--------------------#

excel = read_excel("TIPE/Partie_1/Maisons/Maisons.xlsx")
maisons = [(row['x'], row['y']) for _, row in excel.iterrows()]
generateur = (5,5)

max_transformateurs = 3

Echelle = 15000

#--------------------# EVALUATION DES PERTES #--------------------#

def distance(x1, y1, x2, y2):
    return m.sqrt(((x2 - x1)*Echelle)**2 + ((y2 - y1)*Echelle)**2)

def perte_cable_HT(d):
    return 0.002 * d

def perte_cable_BT(d):
    return 0.005 * d

def perte_transformateur():
    return 345

#--------------------# DETERMINATION DES PERTES D'UNE CONFIGURATION DONNEE #--------------------#

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

#--------------------# BRUTEFORCE DES CONFIGURATIONS POSSIBLES #--------------------#

def optimiser_reseau():
    pertes_minimales = float('inf')
    meilleure_configuration = None
    meilleurs_transformateurs = []

    x_min = min(maison[0] for maison in maisons)
    x_max = max(maison[0] for maison in maisons)
    y_min = min(maison[1] for maison in maisons)
    y_max = max(maison[1] for maison in maisons)

    positions_transformateurs = [(x, y) for x in range(x_min, x_max + 1) for y in range(y_min, y_max + 1) if (x, y) not in maisons]

    for i in range(1, max_transformateurs + 1):
        for transformateurs in combinations(positions_transformateurs, i):
            configuration, perte_config = evaluer_reseau(transformateurs)

            if perte_config < pertes_minimales:
                pertes_minimales = perte_config
                meilleure_configuration = configuration
                meilleurs_transformateurs = transformateurs

    return meilleure_configuration, pertes_minimales, meilleurs_transformateurs

#--------------------# MISE EN ROUTE #--------------------#

configuration_optimale, pertes, transformateurs_optimaux = optimiser_reseau()

#--------------------# REPRESENTATION DU SYSTEME #--------------------#

def voir_reseau(generateur, maisons, transformateurs_optimaux):
    plt.subplots(figsize=(7, 7))
    plt.plot(generateur[0], generateur[1], 'gs')

    for maison in maisons:
        plt.plot(maison[0], maison[1], 'b^')

    for transformateur in transformateurs_optimaux:
        plt.plot(transformateur[0], transformateur[1], 'ro')

    for transformateur in transformateurs_optimaux:
        plt.plot([generateur[0], transformateur[0]], [generateur[1], transformateur[1]], 'r--')

    for maison in maisons:
        distances_transformateurs = [distance(maison[0], maison[1], transformateur[0], transformateur[1]) for transformateur in transformateurs_optimaux]
        transformateur_proche = transformateurs_optimaux[distances_transformateurs.index(min(distances_transformateurs))]
        plt.plot([maison[0], transformateur_proche[0]], [maison[1], transformateur_proche[1]], 'b--')

    plt.show()

voir_reseau(generateur, maisons, transformateurs_optimaux)