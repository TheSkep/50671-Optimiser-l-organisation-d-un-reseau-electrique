import math as m
import matplotlib.pyplot as plt
from random import randint, random
from pandas import read_excel

#--------------------# DONNEES D'APPLICATION #--------------------#

excel = read_excel("TIPE/Partie_1/Maisons/Maisons_100.xlsx")
maisons = [(row['x'], row['y']) for _, row in excel.iterrows()]
generateur = (50,50)

n_generations = 100
n_individus = 100
n_transformateurs_max = 10

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

#--------------------# CREATION D'UNE POPULATION DE TRANSFORMATEURS #--------------------#

def creer_individu(positions_transformateurs, n_transformateurs):
    individu = []
    positions_disponibles = positions_transformateurs[:]
    
    for _ in range(n_transformateurs):

        index = randint(0, len(positions_disponibles) - 1)
        transformateur = positions_disponibles.pop(index)
        individu.append(transformateur)

    return individu

def creer_population(positions_transformateurs, n_transformateurs):
    return [creer_individu(positions_transformateurs, n_transformateurs) for _ in range(n_individus)]

#--------------------# EVALUATION DES PERTES D'UN INDIVIDU #--------------------#

def evaluer_individu(individu):
    configuration, perte = evaluer_reseau(individu)
    return perte

#--------------------# SELECTION DE LA MEILLEURE MOITIE DE LA POPULATION #--------------------#

def selection(population):
    evaluations = [(individu, evaluer_individu(individu)) for individu in population]
    evaluations.sort(key=lambda x: x[1])
    parents = [individu for individu, _ in evaluations[:len(population)//2]]
    return parents

#--------------------# HEREDITE ET MUTATIONS #--------------------#

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

#--------------------# OBTENTION DE LA MEILLEURE CONFIGURATION POUR N TRANSFORMATEURS #--------------------#

def optimiser_reseau(n_transformateurs):
    x_min = min(maison[0] for maison in maisons)
    x_max = max(maison[0] for maison in maisons)
    y_min = min(maison[1] for maison in maisons)
    y_max = max(maison[1] for maison in maisons)
    
    positions_transformateurs = [(x, y) for x in range(x_min, x_max + 1) for y in range(y_min, y_max + 1) if (x, y) not in maisons]

    population = creer_population(positions_transformateurs, n_transformateurs)
    meilleur_score = float('inf')
    meilleur_individu = None

    for _ in range(n_generations):
        parents = selection(population)
        
        for individu in parents:
            score = evaluer_individu(individu)
            if score < meilleur_score:
                meilleur_score = score
                meilleur_individu = individu[:]

        enfants = []
        for j in range(0, len(parents) - 1, 2):
            parent1, parent2 = parents[j], parents[j+1]
            enfant1, enfant2 = croisement(parent1, parent2)
            
            if random() < 0.15:
                enfant1 = mutation(enfant1, positions_transformateurs)
            if random() < 0.15:
                enfant2 = mutation(enfant2, positions_transformateurs)
                
            enfants.extend([enfant1, enfant2])
        
        population = parents + enfants

    meilleure_configuration, pertes_totales = evaluer_reseau(meilleur_individu)

    return meilleure_configuration, pertes_totales, meilleur_individu

#--------------------# COMPARAISON DES CONFIGURATIONS SELON LE NOMBRE DE TRANSFORMATEURS #--------------------#

def Comparaison_Finale():
    meilleure_configuration = None
    pertes_minimales = float('inf')
    transformateurs_optimaux = []

    for n_transformateurs in range(1, n_transformateurs_max + 1):
        configuration_optimale, pertes, meilleurs_transformateurs = optimiser_reseau(n_transformateurs)

        if pertes < pertes_minimales:
            meilleure_configuration = configuration_optimale
            pertes_minimales = pertes
            transformateurs_optimaux = meilleurs_transformateurs

    return meilleure_configuration, pertes_minimales, transformateurs_optimaux

#----------------------------------------# MISE EN ROUTE #----------------------------------------#

configuration_optimale, pertes, transformateurs_optimaux = Comparaison_Finale()

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