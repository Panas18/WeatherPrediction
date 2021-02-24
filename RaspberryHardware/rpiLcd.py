import Adafruit_CharLCD as LCD
from time import sleep
lcd_rs=5
lcd_en=11
lcd_d4=6
lcd_d5=13
lcd_d6=19
lcd_d7=26
lcd_columns=16
lcd_rows=2
lcd=LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,lcd_columns, lcd_rows)

def displayLcd(message):
    message = str(message)
    lcd.clear()
    lcd.message(message)

def clearLcd(time):
    lcd.clear()
    sleep(time)

