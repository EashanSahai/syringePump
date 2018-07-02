from gpiozero import Button, DigitalOutputDevice
from time import sleep

class Stepper():

    DELAY_MILLI_NORMAL = 1.0
    DELAY_MILLI_SLOW = 10.0
    DELAY_MILLI_VERY_SLOW = 20.0
    BOUNCE_TIME = 0.01  # Setting bounce time to 10/1000 seconds

    LARGE_COUNT = 100000

    DIR_CW = -1
    DIR_CCW = 1

    HalfStep = [
        [ 1, 0, 0, 0 ],
        [ 1, 0, 1, 0 ],
        [ 0, 0, 1, 0 ],
        [ 0, 1, 1, 0 ],
        [ 0, 1, 0, 0 ],
        [ 0, 1, 0, 1 ],
        [ 0, 0, 0, 1 ],
        [ 1, 0, 0, 1 ]
    ]

    MAX_COUNT = 5

    def __init__(self, pin_pa, pin_pa_, pin_pb, pin_pb_, pin_sw_cw, pin_sw_ccw):
        self.pa = DigitalOutputDevice(pin_pa)
        self.pa_ = DigitalOutputDevice(pin_pa_)
        self.pb = DigitalOutputDevice(pin_pb)
        self.pb_ = DigitalOutputDevice(pin_pb_)
        self.switch_cw = Button(pin_sw_cw, bounce_time=Stepper.BOUNCE_TIME)
        self.switch_ccw = Button(pin_sw_ccw, bounce_time=Stepper.BOUNCE_TIME)
        self.stepNo = 0
	self.off()

    def off(self):
        self.pa.off()
        self.pa_.off()
        self.pb.off()
        self.pb_.off()

    def step_max_cw(self):
        return self.step(Stepper.LARGE_COUNT, Stepper.DIR_CW)

    def step_max_ccw(self):
        return self.step(Stepper.LARGE_COUNT, Stepper.DIR_CCW)

    def step(self, count, dir):
        # While there are more steps to move
        while (count > 0):
            # If dir = DIR_CW and if CW limit switches has been pressed, then return
            if dir == Stepper.DIR_CW and self.switch_cw.is_pressed:
                return count
            # If dir = DIR_CCW and if CCW limit switches has been pressed, then also return
            elif dir == Stepper.DIR_CCW and self.switch_ccw.is_pressed:
                return count

            count -= 1

            if (self.stepNo < 0):
                self.stepNo = 7
            elif (self.stepNo > 7):
                self.stepNo = 0

            self.pa.on() if Stepper.HalfStep[self.stepNo][0] else self.pa.off()
            self.pa_.on() if Stepper.HalfStep[self.stepNo][1] else self.pa_.off()
            self.pb.on() if Stepper.HalfStep[self.stepNo][2] else self.pb.off()
            self.pb_.on() if Stepper.HalfStep[self.stepNo][3] else self.pb_.off()

            self.stepNo += dir

            if (count < 20):
                delay = Stepper.DELAY_MILLI_VERY_SLOW
            elif (count < 50):
                delay = Stepper.DELAY_MILLI_SLOW
            else:
                delay = Stepper.DELAY_MILLI_NORMAL

            sleep(delay/50000000.0)

        return count

