__author__ = 'kyle'
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)


def finish():
    GPIO.cleanup()


class DigitalInput(object):
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN)

    def get(self):
        return GPIO.input(self.pin)


class PIR(DigitalInput):
    def detect_motion(self):
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
        return ((total_time / 1000.0) / 1.0e-6) * 21


class Output(object):
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    def turn_on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def turn_off(self):
        GPIO.output(self.pin, GPIO.LOW)


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
