import network
import socket
import time
import camera
import sys

# WiFi 設定
SSID = "WiFi_SSID"
PASSWORD = "WiFi_PASSWORD"

# 1. 連線 WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

print("Connecting to WiFi...", end="")
while not wifi.isconnected():
    time.sleep(1)
    print(".", end="")
print("\nConnected! IP:", wifi.ifconfig()[0])

# 2. 設定攝影機
camera_status = camera.init()
if camera_status:
    camera.framesize(7)# 解析度
    camera.quality(50)
    camera.speffect(0)
else:
    print('ternimate program')
    sys.exit(1)

# 啟動 HTTP 伺服器
def start_server():
    addr = ("", 80)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(addr)
    s.listen(5)
    print("Server started. Access it at http://%s" % wifi.ifconfig()[0])
    while True:
        conn, addr = s.accept()
        print("Connection from:", addr)
        request = conn.recv(1024)
        request = request.decode("utf-8")

        if ("GET /capture" in request):
            # 擷取圖片
            img = camera.capture()
            
            response = """\
HTTP/1.1 200 OK
Content-Type: image/jpeg
Content-Length: %d

""" % len(img)
            conn.send(response.encode() + img)

        elif "GET /stream" in request:
            # 串流頁面
            html = """\
HTTP/1.1 200 OK
Content-Type: text/html

<html>
<head>
    <meta charset="utf-8">
    <title>ESP32-CAM Stream</title>
</head>
<body onload="updateImage();">
    <h2>ESP32-CAM 即時影像</h2>
    <img id="esp32_image"  src="/capture" width="320">
    <br>
    <button onclick="capture()">擷取圖片</button>
    <script>
        function updateImage() {
            // Get the image element
            var image = document.getElementById("esp32_image");
            // Adding the timestamp parameter to image src
            image.src= "/capture?t="  + new Date().getTime();
            setTimeout(updateImage, 500);
        }
        function capture() {
            var link = document.createElement('a');
            link.href = '/capture';
            link.download = 'esp32_image.jpg';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    </script>
</body>
</html>
"""
            conn.send(html.encode())

        else:
            # 404 回應
            conn.send("HTTP/1.1 404 Not Found\r\n\r\n")

        conn.close()

start_server()
