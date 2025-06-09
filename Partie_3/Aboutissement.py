import math as m
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from random import randint, random

#--------------------# DONNEES D'APPLICATION #--------------------#

generateur = (50,50)

Départements = {'Ain': (2720.0, 'solaire', 14000), 'Aisne': (1750.0, 'eolien', 9000), 'Allier': (3000.0, 'solaire', 15400), 'Alpes-de-Haute-Provence': (2180.0, 'solaire', 11200), 'Hautes-Alpes': (2720.0, 'solaire', 14000), 'Alpes-Maritimes': (2450.0, 'solaire', 12600), 'Ardèche': (2720.0, 'solaire', 14000), 'Ardennes': (3540.0, 'solaire', 18200), 'Ariège': (2720.0, 'solaire', 14000), 'Aube': (2720.0, 'eolien', 14000), 'Aude': (1420.0, 'eolien', 7300), 'Aveyron': (1750.0, 'eolien', 9000), 'Bouches-du-Rhône': (1750.0, 'eolien', 9000), 'Calvados': (1750.0, 'eolien', 9000), 'Cantal': (2450.0, 'solaire', 12600), 'Charente': (2720.0, 'eolien', 14000), 'Charente-Maritime': (1120.0, 'eolien', 5700), 'Cher': (2720.0, 'eolien', 14000), 'Corrèze': (2720.0, 'solaire', 14000), 'Corse-du-Sud': (1750.0, 'eolien', 9000), 'Haute-Corse': (1750.0, 'eolien', 9000), "Côte-d'Or": (2720.0, 'eolien', 14000), "Côtes-d'Armor": (1750.0, 'eolien', 9000), 'Creuse': (3000.0, 'solaire', 15400), 'Dordogne': (2720.0, 'solaire', 14000), 'Doubs': (3000.0, 'solaire', 15400), 'Drôme': (2450.0, 'solaire', 12600), 'Eure': (1750.0, 'eolien', 9000), 'Eure-et-Loir': (2720.0, 'eolien', 14000), 'Finistère': (1120.0, 'eolien', 5700), 'Gard': (1750.0, 'eolien', 9000), 'Haute-Garonne': (2720.0, 'solaire', 14000), 'Gers': (2720.0, 'solaire', 14000), 'Gironde': (2720.0, 'solaire', 14000), 'Hérault': (1750.0, 'eolien', 9000), 'Ille-et-Vilaine': (2350.0, 'eolien', 12100), 'Indre': (3000.0, 'solaire', 15400), 'Indre-et-Loire': (2720.0, 'eolien', 14000), 'Isère': (3000.0, 'solaire', 15400), 'Jura': (3000.0, 'solaire', 15400), 'Landes': (3000.0, 'solaire', 15400), 'Loir-et-Cher': (3250.0, 'eolien', 16700), 'Loire': (2720.0, 'solaire', 14000), 'Haute-Loire': (2350.0, 'eolien', 12100), 'Loire-Atlantique': (1420.0, 'eolien', 7300), 'Loiret': (2720.0, 'eolien', 14000), 'Lot': (2720.0, 'solaire', 14000), 'Lot-et-Garonne': (2720.0, 'solaire', 14000), 'Lozère': (1750.0, 'eolien', 9000), 'Maine-et-Loire': (2720.0, 'eolien', 14000), 'Manche': (1120.0, 'eolien', 5700), 'Marne': (2350.0, 'eolien', 12100), 'Haute-Marne': (3250.0, 'eolien', 16700), 'Mayenne': (1750.0, 'eolien', 9000), 'Meurthe-et-Moselle': (3250.0, 'eolien', 16700), 'Meuse': (2720.0, 'eolien', 14000), 'Morbihan': (2350.0, 'eolien', 12100), 'Moselle': (2350.0, 'eolien', 12100), 'Nièvre': (3270.0, 'solaire', 16800), 'Nord': (1420.0, 'eolien', 7300), 'Oise': (2350.0, 'eolien', 12100), 'Orne': (2350.0, 'eolien', 12100), 'Pas-de-Calais': (1420.0, 'eolien', 7300), 'Puy-de-Dôme': (2720.0, 'solaire', 14000), 'Pyrénées-Atlantiques': (3000.0, 'solaire', 15400), 'Hautes-Pyrénées': (2720.0, 'solaire', 14000), 'Pyrénées-Orientales': (2180.0, 'solaire', 11200), 'Bas-Rhin': (3270.0, 'solaire', 16800), 'Haut-Rhin': (3000.0, 'solaire', 15400), 'Rhône': (2350.0, 'eolien', 12100), 'Haute-Saône': (3250.0, 'eolien', 16700), 'Saône-et-Loire': (3000.0, 'solaire', 15400), 'Sarthe': (2350.0, 'eolien', 12100), 'Savoie': (2450.0, 'solaire', 12600), 'Haute-Savoie': (2720.0, 'solaire', 14000), 'Paris': (1750.0, 'eolien', 9000), 'Seine-Maritime': (1420.0, 'eolien', 7300), 'Seine-et-Marne': (3250.0, 'eolien', 16700), 'Yvelines': (2350.0, 'eolien', 12100), 'Deux-Sèvres': (2350.0, 'eolien', 12100), 'Somme': (1420.0, 'eolien', 7300), 'Tarn': (2350.0, 'eolien', 12100), 'Tarn-et-Garonne': (2720.0, 'solaire', 14000), 'Var': (1750.0, 'eolien', 9000), 'Vaucluse': (1750.0, 'eolien', 9000), 'Vendée': (1750.0, 'eolien', 9000), 'Vienne': (2720.0, 'eolien', 14000), 'Haute-Vienne': (3000.0, 'solaire', 15400), 'Vosges': (3250.0, 'eolien', 16700), 'Yonne': (3270.0, 'solaire', 16800), 'Territoire de Belfort': (3000.0, 'solaire', 15400), 'Essonne': (2720.0, 'eolien', 14000), 'Hauts-de-Seine': (3270.0, 'solaire', 16800), 'Seine-Saint-Denis': (2350.0, 'eolien', 12100), 'Val-de-Marne': (2350.0, 'eolien', 12100), "Val-d'Oise": (1750.0, 'eolien', 9000)}
n_generations = 100
n_individus = 100
n_transformateurs_max = 10

