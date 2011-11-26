class Controller(object):
    def initAngle(self):
        return [-90+i*10 for i in xrange(19)]

    def control(self, sensor):
        pass

    def reset(self):
        pass

    def shutdown(self):
        pass

    def action(self, accel=0, brake=0, clutch=0, gear=0, steer=0, meta=0, focus=360):
        return '(accel %d) (brake %d) (clutch %d) (gear %d) (steer %d) (meta %d) (focus %d)' % (accel, brake, clutch, gear, steer, meta, focus)