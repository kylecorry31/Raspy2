import RPi.GPIO as GPIO
import time
import math

GPIO.setmode(GPIO.BOARD)


def finish():
    """Use this at the end of every program to reset the GPIO pins of the Pi."""
    GPIO.cleanup()


class DigitalInput(object):
    def __init__(self, pin):
        """A digital input on the Pi."""
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN)

    def get(self):
        """Get the current value of the digital input pin."""
        return GPIO.input(self.pin)


class PIR(DigitalInput):
    def detect_motion(self):
        """Detects motion using the PIR sensors."""
        return bool(self.get())


class AnalogInput(object):
    def __init__(self, pin, capacitance=1e-6):
        self.pin = pin
        self.capacitance = capacitance

    def get_resistance(self):
        GPIO.setmode(GPIO.BOARD)
        start_time = time.time()
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(0.1)
        GPIO.setup(self.pin, GPIO.IN)
        while GPIO.input(self.pin) == GPIO.LOW:
            pass
        total_time = time.time() - start_time
        return math.round(((total_time / 1000.0) / self.capacitance - 100.208) / 0.0004906)


class Output(object):
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    def turn_on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def turn_off(self):
        GPIO.output(self.pin, GPIO.LOW)


class Ultrasonic(object):
    def __init__(self, triggerPin, echoPin):
        self.triggerPin = triggerPin
        self.echoPin = echoPin
        GPIO.setup(self.triggerPin, GPIO.OUT)
        GPIO.setup(self.echoPin, GPIO.IN)
        time.sleep(0.1)

    def get_distance(self):
        """Gets the current distance in CM"""
        GPIO.output(self.triggerPin, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.triggerPin, GPIO.LOW)
        while GPIO.input(self.echoPin) == 0:
            pass
        start = time.time()
        while GPIO.input(self.echoPin) == 1:
            pass
        stop = time.time()
        return (stop - start) * 17000


class LED(Output):
    def __init__(self, pin):
        super(LED, self).__init__(pin)
        self.pwm = None

    def set_brightness(self, brightness):
        """Sets the brightness of the LED. Brightness ranges from 0 (off) to 100 (fully on)."""
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(brightness)

    def turn_on(self):
        if self.pwm:
            self.pwm.stop()
        super(LED, self).turn_on()

    def turn_off(self):
        if self.pwm:
            self.pwm.stop()
        super(LED, self).turn_off()
