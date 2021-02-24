
import Adafruit_DHT

def dthData():
    humidity, temperature= Adafruit_DHT.read_retry(11,21)
    return humidity, temperature

if __name__ =="__main__":
    while True:
        humidity, temperature = dthData()
        print(f"Humidity = {humidity}, Temperature = {temperature}")