Fond_satellitaire   = "TIPE/Partie_3/Images/satellitaire.png"
Icone_maison        = "TIPE/Partie_3/Images/maison.png"
Icone_solaire       = "TIPE/Partie_3/Images/solaire.png"
Icone_eolien        = "TIPE/Partie_3/Images/eolien.png"

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

#----------------------------------------# SELECTION DU DEPARTEMENT #----------------------------------------#

for Département_nom in Départements.keys():
    print(f"- {Département_nom}")

Département_choisi = ""
while Département_choisi not in Départements:
    Département_choisi = input("Département : ")

#--------------------# PLACEMENT DES MAISONS #--------------------#

def placement_maisons():
    coordonnees = []
    fig, ax = plt.subplots(figsize=(7, 7))
    img = plt.imread(Fond_satellitaire)
    ax.imshow(img, extent=[0, 100, 0, 100])
    ax.axis('off')
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    def clic(event):
        x, y = (round(v) for v in (event.xdata, event.ydata))
        coordonnees.append((x, y))
        ax.plot(x, y, 'bo', markersize=5)
        fig.canvas.draw()

    clic = fig.canvas.mpl_connect('button_press_event', clic)
    plt.show()
    fig.canvas.mpl_disconnect(clic)
    return coordonnees

maisons = placement_maisons()

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

maisons_deconnectees_log = [] 

meilleure_config_finale_stable = []
pertes_minimales_finale_stable = float('inf')
transformateurs_optimaux_finaux_stable = []

