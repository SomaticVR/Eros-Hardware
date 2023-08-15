#!/bin/python3
import xarm

# arm is the first xArm detected which is connected to USB
arm = xarm.Controller('USB', debug=True)
print('Battery voltage in volts:', arm.getBatteryVoltage())

servo1 = xarm.Servo(1)
servo2 = xarm.Servo(2)
servo3 = xarm.Servo(3)
servo4 = xarm.Servo(4)
servo5 = xarm.Servo(5)
servo6 = xarm.Servo(6)

# Gets the position of servo 1 in units
position = arm.getPosition(1)
print('Servo 1 position:', position)

# Gets the position of servo 2 as defined above
position = arm.getPosition(servo2)
print('Servo 2 position:', position)

# Gets the position of servo 3 in degrees
position = arm.getPosition(3, True)
print('Servo 3 position (degrees):', position)

# Gets the position of servo 2 as defined above
# It is not necessary to set the degreees parameter
# because the Servo object performes that conversion
position = arm.getPosition([servo1, servo2, servo3])
print('Servo 1 position (degrees):', servo1.angle)
print('Servo 2 position (degrees):', servo2.angle)
print('Servo 3 position (degrees):', servo3.angle)
print('Servo 4 position (degrees):', servo4.angle)
print('Servo 5 position (degrees):', servo5.angle)
print('Servo 6 position (degrees):', servo6.angle)