from time import sleep
import socket
from random import randint
from grove.grove_ryb_led_button import GroveLedButton # Hàm GroveLedButton dùng để điều khiển red led button
from grove.display import JHD1802
from seeed_dht import DHT

LED1 = GroveLedButton(16)  # Khai báo chân Red Led Button ở cổng D5
LED2 = GroveLedButton(18)
LED3 = GroveLedButton(22)
lcd = JHD1802()
sensor = DHT('11', 5)       # Khai báo chân cảm biến nhiệt độ độ ẩm DHT11 ở cổng D5
def control(message):
    btn_str = message
    btn = btn_str.split('&')#[1&0&1]
    if (int(btn[0]) == 1):
        LED1.led.light(True)
        print('Led 1 on!')
    else:
        LED1.led.light(False)
        print('Led 1 off!')
        
    if (int(btn[1]) == 1):
        LED2.led.light(True)
        print('Led 2 on!')
    else:
        LED2.led.light(False)
        print('Led 2 off!')    
    
    if (int(btn[2]) == 1):
        LED3.led.light(True)
        print('Led 3 on!')
    else:
        LED3.led.light(False)
        print('Led 3 off!')


def calculate_crc(frame):
    crc = 0
    for byte in frame:
        crc ^= byte
    return crc

def calculate_crc_re(response): # Tính CRC 
    crc = 0
    for byte in response[:-2]:  # Không tính Stop byte và CRC byte
        crc ^= byte
    return crc


def parse_frame(response, client_socket, addr):
    #print(response)
    start_byte = response[0]
    id_byte = response[1]
    cmd_byte = response[2]
    length_byte = response[3]
    data = response[4:4+length_byte]
    crc_byte = response[-2]
    stop_byte = response[-1]    
    
    # Kiểm tra tính hợp lệ của Frame
    if stop_byte != 0xFF:
        print("Lỗi: Error Stop byte")
        return
    if (crc_byte) != calculate_crc_re(response):
        print(f"Lỗi: Error CRC byte: {crc_byte} - {calculate_crc_re(response)}")
        return
    
    # Giải mã Data từ byte thành chuỗi
    message = data.decode('utf-8')  # Chuyển mảng byte thành chuỗi
    print(f"Frame hợp lệ: Start byte = {start_byte}, ID = {id_byte}, CMD = {cmd_byte}, Data = {message}, CRC = {crc_byte} ,length  = {length_byte}, stop = {stop_byte}")

    # Chuỗi dữ liệu cần tách
    data_str = message
    return data_str

# Tạo Frame
def build_frame(start_byte, id_byte, cmd_byte, data):
    length_byte = len(data)  # Độ dài của phần Data
    frame = bytearray()
    # Thêm các byte vào Frame
    frame.append(start_byte)        # Start bytes
    frame.append(id_byte)           # ID byte
    frame.append(cmd_byte)          # CMD byte
    frame.append(length_byte)       # Length byte
    frame.extend(data)              # Data bytes
    # Tính CRC byte
    crc_byte = calculate_crc(frame)
    frame.append(crc_byte)          # CRC byte
    # Thêm Stop byte
    frame.append(0xFF)              # Stop byte (giả sử 0xFF là Stop byte)
    return frame


def main():
    # Tạo socketTCPđể gửi và nhận dữ liệu
    client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    client_socket.settimeout(10)  # Đặt thời gian chờ để nhận phản hồi
    server_address = ('192.168.171', 8000)
    while True:
        try:
            # Gửi Frame
            hum, tem = sensor.read()
            lcd.clear()
            lcd.setCursor(0,0)
            lcd.write("  Tem: {}".format(tem))
            lcd.setCursor(1,0)
            lcd.write("  Hum: {}".format(hum))
            data = ("{}&{}".format(tem,hum)).encode()
            frame = build_frame(start_byte=0x80, id_byte=0x01, cmd_byte=0x01, data=data)
            client_socket.sendto(frame, server_address)
            print("Đã gửi Frame:", frame)
            sleep(1)
            # Nhận phản hồi từ Master
            response, addr = client_socket.recvfrom(1024)
            message = parse_frame(response, client_socket, addr)
            print("Phản hồi từ Master:", message)
            control(message)
            print("-------------------------------------")
        except:
            print("Lỗi: Không nhận được phản hồi từ Master")
            sleep(2)
     