icone_energie_definie_par_dept = Départements[Département_choisi][1]

while True:
    
    # Etape 1: Optimisation du réseau avec les maisons actuellement dans la liste globale `maisons`
    
    current_config_optimale, current_pertes, current_transformateurs = Comparaison_Finale()
    changements_cette_iteration = False 
    transformateurs_pour_suite_iteration = list(current_transformateurs)
    maisons_candidates_reseau_apres_regles = list(maisons) 

    # Etape 2: Appliquer la règle "moins de 3 maisons par transformateur"

    if current_transformateurs:
        maisons_connectees_par_transfo_actuel = {} 

        for m_coord in maisons_candidates_reseau_apres_regles: 
            if not current_transformateurs: break
            
            distances_a_transfos_actuels = [distance(m_coord[0], m_coord[1], t[0], t[1]) for t in current_transformateurs]
            if not distances_a_transfos_actuels: continue

            idx_transfo_proche = distances_a_transfos_actuels.index(min(distances_a_transfos_actuels))
            transfo_proche_tuple = tuple(current_transformateurs[idx_transfo_proche])
            
            if transfo_proche_tuple not in maisons_connectees_par_transfo_actuel:
                maisons_connectees_par_transfo_actuel[transfo_proche_tuple] = []
            maisons_connectees_par_transfo_actuel[transfo_proche_tuple].append(m_coord)

        transformateurs_a_supprimer_suite_a_regle_3 = []

        for transfo_coord_tuple, maisons_liees in maisons_connectees_par_transfo_actuel.items():
            if len(maisons_liees) < 4:
                transformateurs_a_supprimer_suite_a_regle_3.append(list(transfo_coord_tuple))
                changements_cette_iteration = True

                for m_a_convertir in maisons_liees:
                    if m_a_convertir in maisons_candidates_reseau_apres_regles: 
                        maisons_candidates_reseau_apres_regles.remove(m_a_convertir)
                        maisons_deconnectees_log.append({'coords': m_a_convertir, 'icone_type': icone_energie_definie_par_dept})
        
        if transformateurs_a_supprimer_suite_a_regle_3:
            temp_transformateurs_apres_regle_3 = []
            for t_original in current_transformateurs: 
                if list(t_original) not in transformateurs_a_supprimer_suite_a_regle_3:
                    temp_transformateurs_apres_regle_3.append(t_original)
            transformateurs_pour_suite_iteration = temp_transformateurs_apres_regle_3
    
    # Etape 3: Logique de déconnexion par distance maximale autorisée
    
    maisons_a_verifier_pour_distance = list(maisons_candidates_reseau_apres_regles)
    distance_max_autorisee = Départements[Département_choisi][0]*Echelle/100

    if not transformateurs_pour_suite_iteration: 
        for m_coord in maisons_a_verifier_pour_distance: 
            if m_coord in maisons_candidates_reseau_apres_regles: 
                maisons_candidates_reseau_apres_regles.remove(m_coord) 
            maisons_deconnectees_log.append({'coords': m_coord, 'icone_type': icone_energie_definie_par_dept})
            changements_cette_iteration = True 
    else: 
        for m_coord in maisons_a_verifier_pour_distance:
            min_dist_maison_transfo = min(distance(m_coord[0], m_coord[1], t_pos[0], t_pos[1]) for t_pos in transformateurs_pour_suite_iteration)
            if min_dist_maison_transfo > distance_max_autorisee:
                if m_coord in maisons_candidates_reseau_apres_regles: 
                    maisons_candidates_reseau_apres_regles.remove(m_coord) 
                maisons_deconnectees_log.append({'coords': m_coord, 'icone_type': icone_energie_definie_par_dept})
                changements_cette_iteration = True

    maisons.clear()
    maisons.extend(maisons_candidates_reseau_apres_regles)

    # Etape 4: Décider si la boucle doit continuer et stocker la configuration stable

    if not changements_cette_iteration:
        transformateurs_optimaux_finaux_stable = list(transformateurs_pour_suite_iteration) 

        if maisons and transformateurs_optimaux_finaux_stable:
            meilleure_config_finale_stable, pertes_minimales_finale_stable = evaluer_reseau(transformateurs_optimaux_finaux_stable)
        elif maisons and not transformateurs_optimaux_finaux_stable: 
            for m_coord_restante in list(maisons): 
                 maisons_deconnectees_log.append({'coords': m_coord_restante, 'icone_type': icone_energie_definie_par_dept})
            maisons.clear() 
            meilleure_config_finale_stable = []
            pertes_minimales_finale_stable = 0
            transformateurs_optimaux_finaux_stable = []
        else: 
            meilleure_config_finale_stable = []
            pertes_minimales_finale_stable = 0
            transformateurs_optimaux_finaux_stable = []
            
        break

