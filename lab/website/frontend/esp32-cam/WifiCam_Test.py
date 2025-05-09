import network
import time
import camera
import socket

# ====== 初始化攝影機 ======
def init_camera():
    try:
        camera.init()
        print("攝影機初始化完成")
    except Exception as e:
        print("攝影機初始化失敗:", e)

# ====== 釋放攝影機資源（手動中斷時用） ======
def release_camera():
    try:
        camera.deinit()
        print("攝影機資源已釋放")
    except:
        pass

# ====== 啟動 MJPEG 串流伺服器 ======
def start_stream_server(ip):
    #addr = socket.getaddrinfo(ip, 80)[0][-1]
    addr = ("", 80)
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    print("伺服器啟動，請用瀏覽器開啟：http://{}/".format(ip))

    while True:
        try:
            cl, addr = s.accept()
            cl.settimeout(10)
            print('客戶端連線：', addr)
            request = cl.recv(1024)

            if b'/stream' in request:
                cl.send(b"HTTP/1.1 200 OK\r\n")
                cl.send(b"Content-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n")
                try:
                    while True:
                        try:
                            buf = camera.capture()
                            if buf:
                                cl.send(b"--frame\r\n")
                                cl.send(b"Content-Type: image/jpeg\r\n\r\n")
                                cl.send(buf)
                                cl.send(b"\r\n")
                            time.sleep(0.1)
                        except Exception as e:
                            print("影像擷取失敗：", e)
                            break
                except Exception as e:
                    print("串流中斷：", e)
                finally:
                    cl.close()

            else:
                cl.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
                cl.send(b"""
                    <html>
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>ESP32-CAM 即時影像</title>
                        <style>
                            #img-container {
                                display: flex;
                                justify-content: center;
                                align-items: center;
                                max-width: 100%;
                                max-height: 80vh;
                                overflow: hidden;
                                margin-bottom: 20px;
                            }
                            #stream {
                                transition: transform 0.3s;
                                transform-origin: center center;
                                display: block;
                                max-width: 100%;
                                height: auto;
                            }
                        </style>
                    </head>
                    <body>
                        <h1>ESP32-CAM 影像串流</h1>

                        <label for="size">畫面大小：</label>
                        <select id="size" onchange="changeSize()">
                            <option value="320" selected>320px (QVGA)</option>
                            <option value="640">640px (VGA)</option>
                            <option value="800">800px (SVGA)</option>
                        </select>

                        <button onclick="rotateStream()">⟳ 旋轉畫面</button>

                        <br><br>
                        <div id="img-container">
                            <img id="stream" src="/stream" width="320">
                        </div>

                        <script>
                            let rotation = 0;

                            function changeSize() {
                                let w = document.getElementById("size").value;
                                document.getElementById("stream").width = w;
                            }

                            function rotateStream() {
                                rotation = (rotation + 90) % 360;
                                const img = document.getElementById("stream");
                                if (img) {
                                    img.style.transform = "rotate(" + rotation + "deg)";
                                }
                            }
                        </script>
                    </body>
                    </html>
                """)
                cl.close()
        except Exception as e:
            print("伺服器錯誤：", e)

# ====== 主流程 ======
try:
    import Wifi_Test
    ip = Wifi_Test.get_address()
    init_camera()

    for i in range(3):
        try:
            start_stream_server(ip)
            break
        except OSError as e:
            print("伺服器啟動錯誤（第 {} 次）: {}".format(i + 1, e))
            time.sleep(3)

except KeyboardInterrupt:
    print("🔴 手動中止程式，正在釋放資源...")
    release_camera()