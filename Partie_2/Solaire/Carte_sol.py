import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy

departements = gpd.read_file("https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements-version-simplifiee.geojson")

excel = pd.read_excel("TIPE/Partie_2/Bilan.xlsx")

excel["Départements"] = excel["Départements"].str.lower().str.strip()
departements["nom"] = departements["nom"].str.lower().str.strip()

departements = departements.merge(excel, left_on="nom", right_on="Départements", how="left")

fig, ax = plt.subplots(1, 1, figsize=(7, 7))
departements.plot(column="Ensolleilement annuel (Kwh/Kwc)", cmap="YlOrRd", linewidth=0.2, edgecolor="black", legend=True, ax=ax)

plt.axis("off")
plt.show()