#--------------------# REPRESENTATION DU SYSTEME #--------------------#

Image_Icone_maison      = plt.imread(Icone_maison)
Image_Icone_solaire     = plt.imread(Icone_solaire)
Image_Icone_eolien      = plt.imread(Icone_eolien)
Image_Fond_Satellitaire = plt.imread(Fond_satellitaire)

def voir_reseau(config_elements_final, transfos_final_pos, maisons_deconnectees_final_details, nom_dept_final):

    fig_resultat, ax_resultat = plt.subplots(figsize=(7, 7))
    ax_resultat.imshow(Image_Fond_Satellitaire, extent=[0, 100, 0, 100])

    icon_zoom = 0.25

    ax_resultat.plot(generateur[0], generateur[1], 'gs')

    if transfos_final_pos:
        for tx, ty in transfos_final_pos:
            ax_resultat.plot(tx, ty, 'ro')
            ax_resultat.plot([generateur[0], tx], [generateur[1], ty], 'r--')

    maisons_connectees_final_coords = []
    if config_elements_final:
        for type_el, coords_el in config_elements_final:
            if type_el == 'maison':
                maisons_connectees_final_coords.append(coords_el)

    for mx, my in maisons_connectees_final_coords:
        ab = AnnotationBbox(OffsetImage(Image_Icone_maison, zoom=icon_zoom), (mx, my), frameon=False)
        ax_resultat.add_artist(ab)
        if transfos_final_pos:
            dist_sq_min_val = float('inf')
            transfo_proche_final_coords = None
            for tx, ty in transfos_final_pos:
                dist_sq_calc = ((mx-tx)**2 + (my-ty)**2)
                if dist_sq_calc < dist_sq_min_val:
                    dist_sq_min_val = dist_sq_calc
                    transfo_proche_final_coords = (tx, ty)
            if transfo_proche_final_coords:
                ax_resultat.plot([mx, transfo_proche_final_coords[0]], [my, transfo_proche_final_coords[1]], 'b--', linewidth=1)

    for maison_info_dc in maisons_deconnectees_final_details:
        dmx, dmy = maison_info_dc['coords']
        icon_type_dc = maison_info_dc['icone_type']
        image_icone_maison_deconnectee = Image_Icone_maison
        if icon_type_dc == 'solaire':
            image_icone_maison_deconnectee = Image_Icone_solaire
        elif icon_type_dc == 'eolien':
            image_icone_maison_deconnectee = Image_Icone_eolien

        ab = AnnotationBbox(OffsetImage(image_icone_maison_deconnectee, zoom=icon_zoom), (dmx, dmy), frameon=False)
        ax_resultat.add_artist(ab)

    ax_resultat.set_xlim(0, 100)
    ax_resultat.set_ylim(0, 100)
    ax_resultat.axis('off')
    fig_resultat.subplots_adjust(left=0, right=1, top=1, bottom=0)

    plt.show()

voir_reseau(meilleure_config_finale_stable, transformateurs_optimaux_finaux_stable, maisons_deconnectees_log, Département_choisi)