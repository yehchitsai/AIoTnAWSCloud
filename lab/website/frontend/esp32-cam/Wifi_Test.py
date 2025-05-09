# enable station interface and connect to Wi-Fi access point
import network, time, machine
import binascii

# WiFi configuration
SSID = '自己熱點'
PASSWORD = '熱點密碼'
ip_address = ''

def connect_wifi():
    global ip_address
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
            print('.',end='')
            pass
    print('network config: ', wlan.ifconfig())
    ip_address = wlan.ifconfig()[0]
    print('MAC Address: ',binascii.hexlify(wlan.config('mac')).decode())

def get_address():
    global ip_address
    return ip_address
connect_wifi()
#wlan.disconnect()

