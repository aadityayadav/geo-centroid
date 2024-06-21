import googlemaps
import math

class CentroidCalculator:
    def __init__(self, api_key):
        """
        Initializes the CentroidCalculator object with the Google Maps API key.
        """
        self.gmaps = googlemaps.Client(key=api_key)

    def geocode_address(self, address):
        """
        Geocodes an address to get the latitude and longitude coordinates.
        @parameters:
        - address (str): The address to geocode.
        @returns:
        - [lat, lng] (list): The latitude and longitude coordinates of the address.
        """
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
        """
        Calculates the centroid of two points with weights.
        @parameters:
        - lat1 (float): The latitude of the first point.
        - lng1 (float): The longitude of the first point.
        - w1 (int): The weight of the first point.
        - lat2 (float): The latitude of the second point.
        - lng2 (float): The longitude of the second point.
        - w2 (int): The weight of the second point.
        @returns:
        - [clat, clng, w1 + w2] (list): The latitude, longitude, and combined weight of the centroid.
        """
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
        """
        Generates the centroid of a list of geocoded addresses with weights.
        @parameters:
        - geocoded (list): A list of geocoded addresses.
        @returns:
        - [clat, clng, w] (list): The latitude, longitude, and combined weight of the centroid.
        """
        while len(geocoded) > 1:
            new_coord = self.calculate_two_point_centroid(*geocoded[0], *geocoded[1])
            geocoded = geocoded[2:]
            geocoded.append(new_coord)
        return geocoded[0]

    def get_centroid(self, addresses):
        """
        Calculates the centroid of a list of addresses.
        @parameters:
        - addresses (list): A list of addresses.
        Each element in the addresses list can be:
              A string representing the address,
              A geocoded address [lat, lng],
              An address with a weight [address, weight] | [lat, lng, weight].
        @returns:
        - [clat, clng, w] (list): The latitude, longitude, and combined weight of the centroid.
        """
        geocoded =[]

        for address in addresses:
            if type(address) == list:
                if len(address) == 2:
                    if type(address[0]) == str and type(address[1]) == int:
                        geocoded_address = self.geocode_address(address[0])
                        if geocoded_address is None:
                            continue
                        geocoded_address.append(address[1])
                    elif type(address[0]) == float and type(address[1]) == float \
                        and address[0] >= -90.0 and address[0] <= 90.0 and address[1] >= -180.0 and address[1] <= 180.0:
                        geocoded_address = address
                        geocoded_address.append(1)
                    else:
                        print("Could not geocode address (Skipping): ", address)
                        continue
                elif len(address) == 3:
                    if type(address[0]) == float and type(address[1]) == float and type(address[2]) == int \
                        and address[0] >= -90.0 and address[0] <= 90.0 and address[1] >= -180.0 and address[1] <= 180.0:
                        geocoded_address = address
                    else:
                        print("Could not geocode address (Skipping): ", address)
                        continue
                else:
                    print("Could not geocode address (Skipping): ", address)
                    continue
            elif type(address) == str:
                geocoded_address = self.geocode_address(address)
                if geocoded_address is None:
                    continue
                geocoded_address.append(1)
            else:
                print("Could not geocode address (Skipping): ", address)
                continue
            geocoded.append(geocoded_address)

        if len(geocoded) > 1:
            print(geocoded)
            return self.generate_centroid(geocoded)
        else:
            print("Failed to calculate centroid (Not enough geocoded addresses)")
            return None
