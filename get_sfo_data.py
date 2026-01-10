import overpy
import json

# Initialize the API
api = overpy.Overpass()

# Query SFO Airport (coordinates 37.6213, -122.3790) for food, lounges, toilets, etc.
# We look for nodes/ways with 'amenity' or 'shop' tags.
query = """
[out:json];
(
  node["amenity"](around:3000, 37.6213, -122.3790);
  way["amenity"](around:3000, 37.6213, -122.3790);
  node["shop"](around:3000, 37.6213, -122.3790);
  way["shop"](around:3000, 37.6213, -122.3790);
);
out center;
"""

print("Fetching SFO data... this might take 30 seconds...")
try:
    result = api.query(query)
except Exception as e:
    print(f"Error fetching data: {e}")
    exit(1)

amenities = []

def process_element(element, type_tag):
    tags = element.tags
    if "name" in tags:
        lat = float(element.lat) if hasattr(element, 'lat') else float(element.center_lat)
        lon = float(element.lon) if hasattr(element, 'lon') else float(element.center_lon)
        
        amenities.append({
            "name": tags.get("name"),
            "type": tags.get(type_tag),
            "terminal": tags.get("ref", "General Area"),
            "desc": f"{tags.get('name')} is a {tags.get(type_tag)} located at SFO airport.",
            "lat": lat,
            "lon": lon
        })

for node in result.nodes:
    process_element(node, "amenity" if "amenity" in node.tags else "shop")

for way in result.ways:
    process_element(way, "amenity" if "amenity" in way.tags else "shop")

# Save to a file we will upload to MongoDB tomorrow
with open("sfo_amenities.json", "w") as f:
    json.dump(amenities, f, indent=2)

print(f"Success! Saved {len(amenities)} places to sfo_amenities.json")
