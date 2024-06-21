## Introduction
A python package that can be used to generate a centroid from a given list of addresses/geocoded locations.
Further, weights can be attached to each location, to give it a bias, and calculate a weighted centroid.
<br>
<br>

## Requirements
- Python 3.5 or later
- [Google Maps API Key](https://developers.google.com/maps/documentation/embed/get-api-key)
<br>
<br>


## Installation
```
pip install geocentroid
```
<br>
<br>


## Usage
This example shows how to use the geocentroid package.
```
import geocentroid 

geo_calculator = geocentroid.CentroidCalculator(api_key = "ADD YOUR GOOGLE API KEY HERE")

# Geocoding an address.
waterloo_address = geo_calculator.geocode_address("200 University Ave W, Waterloo, ON N2L 3G1")

# Calculate the centroid given two geocoded locations with weights.
centroid_of_two_addresses = geo_calculator.calculate_two_point_centroid(43.4740533, -80.5205138, 1, 43.4683522, -80.5425357, 1)

# Calculate the centroid for a list of addresses:
centroid_of_addresses = geo_calculator.get_centroid(["200 University Ave W, Waterloo, ON N2L 3G1",
                                                     "CIF Waterloo Ontario",
                                                     "King Street towers, waterloo ontario"])

# Calculate the centroid for a list of geocoded addresses:
centroid_of_addresses = geo_calculator.get_centroid([43.4740533, -80.5205138],
                                                    [43.4683522, -80.5425357],
                                                    [44.4482542, -79.4425354]])

# Calculate the centroid for a list of addresses with weights
centroid_of_addresses = geo_calculator.get_centroid([[43.4740533, -80.5205138, 10],
                                                     [43.4683522, -80.5425357, 22],
                                                     ["King Street towers, waterloo ontario", 38]])

```
For test cases check out: [tests](https://github.com/aadityayadav/geo-centroid/blob/main/app/geocentroid/test/test_centroid_calculator.py).
<br>
<br>

## Documentation

### 1) geocode_address(self, address)
Geocodes an address to get the latitude and longitude coordinates.

**Parameters:**
- `address` (str): The address to geocode.

**Returns:**
- `[lat, lng]` (list): The latitude and longitude coordinates of the address.

<br>

### 2) calculate_two_point_centroid(self, lat1, lng1, w1, lat2, lng2, w2)
Calculates the centroid of two points with weights.

**Parameters:**
- `lat1` (float): The latitude of the first point.
- `lng1` (float): The longitude of the first point.
- `w1` (int): The weight of the first point.
- `lat2` (float): The latitude of the second point.
- `lng2` (float): The longitude of the second point.
- `w2` (int): The weight of the second point.

**Returns:**
- `[clat, clng, w1 + w2]` (list): The latitude, longitude, and combined weight of the centroid.

<br>

### 3) generate_centroid(self, geocoded)
Generates the centroid of a list of geocoded addresses with weights.

**Parameters:**
- `geocoded` (list): A list of geocoded addresses.

**Returns:**
- `[clat, clng, w]` (list): The latitude, longitude, and combined weight of the centroid.

<br>

### 4) get_centroid(self, addresses)
Calculates the centroid of a list of addresses.

**Parameters:**
- `addresses` (list): A list of addresses. Each element in the addresses list can be:
    - A string representing the address,
    - A geocoded address `[lat, lng]`,
    - An address with a weight `[address, weight]` | `[lat, lng, weight]`.

**Returns:**
- `[clat, clng, w]` (list): The latitude, longitude, and combined weight of the centroid.
<br>
<br>

## Testing
To run the tests, clone the repository and from the root directory run:
```
python3 -m unittest path/to/your/test/test_centroid_calculator.py
```
<br>
<br>

## Building the Package and Installing Locally
Clone the repository then build the packages using:
```
pip3 install wheel
python3 setup.py bdist_wheel sdist
pip3 install .
```
