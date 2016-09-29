# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 17:31:15 2016

@author: Ground Station
"""

import serial
import time
import math

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

def panBothServos():                        #Moves servos through range of motion tests
    #global s
    print "Starting serial communication with",servoCOM
    if servoAttached:
        for i in range(127,0,-2):
            moveTiltServo(i)
            movePanServo(i)
            time.sleep(0.05)
        time.sleep(1)

        for i in range(0,254,2):
            moveTiltServo(i)
            movePanServo(i)
            time.sleep(0.05)
        time.sleep(1)
        print "Motion Test Finished"
    else:
        print "Error: Settings set to no Servo Connection"

def moveToCenterPos():              #Send servos to their center pos (should be horizontal and straight ahead if zeroed)
    #global s
    print "Starting serial communication with",servoCOM
    if servoAttached:
        moveTiltServo(127)
        movePanServo(127)
        print "Move to Center Command Sent via", servoCOM
    else:
        print "Error: Settings set to no Servo Connection"

def moveToTarget(bearing,elevation):        #moves servos based on a bearing and elevation angle
        
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
            movePanServo(math.trunc(panTo)) 
        #tiltTo = (255*(96-elevation))/90
        #tiltTo = (255*(tiltRange-elevation+tiltOffset))/90
        #If Error in Antenna Mount i.e. put antenna on backwards fix with changing 0-elevation to elevation (must change tilt stops too
        tiltTo = (((0-elevation) - tilt_angle_min) * (servo_max - servo_min) / (tilt_angle_max - tilt_angle_min) + servo_min) + tiltOffset
        if tiltTo > 254: tiltTo = 254
        if tiltTo < 0: tiltTo = 0
        if servoAttached:
            moveTiltServo(math.trunc(tiltTo))
        if (temp!= 0):
                centerBear = temp
        #if servoAttached:
        #    s.close()




def moveTiltServo(position):
            s = serial.Serial(str(servoCOM), baudrate = servoBaud, timeout = servoTimeout)
            #move tilt
            if(position < 70):          #80 degrees upper limit
                    moveTilt = [moveCommand,tiltChannel,chr(70)]
            elif(position > 123):       #5 degrees lower limit
                    moveTilt = [moveCommand,tiltChannel,chr(123)]
            else:
                    moveTilt = [moveCommand,tiltChannel,chr(position)]
            s.write(moveTilt)
            print "\t\tTilt Pan: ", float(position)
            #RFD (for use with a second antenna tracker)
#            moveTilt = [moveCommand,rfd_tiltChannel,chr(position)]
            s.close()

def movePanServo(position):
    
            s = serial.Serial(str(servoCOM), baudrate = servoBaud, timeout = servoTimeout)
            '''
            if previousPan > position:
                position += 1
            previousPan = position
            '''
            #move Ubiquity
            movePan = [moveCommand,panChannel,chr(255-position)]
            s.write(movePan)
            #move RFD
 #           movePan = [moveCommand,rfd_panChannel,chr(255-position)]
#            s.write(movePan)
            print "\t\tMove Pan: ", float(position)
            s.close()
        
def pointToTarget(pointtoLon, pointtoLat, pointtoAlt):
    groundLat = 32.827227
    groundLon = -83.648384
    groundAlt = 100
    
    deltaAlt = float(pointtoAlt) - groundAlt
    distanceToTarget = 0.87*haversine( groundLat,  groundLon, pointtoLat, pointtoLon)
    bearingToTarget = bearing(groundLat,  groundLon, pointtoLat, pointtoLon)   
    elevationAngle = math.degrees(math.atan2(deltaAlt,distanceToTarget))
    print(distanceToTarget,bearingToTarget,elevationAngle)
    moveToTarget(bearingToTarget,elevationAngle)


# great circle bearing, see: http://www.movable-type.co.uk/scripts/latlong.html 
def bearing(trackerLat, trackerLon, remoteLat, remoteLon):
        dLat = math.radians(remoteLat-trackerLat)       # delta latitude in radians
        dLon = math.radians(remoteLon-trackerLon)       # delta longitude in radians
        
        y = math.sin(dLon)*math.cos(math.radians(remoteLat))
        x = math.cos(math.radians(trackerLat))*math.sin(math.radians(remoteLat))-math.sin(math.radians(trackerLat))*math.cos(math.radians(remoteLat))*math.cos(dLat)
        tempBearing = math.degrees(math.atan2(y,x))     # returns the bearing from true north
        if (tempBearing < 0):
                tempBearing = tempBearing + 360
        return tempBearing

    ##############################
    ## Returns Data in Nautical ##
    ##############################

# haversine formula, see: http://www.movable-type.co.uk/scripts/latlong.html    
def haversine(trackerLat, trackerLon, remoteLat, remoteLon):
        R = 6371        # radius of earth in Km

        dLat = math.radians(remoteLat-trackerLat)       # delta latitude in radians
        dLon = math.radians(remoteLon-trackerLon)       # delta longitude in radians
        ####################################
        a = math.sin(dLat/2)*math.sin(dLat/2)+math.cos(math.radians(trackerLat))*math.cos(math.radians(remoteLat))*math.sin(dLon/2)*math.sin(dLon/2)
        #############################
        c = 2*math.atan2(math.sqrt(a),math.sqrt(1-a))
        
        d = R*c
        
        return d*3280.839895 # multiply distance in Km by 3280 for feet

         
         
if __name__ == "__main__":

    print("Starting Servo Tester")
    print("------------------------------")    
    
#    val = 10    
    
    #moveToCenterPos()    
    #32.827227, -83.648384
    pointToTarget(32.827227, -83.648384, 0)
    print("North")
    time.sleep(2)

    pointToTarget(32.827607, -83.648578, 0)
    print("North")
    time.sleep(2)
    
    pointToTarget(32.818444, -83.648427, 0)
    print("South")
    time.sleep(2)    
    
    pointToTarget(0, 0, 0)
    print("South")
    time.sleep(2)
