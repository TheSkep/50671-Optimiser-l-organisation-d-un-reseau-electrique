import math as m
import matplotlib.pyplot as plt
from pandas import read_excel

excel = read_excel("TIPE/Partie_1/Maisons/Maisons.xlsx")
maisons = [(row['x'], row['y']) for _, row in excel.iterrows()]
generateur = (5,5)

def voir_reseau(generateur, maisons):
    plt.subplots(figsize=(7, 7))
    plt.plot(generateur[0], generateur[1], 'gs')

    for maison in maisons:
        plt.plot(maison[0], maison[1], 'b^')

    plt.show()

voir_reseau(generateur, maisons)