from __future__ import division

import math
from controller import Controller

WARUP = 0
QUALIFYING = 1
RACE = 2

class SimpleDriver(Controller):
    stage = 0

    def __init__(self):
        # Gear Changing Constants
        self.gearUp = [5000, 6000, 6000, 6500, 7000, 0]
        self.gearDown = [0, 2500, 3000, 3000, 3500, 3500]

        # Stucks Constants
        self.stuckTime = 25
        self.stuckAgle = 0.523598775

        # Accel and Brake Constants
        self.maxSpeedDist = 70
        self.maxSpeed = 150
        self.sin5 = 0.08716
        self.cos5 = 0.99619

        # Steering Constants
        self.steerLock = 0.785398
        self.steerSensitivityOffset = 80
        self.wheelSensitivityCoeff = 1

        # ABS Filter Constants
        self.wheelRadius = [0.3179, 0.3179, 0.3276, 0.3276]
        self.absSlip = 2
        self.absRange = 3
        self.absMinSpeed = 3

        # Clutching Constants
        self.clutchMax = 0.5
        self.clutchDelta = 0.05
        self.clutchRange = 0.82
        self.clutchDeltaTime = 0.02
        self.clutchDeltaRaced = 10
        self.clutchDec = 0.01
        self.clutchMaxModifier = 1.3
        self.clutchMaxTime = 1.5

        self.stuck = 0
        self.clutch = 0

    def initAngle(self):
        return [-90,-75,-60,-45,-30,-20,-15,-10,-5,0,5,10,15,20,30,45,60,75,90]

    def reset(self):
        print 'Restarting the race.'

    def shutdown(self):
        print 'Shutting down.'

    def control(self, sensor):
        if abs(sensor['angle'] > self.stuckAgle):
            self.stuck += 1
        else:
            self.stuck = 0
        
        if self.stuck > self.stuckTime:
            steer = -sensor['angle']/self.steerLock
            gear = -1

            if sensor['angle']*sensor['trackPos'] > 0:
                gear = 1
                steer = -steer
            
            self.clutch = self.clutching(sensor, self.clutch)

            return self.action(1, 0, self.clutch, gear, steer)
        else:
            accel_and_brake = self.getAccel(sensor)
            gear = self.getGear(sensor)
            steer = self.getSteer(sensor)

            if steer < -1: steer = -1
            if steer > 1: steer = 1

            if accel_and_brake > 0:
                accel = accel_and_brake
                brake = 0
            else:
                accel = 0
                brake = self.filterABS(sensor, -accel_and_brake)
            
            self.clutch = self.clutching(sensor, self.clutch)

            return self.action(accel, brake, self.clutch, gear, steer)
    
    def getGear(self, sensor):
        gear = sensor['gear']
        rpm = sensor['rpm']

        if gear < 1: return 1
        if gear < 6 and rpm >= self.gearUp[int(gear)-1]: 
            return gear + 1
        else:
            if gear > 1 and rpm <= self.gearDown[int(gear)-1]:
                return gear - 1
            else:
                return gear

    def getSteer(self, sensor):
        targetAngle = (sensor['angle']-sensor['trackPos']*0.5)
        if sensor['speedX'] > self.steerSensitivityOffset:
            return targetAngle/(self.steerLock*(sensor['speedX']-self.steerSensitivityOffset)*self.wheelSensitivityCoeff)
        else:
            return targetAngle/self.steerLock

    def getAccel(self, sensor):
        if -1 < sensor['trackPos'] < 1:
            rxSensor = sensor['track'][10]
            sensorsensor = sensor['track'][9]
            sxSensor = sensor['track'][8]
            if sensorsensor>self.maxSpeedDist or (sensorsensor>=rxSensor and sensorsensor>=sxSensor):
                targetSpeed = self.maxSpeed;
            else:
                h = sensorsensor*self.sin5
                
                if rxSensor > sxSensor:
                    b = rxSensor - sensorsensor*self.cos5
                else:
                    b = sxSensor - sensorsensor*self.cos5

                sinAngle = (b*b)/(h*h + b*b)
                targetSpeed = self.maxSpeed*(sensorsensor*sinAngle/self.maxSpeedDist)
            
            return 2/(1+math.exp(sensor['speedX']-targetSpeed)) - 1
        else:
            return 0.3

    def filterABS(self, sensor, brake):
        speed = sensor['speedX']/3.6
        if speed < self.absMinSpeed: return brake
        
        slip = 0
        for i in xrange(4):
            slip += sensor['wheelSpinVel'][i]*self.wheelRadius[i]
        
        slip = speed - slip/4
        if slip > self.absSlip:
            brake -= (slip - self.absSlip)/self.absRange
        
        if brake < 0:
            return 0
        else:
            return brake

    def clutching(self, sensor, clutch):
        maxClutch = self.clutchMax

        if sensor['curLapTime'] < self.clutchDeltaTime and \
           self.stage==RACE and \
           sensor['distRaced'] < self.clutchDeltaRaced:
            clutch = maxClutch
        
        if clutch > 0:
            delta = self.clutchDelta
            if sensor['gear'] < 2:
                delta /= 2
                maxClutch *= clutchMaxModifier
                if sensor['curLapTime'] < self.clutchMaxTime:
                    clutch = maxClutch
            
            clutch = min([maxClutch, clutch])

            if clutch != maxClutch:
                clutch -= delta
                clutch = max([0, clutch])
            else:
                clutch -= self.clutchDec
        
        return clutch