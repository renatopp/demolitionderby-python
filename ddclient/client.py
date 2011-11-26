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
            self.act(action)
        
        controller.shutdown()
        self.__socket.close()

def run(controller):
    client.loadParameters()
    client.connect()
    client.run(controller)
