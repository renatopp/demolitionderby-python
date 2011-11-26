class Sensor(dict):
    def __init__(self, message):
        super(Sensor, self).__init__()
        print '>>> received:'
        self.parse(message.strip('\x00'))

    def parse(self, message):
        tokens = message.split('(')
        for token in tokens:
            reading = token.strip(')').split()
            if len(reading) > 1:
                key = reading[0]
                values = reading[1:]

                if key in ['opponents', 'track', 'wheelSpinVel', 'focus']:
                    self[key] = map(float, values)
                else:
                    print key, values
                    self[key] = float(values[0])
