# 匯入所需模組
from machine import Pin, Timer, PWM
from time import sleep

Flash_LED_Pin = 4
LED_Pin = 13

# setup gpio pin
flash_pin_pwm = PWM(Pin(Flash_LED_Pin),4)
flash_pin_pwm.duty(5)
led_pin = Pin(LED_Pin, Pin.OUT)

(STANDBY, WIFI, CAMERA, ERROR) = (1000, 500, 100, 10)

# ISR routine for led blink
def led_blink_timed(timer, led_pin, millisecond):
    period = int(0.5 * millisecond)
    timer.init(period=period, mode=Timer.PERIODIC, callback=lambda t: led_pin.value(not led_pin.value()))
    
# initiate timer
led_timer = Timer(1) 

# setup ISR
led_blink_timed(led_timer, led_pin, STANDBY)


