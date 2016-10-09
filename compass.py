#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import math


class Compass():

    def __init__(self, current_lat, current_lon, current_alt):
        self.current_lon = current_lon
        self.current_lat = current_lat
        self.current_alt = current_alt


    def get_bearing(self, remote_Lat, remote_Lon):
        """
        Follows the formula below to find the bearing to the new points.
        θ = atan2(sin(Δlong)*cos(lat2),
                  cos(lat1)*sin(lat2) − sin(lat1)*cos(lat2)*cos(Δlong))
        """

        radCurrentLat = math.radians(self.current_lat)
        radRemoteLat = math.radians(remote_Lat)

        dLat = math.radians(remote_Lat - self.current_lat)       # delta latitude in radians
        dLon = math.radians(remote_Lon - self.current_lon)       # delta longitude in radians
        
        y = math.sin(dLon) * math.cos(radRemoteLat)
        x = math.cos(radCurrentLat) * math.sin(radRemoteLat) - \
            math.sin(radCurrentLat) * math.cos(radRemoteLat) * math.cos(dLon)
        bearing = math.degrees(math.atan2(y,x))     # returns the bearing from true north
        if (bearing < 0):
                bearing = bearing + 360
        return bearing

  
    def get_distance(self, remote_Lat, remote_Lon):
        """
        haversine formula, see: http://www.movable-type.co.uk/scripts/latlong.html 
        """
        radius = 6371        # radius of earth in Km

        radCurrentLat = math.radians(self.current_lat)
        radRemoteLat = math.radians(remote_Lat)

        dLat = math.radians(remote_Lat - self.current_lat)       # delta latitude in radians
        dLon = math.radians(remote_Lon - self.current_lon)       # delta longitude in radians

        a = (math.sin(dLat / 2.0) ** 2 + 
             math.cos(radCurrentLat) * 
             math.cos(radRemoteLat) * 
             math.sin(dLon / 2.0) ** 2)

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = radius * c
        
        return distance*3280.839895 # multiply distance in Km by 3280 for feet

    def get_elevation(self, remote_Lat, remote_Lon, remote_alt):
        deltaAlt = float(remote_alt) - self.current_alt
        distanceToTarget = self.get_distance(remote_Lat, remote_Lon)
        return math.degrees(math.atan2(deltaAlt,distanceToTarget))

    def __repr__(self):
        return "Compass: ({0},{1},{2})".format(self.current_lat, self.current_lon, self.current_alt)
