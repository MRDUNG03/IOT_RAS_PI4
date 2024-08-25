from grove.display.jhd1802 import JHD1802

# Khởi tạo màn hình LCD
lcd = JHD1802(0x27)

# Hiển thị văn bản trên màn hình LCD
lcd.setCursor(0, 0)
lcd.write("Hello World")

lcd.setCursor(1, 0)
lcd.write("Grove LCD Test")
