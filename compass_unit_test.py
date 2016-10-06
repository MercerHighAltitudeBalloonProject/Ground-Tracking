from __future__ import division
import unittest
import compass

class unit_test_compass(unittest.TestCase):

    def test_bearing(self):
        C = compass.compass(43.682213,-70.450696)
        self.assertEqual(round(C.get_bearing(43.682194,-70.450769),2), 250.21)
        C = compass.compass(0, 0)
        self.assertEqual(round(C.get_bearing(90, 0),2), 0)
        self.assertEqual(round(C.get_bearing(0, 90),2), 90)
        self.assertEqual(round(C.get_bearing(-90, 0),2), 180)
        self.assertEqual(round(C.get_bearing(0, -90),2), 270)
        C = compass.compass(33.77487 , -84.39904)
        self.assertEqual(round(C.get_bearing(34.44768, -84.39367), 3), 0.377) #N - 74.633 km, 46.375 mi, 
        self.assertEqual(round(C.get_bearing(34.28672, -83.75097), 3), 46.197) #NE - 82.495 km, 51.26 mi
        self.assertEqual(round(C.get_bearing(33.77001, -83.69604), 3), 90.281) #E - 65.121 km, 40.464 mi
        self.assertEqual(round(C.get_bearing(33.46581, -83.98718), 3), 131.909) #SE - 51.339 km, 31.901 mi
        self.assertEqual(round(C.get_bearing(33.4933, -84.43487), 3), 186.058) #S - 31.407 km, 19.515 mi
        self.assertEqual(round(C.get_bearing(33.54368, -84.62301), 3), 218.943) #SW - 33.001 km, 20.506 mi
        self.assertEqual(round(C.get_bearing(33.76829, -84.71982), 3), 268.676) #W - 29.723 km, 18.469 mi
        self.assertEqual(round(C.get_bearing(34.03842, -84.68068), 3), 318.508) #NW - 39.154 km, 24.329 mi

    def test_distance(self):
        C = compass.compass(33.77487 , -84.39904)
        feet_to_miles = (1/5280)
        self.assertEqual(round(C.get_distance(34.44768, -84.39367) * feet_to_miles, 1), 46.5) #N - 74.633 km, 46.375 mi, 
        self.assertEqual(round(C.get_distance(34.28672, -83.75097) * feet_to_miles, 1), 51.3) #NE - 82.495 km, 51.26 mi
        self.assertEqual(round(C.get_distance(33.77001, -83.69604) * feet_to_miles, 1), 40.4) #E - 65.121 km, 40.464 mi
        self.assertEqual(round(C.get_distance(33.46581, -83.98718) * feet_to_miles, 1), 31.9) #SE - 51.339 km, 31.901 mi
        self.assertEqual(round(C.get_distance(33.4933, -84.43487) * feet_to_miles, 1), 19.6) #S - 31.407 km, 19.515 mi
        self.assertEqual(round(C.get_distance(33.54368, -84.62301) * feet_to_miles, 1), 20.5) #SW - 33.001 km, 20.506 mi
        self.assertEqual(round(C.get_distance(33.76829, -84.71982) * feet_to_miles, 1), 18.4) #W - 29.723 km, 18.469 mi
        self.assertEqual(round(C.get_distance(34.03842, -84.68068) * feet_to_miles, 1), 24.3) #NW - 39.154 km, 24.329 mi

if __name__ == '__main__':
    unittest.main()


  