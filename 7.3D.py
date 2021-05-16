import RPi.GPIO as GPIO
import time

# GPIO Pins
TRIGGER_PIN = 23
ECHO_PIN = 24
LED_PIN = 26


# GPIO Setups
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)
LEDBrightness = GPIO.PWM(LED_PIN, 50)
LEDBrightness.start(0)

def distance():
    time.sleep(0.1)
    # Trigger set to high to create bursts.
    GPIO.output(TRIGGER_PIN, True)
    
    # Wait 0.01ms and set Trigger to low.
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, False)
 
    # Record time of sending bursts.
    while GPIO.input(ECHO_PIN) == 0:
        SentTime = time.time()

    # Record time of bursts returning.
    while GPIO.input(ECHO_PIN) == 1:
        RecieveTime = time.time()

    # Determine time taken to recieve response.
    ResponseTime = RecieveTime - SentTime

    # Determine distance by multiplying with speed of sound
    # divided by 2 as we have the time to and from the target.
    # Returns distance in cm.
    Distance = (ResponseTime * 34300) / 2
    return Distance

# Adjusts LED brightness based on object distance. Light begins increasing under 1 metre.
def AdjustLight(ObjectDistance):
    if ObjectDistance < 100:
        LEDBrightness.ChangeDutyCycle(round(100 - ObjectDistance))
    else:
        LEDBrightness.ChangeDutyCycle(0)
        
# Looping over functions reading distance and adjusting LED until keyboard interrupt.
try:

    while 1:
        ObjectDistance = distance()
        AdjustLight(ObjectDistance)
        
except KeyboardInterrupt:
    LEDBrightness.stop()
    GPIO.cleanup()