import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)


def finish():
    """Use this at the end of every program to reset the GPIO pins of the Pi."""
    GPIO.cleanup()


class DigitalInput(object):
    """A digital sensor for the Raspberry Pi."""

    def __init__(self, pin):
        """A digital input on the Pi."""
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN)

    def get(self):
        """Get the current value of the digital input pin."""
        return GPIO.input(self.pin)


class PIR(DigitalInput):
    """A passive infrared sensor for the Raspberry Pi. Used to detect motion."""

    def detect_motion(self):
        """Detects motion using the PIR sensors."""
        return bool(self.get())


class Ultrasonic(object):
    """An ultrasonic sensor for the Raspberry Pi. Used to detect distance."""

    def __init__(self, triggerPin, echoPin):
        self.triggerPin = triggerPin
        self.echoPin = echoPin
        GPIO.setup(self.triggerPin, GPIO.OUT)
        GPIO.setup(self.echoPin, GPIO.IN)
        self.pwm = GPIO.pwm(self.triggerPin, 40)
        time.sleep(0.1)

    def get_distance(self):
        """Gets the current distance in CM"""
        self.pwm.start(12)
        time.sleep(0.0001)
        self.pwm.stop()
        while GPIO.input(self.echoPin) == GPIO.LOW:
            pass
        start = time.time()
        while GPIO.input(self.echoPin) == GPIO.HIGH:
            pass
        stop = time.time()
        return (stop - start) * 17000


class AnalogInput(object):
    """An analog sensor for the Raspberry Pi."""

    def __init__(self, pin, capacitance=1e-6):
        self.pin = pin
        self.capacitance = capacitance

    def get_resistance(self):
        """Gets the current resistance in ohms"""
        GPIO.setmode(GPIO.BOARD)
        start_time = time.time()
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(0.1)
        GPIO.setup(self.pin, GPIO.IN)
        while GPIO.input(self.pin) == GPIO.LOW:
            pass
        total_time = time.time() - start_time
        return round(total_time / self.capacitance)


class Output(object):
    """An output device for the Raspberry Pi."""

    def __init__(self, pin):
        self.pin = pin
        self.pwm = None
        GPIO.setup(self.pin, GPIO.OUT)

    def turn_on(self):
        """Turns on the output device"""
        if self.pwm:
            self.pwm.stop()
        GPIO.output(self.pin, GPIO.HIGH)

    def turn_off(self):
        """Turns off the output device"""
        if self.pwm:
            self.pwm.stop()
        GPIO.output(self.pin, GPIO.LOW)


class LED(Output):
    """A light emitting diode for the Raspberry Pi."""

    def set_brightness(self, brightness):
        """Sets the brightness of the LED. Brightness ranges from 0 (off) to 100 (fully on)."""
        self.pwm = GPIO.PWM(self.pin, 50)
        self.pwm.start(brightness)
