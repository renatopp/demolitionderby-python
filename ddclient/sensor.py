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

class Sensor(dict):
    def __init__(self, message):
        super(Sensor, self).__init__()
        # print '>>> received:'
        self.parse(message.strip('\x00'))

    def parse(self, message):
        tokens = message.split('(')
        for token in tokens:
            reading = token.strip(')').split()
            if len(reading) > 1:
                key = reading[0]
                values = reading[1:]
                if key in ['opponents', 'track', 'wheelSpinVel', 'focus']:
                    # print key, values
                    self[key] = map(float, values)
                else:
                    # print key, values
                    self[key] = float(values[0])
        
        self['minOpponents'] = self['opponents'].index(min(self['opponents']))
        self['minOpponentsDistance'] = self['opponents'][self['minOpponents']]
        self['minOpponentsAngle'] =  math.radians(180 - self['minOpponents']*10)
        