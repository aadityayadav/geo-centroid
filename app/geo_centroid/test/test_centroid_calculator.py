from app.geo_centroid.src.centroid_calculator import CentroidCalculator

# test 1: 64 Marshall st, Waterloo Ontario. Result: [43.4741752, -80.5204558] 
# print(calculator.geocode_address("64 Marshall st, Waterloo Ontario"))

# test2:
# address_list = ["64 Marshall st Waterloo Ontario", "CIF waterloo ontario", "King Street towers, waterloo ontario"]  # Provide your address list here
# calculator = CentroidCalculator(api_key)
# # print(calculator.geocode_address("india"))
# centroid = calculator.get_centroid(address_list) Result:[[43.47649843865154, -80.53145133903517, 3]]

# test 3: all same as above
# address_list = [["64 Marshall st Waterloo Ontario", 5], "CIF waterloo ontario", "King Street towers, waterloo ontario"] 
# [[43.47580075938039, -80.540801226302, 7]]

# test4: all same and same results
# address_list = [[43.4740533, -80.5205138, 5], [43.475277, -80.54781349999999, 1], [43.4801632, -80.5260265, 1]]