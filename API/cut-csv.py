import pandas as pd

# Chemin vers le fichier CSV d'origine
input_file = 'data/meteo-0025.csv'

# Chemin vers le fichier CSV nettoyé
output_file = 'data/meteo-0025-cleaned.csv'

# Charger le fichier CSV dans un DataFrame
data = pd.read_csv(input_file, sep=',')  # Utilisez une virgule comme séparateur

# Afficher les colonnes détectées
print("Colonnes détectées dans le fichier CSV :")
print(data.columns)

# Supprimer les lignes avec des cases vides entre 'Forecast timestamp' et 'Commune'
columns_to_check = ['Position', '2 metre temperature',
                    'Minimum temperature at 2 metres', 'Maximum temperature at 2 metres','Commune']
data_cleaned = data.dropna(subset=columns_to_check)

# Afficher un aperçu des données après nettoyage
print("\nAperçu des données après nettoyage :")
print(data_cleaned.head())

# Enregistrer le fichier nettoyé
data_cleaned.to_csv(output_file, sep=',', index=False)

print(f"\nFichier nettoyé enregistré sous : {output_file}")