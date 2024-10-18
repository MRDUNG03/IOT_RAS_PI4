import socket  #cung cấp các giao diện mạng cấp thấp để làm việc với các kết nối mạng , gồm slave và master
from time import sleep # thư viện về thời gian được tính bằng giây
from random import randint #thư viện random một số nguyễn ngẫu nhiên từ 2 số nguyên được cho
from urllib import request, parse #thư viện sử dụng giao thức HTTP
import json
from datetime import datetime

channel_id = '2654555' #id của channels từ thingspeak
api_key_write = '4J01GFUKQXXQ4ZR9' # API viết từ thingspeak

def make_param_thingspeak(humi, temp): # chứa tham số nhiệt độ và độ ẩm và gửi lên thingspeak hai giá trị của hàm
    params = parse.urlencode({'field1': humi, 'field2': temp}).encode() # má hóa dữ liệu .encode là chuyển chuổi thành byte và gửi lên thingspeak
    return params # trả về chuỗi tham số đã mã hóa

def thingspeak_post(params): #tạo 1 funcion trong dó có chứa hàm(tham số đầu vào ).gửi lên thingspeak
    req = request.Request('https://api.thingspeak.com/update', method="POST") #tạo 1 đối tượng là Request nó yêu cầu http đến url. method post dùng đẻ gửi dữ liệu
    req.add_header("Content-Type", "application/x-www-form-urlencoded") #gửi dữ liệu theo định dạng urlencoded
    req.add_header("X-THINGSPEAKAPIKEY", api_key_write) #khóa api xác thực từ thingspeak
    r = request.urlopen(req, data=params) # urlopen gửi yêu cầu HTTP POST tới ThingSpeak với dữ liệu là params,params là chuỗi byte đã mã hóa là nhiệt độ và độ ẩm 
    response_data = r.read() #  đọc và trả data phản hồi và nó sẽ lưu vào response_data
    return response_data #hàm trả về dữ liệu phản hồi , bao gồm các trạng thái của dữ liệu trên thingspeak

def calculate_crc(frame): # hàm tính toán CRC_BYTE 
    crc = 0 #giá trị ban đầu = 0 
    for byte in frame[:-2]:  # Không tính Stop byte và CRC byte,lấy tất cả các phần tử ở frame đầu tiên đến vị trí trước hai phần tử cuối cùng
        crc ^= byte #phép toán XOR
    return crc # trả về giá trị crc vừa được tính toán

def calculate_crc_re(frame):
    crc = 0 #giá trị ban đầu = 0 
    for byte in frame: # duyệt qua tất cả các byte trong chuỗi dữ liệu frame
        crc ^= byte #phép toán XOR
    return crc #trả về giá trị crc vừa được tính toán

def build_frame(start_byte, id_byte, cmd_byte, data):
    length_byte = len(data) #Tính độ dài của chuỗi dữ liệu
    frame2 = bytearray() #kiểu dữ liệu có thể mở rộng cho các byte , tạo khung data
    frame2.append(start_byte)  # Start byte,append : thêm byte đầu tiên 
    frame2.append(id_byte)     # ID byte
    frame2.append(cmd_byte)    # CMD byte
    frame2.append(length_byte) # Length byte
    frame2.extend(data)        # Data bytes
    crc_byte = calculate_crc_re(frame2)  # CRC byte
    frame2.append(crc_byte) #Thêm byte CRC vào cuối khung
    frame2.append(0xFF)  # Stop byte (giả sử 0xFF là Stop byte)
    return frame2 #Hàm trả về khung dữ liệu hoàn chỉnh (kiểu bytearray), bao gồm: Start byte, ID byte, CMD byte, Length byte, Dữ liệu, CRC byte, và Stop byte.

def parse_frame(frame, server_socket, addr, led1, led2, led3): # chúng ta khai bám một hàm truyền mảng data
    start_byte = frame[0] # lấy ở vị trí đầu tiên trong mảng  data frame
    id_byte = frame[1] # lấy vị trị thứ 1 trong mảng data frame 
    cmd_byte = frame[2] #lấy vị trí thứ 2 trong mảng data frame
    length_byte = frame[3] # lấy vị trí thứ 3 trong mảng data frame
    data = frame[4:4 + length_byte] # lấy từ vị trí thứ 4 trong magnr và cộng với độ dài của chiều dữ liệu tư data
    crc_byte = frame[-2]
    stop_byte = frame[-1]

    
    if stop_byte != 0xFF:
        print("Lỗi: Sai Stop byte")
        return
    if crc_byte != calculate_crc(frame):
        print("Lỗi: Sai CRC byte")
        return

    message = data.decode('utf-8')  # Chuyển mảng byte thành chuỗi
    print(f"Frame hợp lệ: Start byte = {start_byte}, ID = {id_byte}, CMD = {cmd_byte}, Data = {message}, CRC = {crc_byte} ,length  = {length_byte}, stop = {stop_byte}")

    data_parts = message.split('&')
    tem = int(data_parts[0]) 
    hum = int(data_parts[1])

    # Build response frame
    response_data = ("{}&{}&{}".format(led1, led2, led3)).encode()
    # 
    response_frame = build_frame(start_byte=0x80, id_byte=0x01, cmd_byte=0x01, data=response_data)
    server_socket.sendto(response_frame, addr)
    print(f"Đã gửi phản hồi về {addr}: {response_frame}")

    return tem, hum

def main():
    # Create TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 8000))
    server_socket.listen(5)  # Start listening for incoming connections
    print("TCP Server đang lắng nghe...")
    client_socket, addr = server_socket.accept()
    print(f"Kết nối từ {addr}")
        
    while True:
        try:
            avghum = 0.0
            avgtem = 0.0

            # Accept incoming connection
            
            for i in range(20):
                led1 = randint(0, 1)
                led2 = randint(0, 1)
                led3 = randint(0, 1)

                frame = client_socket.recv(1024)
                print(f"Nhận từ {addr}: {frame}")

                tem, hum = parse_frame(frame, client_socket, addr, led1, led2, led3)
                avghum += hum
                avgtem += tem

                # In ra kết quả
                print(f"Nhiệt độ (tem) thứ {i}: {tem}")
                print(f"Độ ẩm (hum) thứ {i}: {hum}")
                print("----------------------------------------")

            # Calculate and print averages
            avghum /= 20
            avgtem /= 20
            print("Độ ẩm trung bình (hum):", avghum)
            print("Nhiệt độ trung bình (tem):", avgtem)

            # Send data to ThingSpeak
            params_thingspeak = make_param_thingspeak(avghum, avgtem)
            thingspeak_post(params_thingspeak)
 
        except Exception as e:
            print(f"Lỗi: {e}")
            sleep(1)  # Wait before retrying in case of an error
        
main()