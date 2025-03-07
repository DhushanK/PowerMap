from taipy.gui import Markdown, Gui, notify, Html
import os
import sys
import googlemaps
from datetime import datetime
import csv
from io import StringIO

script_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(script_folder_path)

gmaps = googlemaps.Client(key='AIzaSyBRObqLQz94vIUpxHZQEhLd9omPJSYmQ10')


from Analysis import *
carData = os.path.join("Models","seattle.sample.daily.csv")
text = "The sizes of the markers indicate the relative differences inactivity index total "
content=""


data = Analysis(carData, 0.1,5)
places = data.runcalc(10)

def get_addresses(places):
    # Initialize the Google Maps client
    
    # List to store the results
    results = []
    
    for place in places:
        # Perform reverse geocoding
        reverse_geocode_result = gmaps.reverse_geocode((place['lat'], place['lon']))
        
        # Check if we got any results
        if reverse_geocode_result:
            # Take the first result and get its formatted address
            address = reverse_geocode_result[0]['formatted_address']
            
            # Create a new dictionary with the original place data and the new address
            place_with_address = place.copy()
            place_with_address['address'] = address
            
            # Add to our results list
            results.append(place_with_address)
        else:
            # If no address was found, add the original place data with a note
            place_with_address = place.copy()
            place_with_address['address'] = "Address not found"
            results.append(place_with_address)
    
    return results

def create_google_maps_url(places, zoom=12, size="1200x1200", api_key="YOUR_API_KEY"):
    base_url = "https://maps.googleapis.com/maps/api/staticmap"
    
    # Calculate center coordinates
    center_lat = sum(place['lat'] for place in places) / len(places)
    center_lon = sum(place['lon'] for place in places) / len(places)
    
    # Set the center and basic parameters
    params = f"?center={center_lat},{center_lon}&zoom={zoom}&size={size}"
    
    # Add markers for each place
    for place in places:
        rank = int(place['name'].split()[1])  
        color = "red" 
        label = chr(64 + rank) if rank <= 26 else "" 
        markers = f"&markers=color:{color}%7Clabel:{label}%7C{place['lat']},{place['lon']}"
        params += markers
    
    # Add the API key
    params += f"&key={api_key}"
    
    return base_url + params

def convert_to_csv(places_with_addresses):
    # Create a StringIO object to write CSV data
    output = StringIO()
    
    # Check if we have any data
    if not places_with_addresses:
        return "No data to convert"
    
    # Get the fieldnames from the first dictionary
    fieldnames = places_with_addresses[0].keys()
    
    # Create a CSV writer object
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    
    # Write the header
    writer.writeheader()
    
    # Write the rows
    for place in places_with_addresses:
        writer.writerow(place)
    
    # Get the CSV data as a string
    csv_data = output.getvalue()
    
    # Close the StringIO object
    output.close()
    
    return csv_data


data = pd.DataFrame(places)

solve = np.linalg.solve([[data["activity_index_total"].min(), 1], [data["activity_index_total"].max(), 1]],
                        [5, 60])
data["size"] = data["activity_index_total"].apply(lambda p: p*solve[0]+solve[1])

data["text"] = data.apply(lambda row: f"{row['name']} [{row['activity_index_total']}]", axis=1)



marker={
      
        "size": "size"
    }
layout={
        "geo": {
            "showland": True,
            "landcolor": "4A4",
            "scope": "north america",
            "fitbounds": "locations"

        }
    }

content = create_google_maps_url(places, api_key="AIzaSyBRObqLQz94vIUpxHZQEhLd9omPJSYmQ10")
placesWithAddresses = get_addresses(places)
csv_string = convert_to_csv(placesWithAddresses)
resultsData = pd.read_csv(StringIO(csv_string))

results_md = Markdown("""

# Clusters by Activity Index

<|id=chart|{data}|chart|type=scattergeo|mode=markers|lat=lat|lon=lon|text=text|layout={layout}|marker={marker}|width="1000px"|>
<|{resultsData}|table|page_size=10|filter=true|>
""")

googlemaps_md = Markdown("""

# Plot of Optimal Locations
<|id=googlemaps|{content}|image|width="1000px"|>
""")












