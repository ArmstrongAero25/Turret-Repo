
from adafruit_servokit import Servokit
import time

kit = Servokit(16)

kit.servo[14].throttle = 1
time.sleep(1)
kit.servo[14].throttle = 0
