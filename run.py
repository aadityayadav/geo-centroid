import os
from dotenv import load_dotenv
import geocentroid 

load_dotenv()

geo_calculator = geocentroid.CentroidCalculator(api_key = os.environ.get("API_KEY"))

# Geocoding an address.
print(geo_calculator.geocode_address("200 University Ave W, Waterloo, ON N2L 3G1"))


# Calculate the centroid given two points with weights.
print(geo_calculator.calculate_two_point_centroid(43.4740533, -80.5205138, 1, 43.4683522, -80.5425357, 1))

# Generates the centroid of a list of geocoded addresses.
print(geo_calculator.generate_centroid([[43.4740533, -80.5205138, 1], [43.4683522, -80.5425357, 1]]))