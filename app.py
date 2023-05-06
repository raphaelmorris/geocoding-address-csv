import csv
from tqdm import tqdm
from geopy.geocoders import GoogleV3

# Spécifiez votre clé d'API Google Maps Geocoding
API_KEY = 'enter_api_key'

# Créez une instance du géocodeur GoogleV3
geolocator = GoogleV3(api_key=API_KEY)

# Spécifiez le nom de fichier CSV d'entrée et de sortie
input_file = 'input.csv'
output_file = 'output.csv'

# Comptez le nombre total de lignes dans le fichier d'entrée
with open(input_file, 'r') as f:
    total_lines = sum(1 for line in f)

# Ouvrez le fichier CSV d'entrée et créez un objet DictReader
with open(input_file, 'r') as csv_file:
    reader = csv.DictReader(csv_file)

    # Créez une liste vide pour stocker les coordonnées géographiques extraites
    coordinates_list = []

    # Parcourez chaque ligne du fichier CSV
    for row in tqdm(reader, total=total_lines):

        # Obtenez l'adresse à partir de la colonne "adresse" de la ligne actuelle
        address = row['adresse']

        # Utilisez le géocodeur GoogleV3 pour géocoder l'adresse
        location = geolocator.geocode(address, timeout=10)

        # Si la localisation est valide, extrayez les coordonnées géographiques
        if location is not None:
            lat = location.latitude
            lng = location.longitude

            # Ajoutez les coordonnées géographiques à la liste
            coordinates_list.append({'adresse': address, 'latitude': lat, 'longitude': lng})
        else:
            print(f"L'adresse suivante n'a pas pu être géocodée : {address}")

    # Écrivez les coordonnées géographiques dans le fichier CSV de sortie
    with open(output_file, 'w', newline='') as output_csv:
        fieldnames = ['adresse', 'latitude', 'longitude']
        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        writer.writeheader()
        for coordinates in coordinates_list:
            writer.writerow(coordinates)
