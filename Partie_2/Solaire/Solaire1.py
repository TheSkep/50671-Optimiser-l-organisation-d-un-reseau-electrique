from pandas import read_excel

excel = read_excel("TIPE/Partie_2/Solaire/Centre_departement.xlsx")
dict_departements = {rangee['Départements']: [rangee['Latitude'], rangee['Longitude']] for _, rangee in excel.iterrows()}

print(dict_departements)