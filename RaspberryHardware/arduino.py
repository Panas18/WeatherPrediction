import serial
ser = serial.Serial("/dev/ttyACM0",9600)

def data():
    read_serial = ser.readline().decode("utf-8").rstrip()
    arduino_data = read_serial.split("-")
    try:
        dust = arduino_data[0]
        pressure = arduino_data[1]
    except IndexError:
        data()
    return dust, pressure
if __name__ == "__main__":
    while True:
        dust,pressure = data()
        print(dust, pressure)
