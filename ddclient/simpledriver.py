# =============================================================================
# Federal University of Rio Grande do Sul (UFRGS)
# Connectionist Artificial Intelligence Laboratory (LIAC)
# Renato de Pontes Pereira - rppereira@inf.ufrgs.br
# =============================================================================
# Copyright (c) 2011 Renato de Pontes Pereira, renato.ppontes at gmail dot com
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
# =============================================================================

import math
from ddclient import *

class SimpleDriver(Controller):
    def __init__(self):
        self.gearUp = [8500, 9000, 9500, 9500, 9500, 0]
        self.gearDown = [0, 3300, 6200, 7000, 7300, 7700]
        self.steerLock = 0.785398
        self.maxSpeedDist = 70.0
        self.maxSpeed = 150.0
        self.sin5 = 0.08716
        self.cos5 = 0.99619

        self.iter = 0

    def control(self, sensor):
        self.iter += 1
        if self.iter%100 == 0:
            print sensor.get('damage'), sensor.get('otherdamage')
        
        action = Action()
        action.accel = self.getAccel(sensor)
        action.steer = self.getSteer(sensor)
        action.gear = self.getGear(sensor)

        return action

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
            
            return 2.0/(1+math.exp(sensor['speedX']-targetSpeed)) - 1
        else:
            return 0.3

    def getGear(self, sensor):
        gear = sensor['gear']
        rpm = sensor['rpm']

        if gear < 1: return 1
        if gear < 6 and rpm >= self.gearUp[int(gear)-1]: 
            return gear + 1
        else:
            if gear > 1 and rpm <= self.gearDown[int(gear)-1]:
                return gear - 1
            
        return gear

    def getSteer(self, sensor):
        targetAngle = (sensor['angle']-sensor['trackPos']*0.5)

        return targetAngle/self.steerLock


if __name__ == '__main__':
    run(BatDriver())