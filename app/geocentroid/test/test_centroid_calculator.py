import unittest
import os
from dotenv import load_dotenv
from app.geocentroid.src.centroid_calculator import CentroidCalculator

load_dotenv()

class TestCentroidCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = CentroidCalculator(os.environ.get("API_KEY"))
    
    def assertListAlmostEqual(self, list1, list2, tol):
        """
        Asserts that two lists are equal up to a certain tolerance.
        """
        self.assertEqual(len(list1), len(list2))
        for a, b in zip(list1, list2):
            self.assertAlmostEqual(a, b, tol)
    
    # The error tolerance for the coordinates is up to 3 decimal places. 
    # Because at 4 decimal places, the difference is only 11.1m
    def test_geocode_address(self):
        result = self.calculator.geocode_address("64 Marshall st, Waterloo Ontario")
        self.assertListAlmostEqual(result, [43.4741752, -80.5204558], 3)
        
    def test_get_centroid_all_addresses(self):
        address_list_1 = ["64 Marshall st Waterloo Ontario", "CIF waterloo ontario", "King Street towers, waterloo ontario"]
        result_1 = self.calculator.get_centroid(address_list_1)
        self.assertListAlmostEqual(result_1, [43.47649843865154, -80.53145133903517, 3],3)
        
    def test_get_centroid_all_addresses_with_weight(self):
        address_list_2 = [["64 Marshall st Waterloo Ontario", 5], "CIF waterloo ontario", "King Street towers, waterloo ontario"]
        result_2 = self.calculator.get_centroid(address_list_2)
        self.assertListAlmostEqual(result_2, [43.47580075938039, -80.540801226302, 7],3)
        
    def test_get_centroid_geocoded_addresses_with_weight(self):
        address_list_3 = [[43.4740533, -80.5205138, 5], [43.475277, -80.54781349999999, 1], [43.4801632, -80.5260265, 1]]
        result_3 = self.calculator.get_centroid(address_list_3)
        self.assertListAlmostEqual(result_3, [43.47580075938039, -80.540801226302, 7],3)
        
    def test_get_centroid_single_address(self):
        address_list_4 = [[43.4740533, -80.5205138, 5]]
        result_4 = self.calculator.get_centroid(address_list_4)
        self.assertIsNone(result_4)
        
    def test_get_centroid_mix_address_and_geocoded(self):
        address_list_5 = [["64 Marshall st Waterloo Ontario", 5], [43.475277, -80.54781349999999, 1], "King Street towers, waterloo ontario"]
        result_5 = self.calculator.get_centroid(address_list_5)
        self.assertListAlmostEqual(result_5, [43.47580075938039, -80.540801226302, 7],3)
        
    def test_get_centroid_mix_weighted_and_non_weighted(self):
        address_list_6 = ["64 Marshall st Waterloo Ontario", [43.475277, -80.54781349999999, 2], "King Street towers, waterloo ontario"]
        result_6 = self.calculator.get_centroid(address_list_6)
        self.assertListAlmostEqual(result_6, [43.47619329770745, -80.53554194128088, 4],3)
        
    def test_get_centroid_fake_address(self):
        address_list_7 = ["fake address", [43.475277, -80.54781349999999, 2], "King Street towers, waterloo ontario"]
        result_7 = self.calculator.get_centroid(address_list_7)
        self.assertListAlmostEqual(result_7, [43.4785349262818, -80.53328922483436, 3],3)
        
    def test_get_centroid_invalid_latlng_list(self):
        address_list_8 = ["64 Marshall st Waterloo Ontario", [-80.54781349999999], "King Street towers, waterloo ontario"]
        result_8 = self.calculator.get_centroid(address_list_8)
        self.assertListAlmostEqual(result_8, [43.47710828310337, -80.52327001064637, 2],3)
        
    def test_get_centroid_invalid_latlng_coord(self):
        address_list_9 = ["64 Marshall st Waterloo Ontario", [443.475277, -80.54781349999999, 2], "King Street towers, waterloo ontario"]
        result_9 = self.calculator.get_centroid(address_list_9)
        self.assertListAlmostEqual(result_9, [43.47710828310337, -80.52327001064637, 2],3)
        
    def test_get_centroid_invalid_weight(self):
        address_list_10 = [["64 Marshall st Waterloo Ontario", 5.1], [43.475277, -80.54781349999999, 1]]
        result_10 = self.calculator.get_centroid(address_list_10)
        self.assertIsNone(result_10)

