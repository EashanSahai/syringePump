from stepper import Stepper
from time import sleep

GPIO_PA = 1
GPIO_PA_ = 7
GPIO_PB = 8
GPIO_PB_ = 25

GPIO_SWITCH_FULL = 21
GPIO_SWITCH_EMPTY = 20

print "Initializing stepper"
stepper = Stepper(GPIO_PA, GPIO_PA_, GPIO_PB, GPIO_PB_, GPIO_SWITCH_FULL, GPIO_SWITCH_EMPTY)

print "MAX CCW"
stepper.step_max_ccw()

print "MAX CW"
stepper.step_max_cw()

count = 100
while(count > 0):
	count -= 1
	stepper.step(10, Stepper.DIR_CCW)
	stepper.off()
	sleep(0.5)

