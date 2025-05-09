from microdot import Microdot, Response, send_file
import json
import camera
import time
import sys

# 設定 Response 類型，讓它支援二進制數據
Response.default_content_type = 'text/html'

# ====== 初始化攝影機 ======
def init_camera():
    try:
        camera_status = camera.init()
        if camera_status:
            camera.framesize(7)# 解析度
            camera.quality(50)
            camera.speffect(0)
            print("攝影機初始化完成")
        else:
            print('ternimate program')
            release_camera()
            sys.exit(1)
    except Exception as e:
        print("攝影機初始化失敗:", e)
        sys.exit(1)

# ====== 釋放攝影機資源（手動中斷時用） ======
def release_camera():
    try:
        camera.deinit()
        print("攝影機資源已釋放")
    except:
        pass


# 啟動 `microdot` 伺服器
app = Microdot()

# 提供主頁
@app.route('/')
def index(request):
    return send_file('/index.html')

# 提供即時影像
@app.route('/capture')
def capture(request):
    img = camera.capture()
    return Response(img, headers = {"Content-Type": "image/jpeg"})

# 設定攝影機參數
@app.route('/config', methods=['POST'])
def config(request):
    try:
        data = json.loads(request.body)
        if 'framesize' in data:
            camera.framesize(int(data['framesize']))
        if 'quality' in data:
            camera.quality(int(data['quality']))
        if 'brightness' in data:
            camera.brightness(int(data['brightness']))
        if 'contrast' in data:
            camera.contrast(int(data['contrast']))
        if 'saturation' in data:
            camera.saturation(int(data['saturation']))
        return Response(json.dumps({"status": "ok"}), headers={"Content-Type": "application/json"})
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500)

# 1. 設定 LED 燈號
from led_Test import *
# 連接 Wi-Fi 網路
led_blink_timed(led_timer, led_pin, WIFI)
import Wifi_Test
ip = Wifi_Test.get_address()
# 啟動攝影機
led_blink_timed(led_timer, led_pin, CAMERA)
init_camera()
# 啟動伺服器
try:
    app.run(port=80)
    led_blink_timed(led_timer, led_pin, STANDBY)
except OSError as e:
    print("伺服器啟動錯誤{}".format(e))
    led_blink_timed(led_timer, led_pin, ERROR)