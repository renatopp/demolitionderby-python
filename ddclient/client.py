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

import sys
import socket
import select

from sensor import Sensor

class Client(object):
    host = 'localhost'
    port = 3001
    id = 'championship2011'
    maxEpisodes = 1
    maxSteps = 0
    stage = 0
    trackName = 'unknown'

    def __init__(self):
        self.currStep = 0
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def loadParameters(self, argv=None):
        argv = argv or sys.argv

        for arg in argv[1:]:
            key, value = arg.split(':')

            if key == 'host': self.host = value
            elif key == 'port': self.port = int(value)
            elif key == 'id': self.id = value
            elif key == 'stage': self.stage = int(value)
            elif key == 'trackName': self.trackName = value
            elif key == 'maxEpisodes': self.maxEpisodes = int(value)
            elif key == 'maxSteps': self.maxSteps = int(value)

    def connect(self, host=None, port=None, id=None):
        host = host or self.host
        port = port or self.port
        id = id or self.id
        angles = [-90+i*10 for i in xrange(19)]
        initStr = '%s(init %s)'%(id, ' '.join(map(str, angles)))

        self.__socket.connect((host, port))
        self.__socket.send(initStr)
        self.__socket.recv(65255)

    def receive_async(self):
        r, _1, _2 = select.select([self.__socket], [], [])
        if r:
            return self.__socket.recv(65255)
        else:
            return None

    def receive(self):
        return self.__socket.recv(65255)

    def act(self, action):
        self.__socket.send(action or '(accel 1) (brake 0) (clutch 0) (gear 1) (steer 0) (meta 0) (focus 0)')

    def run(self, controller):
        while True:
            reading = self.receive()
            if '***shutdown***' in reading:
                print 'leaving...'
                break
            
            if '***restart***' in reading:
                controller.reset()
                print 'restarting...'
                break

            sensor = Sensor(reading)
            action = controller.control(sensor)

            if self.currStep >= self.maxSteps:
                action.meta = 1

            self.act(str(action))

            self.currStep += 1
        
        controller.shutdown()
        self.__socket.close()

def run(controller):
    client = Client()
    client.loadParameters()
    client.connect()
    client.run(controller)
