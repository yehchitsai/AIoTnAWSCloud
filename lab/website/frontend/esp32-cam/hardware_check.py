import camera
import io, sys
import base64, json
import urequests as requests
import time, network, ntptime
import machine
import gc
from machine import Timer, Pin, PWM
from microdot import Microdot, Response

(STANDBY, WIFI, CAMERA, ERROR) = (1000, 500, 100, 10)
LED_PIN_NO = 33

# Wi-Fi 設定
SSID = "WiFi_SSID"
PASSWORD = "WiFi_PASSWORD"

# 1. 設定燈號
def led_blink_timed(timer, led_pin, millisecond):
    period = int(0.5 * millisecond)
    timer.init(period=period, mode=Timer.PERIODIC, callback=lambda t: led_pin.value(not led_pin.value()))
    
led_pwm = Pin(LED_PIN_NO, Pin.OUT) # PWM(pin, freq)
timer = Timer(1) # 創建定時器對象

# 2.連上網路
led_blink_timed(timer, led_pwm, WIFI)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        pass
print('1. Wi-Fi okay.\n network config: ', wlan.ifconfig())

# 3. 網路校時
ntptime.host = 'time.stdtime.gov.tw'
while True:
    try:
        ntptime.settime()
    except:
        print('wait for time server')
        led_blink_timed(timer, led_pwm, ERROR)
        sys.exit(1)        
    else:
        break

taipei_timezone = 8
(year, month, day, hour, minute, second, weekday, yearday) = time.gmtime(time.time())
timeforRTC = (year, month, day, weekday, hour + taipei_timezone, minute, second, yearday)
machine.RTC().datetime(timeforRTC)
print("根據時間調整後的本地時間：%s" %str(time.localtime()))
print('2. NTP okay.')

# 4. 測試 https 連線
url = "https://www.uniheart.com.tw/"
try:
    r = requests.get(url)
    print(r.status_code)
except:
    print('https connection error')
    led_blink_timed(timer, led_pwm, ERROR)
    sys.exit(1)
print('3. HTTPS okay.')

# 5. 設定攝影機
led_blink_timed(timer, led_pwm, CAMERA)
camera_status = camera.init()
if camera_status:
    camera.framesize(7)# 解析度
    camera.quality(50)
    camera.speffect(0)
else:
    print('ternimate program')
    led_blink_timed(timer, led_pwm, ERROR)
    sys.exit(1)
print('4. CAMERA okay.')

# 啟動 `microdot` 伺服器
app = Microdot()
# 設定 Response 類型
Response.default_content_type = 'text/html'

# 網頁前端介面
HTML_PAGE = """\
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>ESP32-CAM Stream - Microdot</title>
</head>
<body>
    <h2>ESP32-CAM 即時影像 - using Microdot</h2>
    <img id="video_feed" src="/capture" width="320">
    <br>
    <button onclick="capture()">擷取圖片</button>
    <script>
        function capture() {
            var link = document.createElement('a');
            link.href = '/capture';
            link.download = 'esp32_image.jpg';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
        setInterval(() => {
            document.getElementById('video_feed').src = '/capture?t=' + new Date().getTime();
        }, 500);
    </script>
</body>
</html>
"""

# 提供主頁
@app.route('/')
def index(request):
    return HTML_PAGE

# 提供即時影像
@app.route('/capture')
def capture(request):
    img = camera.capture()
    return Response(img, headers = {"Content-Type": "image/jpeg"})

# 啟動伺服器
print('5. Web Camera okay.')
app.run(port=80)
  