from stepper import Stepper

GPIO_PA = 1
GPIO_PA_ = 7
GPIO_PB = 8
GPIO_PB_ = 25

GPIO_SWITCH_FULL = 21
GPIO_SWITCH_EMPTY = 20

print "Initializing Stepper"
stepper = Stepper(GPIO_PA, GPIO_PA_, GPIO_PB, GPIO_PB_, GPIO_SWITCH_FULL, GPIO_SWITCH_EMPTY)
print "Turning off Stepper"
stepper.off()
