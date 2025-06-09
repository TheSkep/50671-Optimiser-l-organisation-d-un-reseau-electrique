import math as m
import matplotlib.pyplot as plt

Transformateurs = [[5, 2], [1, 9], [4, 8], [2, 1]]
generateur = (5,5)

def voir_reseau(generateur, Transformateurs):
    plt.subplots(figsize=(7, 7))
    plt.plot(generateur[0], generateur[1], 'gs', markersize=8)

    for Transformateur in Transformateurs:
        plt.plot(Transformateur[0], Transformateur[1], 'ro', markersize=8)

    plt.xlabel('Coordonnée X')
    plt.ylabel('Coordonnée Y')
    plt.title('Représentation initiale')
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.show()

voir_reseau(generateur, Transformateurs)

