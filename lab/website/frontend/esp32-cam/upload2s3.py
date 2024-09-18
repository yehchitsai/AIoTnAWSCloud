import camera
import io
import base64, json
import urequests as requests
import time, network, ntptime
import machine
import gc
from machine import Timer, Pin, PWM
(STANDBY,RUN, ERROR) = (500, 100, 10)
ESP32_STATE = STANDBY
# 1. 設定燈號
def led_blink_timed(timer, led_pin, millisecond):
    period = int(0.5 * millisecond)
    timer.init(period=period, mode=Timer.PERIODIC, callback=lambda t: led_pin.value(not led_pin.value()))
    
led_pwm = Pin(33, Pin.OUT) # PWM(pin, freq)
timer = Timer(1) # 創建定時器對象
led_blink_timed(timer, led_pwm, RUN)

# 2.連上網路
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect('SSID', 'PASSWORD')
    while not wlan.isconnected():
        pass
print('network config: ', wlan.ifconfig())

# 3. 網路校時
ntptime.host = 'time.stdtime.gov.tw'
while True:
    try:
        ntptime.settime()
    except:
        print('wait for time server')
    else:
        break

taipei_timezone = 8
(year, month, day, hour, minute, second, weekday, yearday) = time.gmtime(time.time())
timeforRTC = (year, month, day, weekday, hour + taipei_timezone, minute, second, yearday)
machine.RTC().datetime(timeforRTC)
print("根據時間調整後的本地時間：%s" %str(time.localtime()))

# 4 configure camera
led_blink_timed(timer, led_pwm, STANDBY)
camera_status = camera.init()
if camera_status:
    camera.framesize(7)
    camera.quality(50)
    camera.speffect(2)
else:
    led_blink_timed(timer, led_pwm, ERROR)
    while True:
        time.sleep(2)
#
while True:
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    url = 'API_upload_image'
    # 5. 拍照並上傳影像到 S3
    led_blink_timed(timer, led_pwm, RUN)
    r = requests.post(url, data=json.dumps({"key": base64.encodebytes(camera.capture())}), headers=headers)
    print(r.text,dir(r))
    led_blink_timed(timer, led_pwm, STANDBY)
    time.sleep(2)
    gc.collect()
camera.deinit()

