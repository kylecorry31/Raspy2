__author__ = 'kyle'
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)


class Sensor(object):
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN)

    def get(self):
        return GPIO.input(self.pin)

    def __del__(self):
        GPIO.cleanup()


class Output(object):
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    def turn_on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def turn_off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def __del__(self):
        GPIO.cleanup()


class LED(Output):
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
