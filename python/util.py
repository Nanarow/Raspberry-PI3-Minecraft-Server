from gpiozero import LED, Button
from time import sleep
from screenutils import list_screens

def get_screen(name: str):
    for s in list_screens():
        if s.name == name:
            return s

class LEDState:
    red: LED
    green: LED

    def __init__(self, red_pin: int, green_pin: int):
        self.red = LED(red_pin)
        self.green = LED(green_pin)
        self.red.off()
        self.green.off()

    def danger(self):
        self.red.on()
        self.green.off()

    def warning(self,time: int = 5,delay: int = 1):
        self.green.off()
        for _ in range(time):
            self.red.on()
            sleep(delay/2.0)
            self.red.off()
            sleep(delay/2.0)
    

    def success(self):
        self.red.off()
        self.green.on()

    def off(self):
        self.red.off()
        self.green.off()


class ScreenIO:
    def __init__(self, name: str,led: tuple,button: int,timeout: int, pressed = False):
        self.name = name 
        self.led = LEDState(led[0],led[1])
        self.button = Button(button)
        self.pressed = pressed
        self.timeout = timeout