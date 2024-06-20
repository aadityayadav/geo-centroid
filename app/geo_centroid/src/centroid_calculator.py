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

    # def get_weighted_centroid(self, addresses):
    #     geocoded = [self.geocode_address(address[0]).append(address[1]) for address in addresses if self.geocode_address(address) is not None]
    #     if len(geocoded) > 1:
    #         return self.generate_centroid(geocoded)
    #     else:
    #         print("Failed to calculate centroid (Not enough geocoded addresses)")
    #         return None

    def get_centroid(self, addresses):
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
        # geocoded = [self.geocode_address(address).append(1) for address in addresses if self.geocode_address(address) is not None]
        if len(geocoded) > 1:
            print(geocoded)
            return self.generate_centroid(geocoded)
        else:
            print("Failed to calculate centroid (Not enough geocoded addresses)")
            return None

# # Example usage:
# if __name__ == "__main__":
#     api_key = "AIzaSyAGiZ1yqXYCFE2_TfC3q2VHSwgM0UrU10E"
#     # address_list = ["64 Marshall st Waterloo Ontario", "CIF waterloo ontario", "King Street towers, waterloo ontario"]  # Provide your address list here
#     # address_list = [["64 Marshall st Waterloo Ontario", 5], "CIF waterloo ontario", "King Street towers, waterloo ontario"]  # Provide your address list here
#     address_list = [[43.4740533, -80.5205138, 5], [443.475277, -80.54781349999999, 1], [43.4801632, -80.5260265, 1]]
#     calculator = CentroidCalculator(api_key)
#     # print(calculator.geocode_address("india"))
#     centroid = calculator.get_centroid(address_list)
#     if centroid:
#         print("Centroid:", centroid)
#     else:
#         print("Not enough geocoded addresses to calculate centroid.")


# use cases
# 1. address to geocode
# 2. calculate centroid of addresses or geocoded addresses
# 3. given a weight associated with an address find the centroid of the addresses
# 4. get the distance between two addresses