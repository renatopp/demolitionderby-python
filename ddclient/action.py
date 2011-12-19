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

class Action(object):
    _accel = 0
    _brake = 0
    _clutch = 0
    _gear = 0
    _steer = 0
    meta = 0
    focus = 360

    def __init__(self, accel=0, brake=0, clutch=0, gear=0, steer=0, meta=0, focus=360):
        self.accel = accel
        self.brake = brake
        self.clutch = clutch
        self.gear = gear
        self.steer = steer
        self.meta = meta
        self.focus = focus
    
    def get_accel(self): return self._accel
    def set_accel(self, value): self._accel = max(0, min(1, value))
    accel = property(get_accel, set_accel)

    def get_brake(self): return self._brake
    def set_brake(self, value): self._brake = max(0, min(1, value))
    brake = property(get_brake, set_brake)

    def get_clutch(self): return self._clutch
    def set_clutch(self, value): self._clutch = max(0, min(1, value))
    clutch = property(get_clutch, set_clutch)

    def get_steer(self): return self._steer
    def set_steer(self, value): self._steer = max(-1, min(1, value))
    steer = property(get_steer, set_steer)

    def get_gear(self): return self._gear
    def set_gear(self, value): self._gear = max(-1, min(6, value))
    gear = property(get_gear, set_gear)

    def __str__(self):
        return '(accel %.4f) (brake %.4f) (clutch %.4f) (gear %.4f) (steer %.4f) (meta %.4f) (focus %.4f)' % (self.accel, self.brake, self.clutch, self.gear, self.steer, self.meta, self.focus)