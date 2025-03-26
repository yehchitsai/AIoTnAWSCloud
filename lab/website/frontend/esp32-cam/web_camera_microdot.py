from microdot import Microdot, Response
import network
import camera
import time
import sys

# 設定 Response 類型
Response.default_content_type = 'text/html'

# Wi-Fi 設定
SSID = "WiFi_SSID"
PASSWORD = "WiFi_PASSWORD"

# 連線 Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

print("Connecting to WiFi...", end="")
while not wifi.isconnected():
    time.sleep(1)
    print(".", end="")
print("\nConnected! IP:", wifi.ifconfig()[0])

# 設定攝影機
camera_status = camera.init()
if camera_status:
    camera.framesize(7)# 解析度
    camera.quality(50)
    camera.speffect(0)
else:
    print('ternimate program')
    sys.exit(1)

# 啟動 `microdot` 伺服器
app = Microdot()

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
app.run(port=80)
