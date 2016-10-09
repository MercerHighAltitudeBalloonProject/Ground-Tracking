# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 17:31:15 2016

@author: Ground Station
"""

#import serial
from __future__ import division
import time
import math
import geojson
from compass  import Compass
import json

servoCOM = "COM5"
servoBaud = 9600
servoTimeout = 0.5
moveCommand = 0xFF
panChannel = 0
tiltChannel = 1
servoAttached = True

groundAlt = 0.00
centerBear = 0.00
antennaBear = 0.00
antennaEle = 0.00


tilt_angle_min = -180        #-90
tilt_angle_max = 180         #90

servo_min = 0
servo_max = 254
panOffset = 0          # increase to turn right, decrease to turn left
tiltOffset = 0          # increase to raise, decrease to lower

class antenna_tracker():

    def __init__(self, servo_COM, antenna_Lat, antenna_Lon, antenna_altitude):
        self.compass = Compass(antenna_Lat, antenna_Lon, antenna_altitude)
        print(self.compass)
        self.servo_COM = servo_COM


    def panBothServos(self):                        #Moves servos through range of motion tests
        #global s
        print "Starting serial communication with",servoCOM
        if servoAttached:
            for i in range(127,0,-2):
                self.moveTiltServo(i)
                self.movePanServo(i)
                time.sleep(0.05)
            time.sleep(1)

            for i in range(0,254,2):
                self.moveTiltServo(i)
                self.movePanServo(i)
                time.sleep(0.05)
            time.sleep(1)
            print "Motion Test Finished"
        else:
            print "Error: Settings set to no Servo Connection"

    def moveToCenterPos(self):              #Send servos to their center pos (should be horizontal and straight ahead if zeroed)
        #global s
        print "Starting serial communication with",servoCOM
        if servoAttached:
            self.moveTiltServo(127)
            self.movePanServo(127)
            print "Move to Center Command Sent via", servoCOM
        else:
            print "Error: Settings set to no Servo Connection"

    def moveToTarget(self, bearing,elevation):        #moves servos based on a bearing and elevation angle
            
            centerBear = 0

            temp = 0
            if((bearing>180) and (centerBear == 0)):
                    centerBear = 360
            elif (((centerBear - bearing) > 180) and (centerBear >= 270)):
                    bearing = bearing + 360
            elif (((centerBear - bearing) > 180) and (centerBear <=180)):
                    temp = centerBear
                    centerBear = 360 + temp
            print ("\tBearing: %.0f" %bearing)
            print ("\tElevation Angle: %.0f"%elevation)
            #panTo = (((offsetDegrees-bearing+panOffset)*255)/panRange)+127.5
            # With new digital servos, can use map method as described here: http://arduino.cc/en/reference/map
            panTo = ((bearing - (centerBear - 168)) * (servo_max - servo_min) / ((centerBear + 168) - (centerBear - 168)) + servo_min) + (255*panOffset/360)
            if panTo > 254: panTo = 254
            if panTo < 0: panTo = 0
            print "\tServo Degrees:"
            if servoAttached:
                self.movePanServo(math.trunc(panTo)) 
            #tiltTo = (255*(96-elevation))/90
            #tiltTo = (255*(tiltRange-elevation+tiltOffset))/90
            #If Error in Antenna Mount i.e. put antenna on backwards fix with changing 0-elevation to elevation (must change tilt stops too
            tiltTo = (((0-elevation) - tilt_angle_min) * (servo_max - servo_min) / (tilt_angle_max - tilt_angle_min) + servo_min) + tiltOffset
            if tiltTo > 254: tiltTo = 254
            if tiltTo < 0: tiltTo = 0
            if servoAttached:
                self.moveTiltServo(math.trunc(tiltTo))
            if (temp!= 0):
                    centerBear = temp
            #if servoAttached:
            #    s.close()




    def moveTiltServo(self, position):
    #             s = serial.Serial(self.servo_COM, baudrate = servoBaud, timeout = servoTimeout)
    #             #move tilt
    #             if(position < 70):          #80 degrees upper limit
    #                     moveTilt = [moveCommand,tiltChannel,chr(70)]
    #             elif(position > 123):       #5 degrees lower limit
    #                     moveTilt = [moveCommand,tiltChannel,chr(123)]
    #             else:
    #                     moveTilt = [moveCommand,tiltChannel,chr(position)]
    #             s.write(moveTilt)
    #             print "\t\tTilt Pan: ", float(position)
    #             #RFD (for use with a second antenna tracker)
    # #            moveTilt = [moveCommand,rfd_tiltChannel,chr(position)]
    #             s.close()
                print("Tilting")

    def movePanServo(self, position):
    #             s = serial.Serial(self.servo_COM, baudrate = servoBaud, timeout = servoTimeout)
    #             '''
    #             if previousPan > position:
    #                 position += 1
    #             previousPan = position
    #             '''
    #             #move Ubiquity
    #             movePan = [moveCommand,panChannel,chr(255-position)]
    #             s.write(movePan)
    #             #move RFD
    #  #           movePan = [moveCommand,rfd_panChannel,chr(255-position)]
    # #            s.write(movePan)
    #             print "\t\tMove Pan: ", float(position)
    #             s.close()
                print("Paning")
            
    def pointToTarget(self, latitude, longitude, altitude):
        
        distance = self.compass.get_distance(latitude, longitude)
        bearing = self.compass.get_bearing(latitude, longitude)   
        angle = self.compass.get_elevation(latitude, longitude, altitude)
        feet_to_miles = (1/5280)
        print("{0:.2f}, {1:.2f}, {2:.2f}".format(distance*feet_to_miles,bearing,angle))
        self.moveToTarget(bearing, angle)

         
         
if __name__ == "__main__":

    print("Starting Servo Tester")
    print("------------------------------")    
    
    tracker = antenna_tracker("COM5", 32.827103, -83.649268, 0)
    
    gps_file = open("in.txt", "r")

    for line in gps_file:
        lat,lon,alt = [float(x) for x in line.split(", ")]
        tracker.pointToTarget(lat,lon,alt)

    gps_file.close()