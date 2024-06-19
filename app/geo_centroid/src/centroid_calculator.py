import googlemaps
import math

class CentroidCalculator:
    def __init__(self, api_key):
        self.gmaps = googlemaps.Client(key=api_key)

    def geocode_address(self, address):
        result = self.gmaps.geocode(address)
        if result and 'geometry' in result[0]:
            location = result[0]['geometry']['location']
            lat = location['lat']
            lng = location['lng']
            return [lat, lng]
        else:
            print("Could not geocode address (Skipping): ", address)
            return None

    def calculate_two_point_centroid(self, lat1, lng1, w1, lat2, lng2, w2):
        lat1_rad = lat1 * (math.pi / 180)
        lat2_rad = lat2 * (math.pi / 180)
        lng1_rad = lng1 * (math.pi / 180)
        lng2_rad = lng2 * (math.pi / 180)
        delta_lat_rad = (lat2 - lat1) * (math.pi / 180)
        delta_lng_rad = (lng2 - lng1) * (math.pi / 180)
        h = (pow(math.sin(delta_lat_rad / 2), 2) + (math.cos(lat1_rad) * math.cos(lat2_rad) * pow(math.sin(delta_lng_rad / 2), 2)))
        c = 2 * math.atan2(math.sqrt(h), math.sqrt(1 - h))
        if w1 < w2:
            f = 1 - w1 / (w1 + w2)
        else:
            f = 1 - w2 / (w1 + w2)
        a = math.sin((1 - f) * c) / math.sin(c)
        b = math.sin(f * c) / math.sin(c)
        x = a * math.cos(lat1_rad) * math.cos(lng1_rad) + b * math.cos(lat2_rad) * math.cos(lng2_rad)
        y = a * math.cos(lat1_rad) * math.sin(lng1_rad) + b * math.cos(lat2_rad) * math.sin(lng2_rad)
        z = a * math.sin(lat1_rad) + b * math.sin(lat2_rad)
        clat_rad = math.atan2(z, math.sqrt(x * x + y * y))
        clng_rad = math.atan2(y, x)
        clat = clat_rad * (180 / math.pi)
        clng = clng_rad * (180 / math.pi)
        return [clat, clng, w1 + w2]

    def generate_centroid(self, geocoded):
        while len(geocoded) > 1:
            # gotta fix the weight thingy here
            new_coord = self.calculate_two_point_centroid(*geocoded[0], *geocoded[1])
            geocoded = geocoded[2:]
            geocoded.append(new_coord)
        return geocoded

    def get_address_centroid(self, addresses):
        self.geocoded = [self.geocode_address(address) for address in addresses if self.geocode_address(address) is not None]
        if len(self.geocoded) > 1:
            return self.generate_centroid(self.geocoded)
        else:
            print("Failed to calculate centroid (Not enough geocoded addresses)")
            return None

# Example usage:
if __name__ == "__main__":
    api_key = "AIzaSyAGiZ1yqXYCFE2_TfC3q2VHSwgM0UrU10E"
    address_list = ["Address 1", "Address 2", "Address 3"]  # Provide your address list here
    calculator = CentroidCalculator(api_key)
    print(calculator.geocode_address("india"))
    # centroid = calculator.get_address_centroid(address_list)
    # if centroid:
    #     print("Centroid:", centroid)
    # else:
    #     print("Not enough geocoded addresses to calculate centroid.")


# use cases
# 1. address to geocode
# 2. calculate centroid of addresses or geocoded addresses
# 3. given a weight associated with an address find the centroid of the addresses
# 4. get the distance between two addresses