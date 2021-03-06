import serial
ser = serial.Serial("/dev/ttyACM0",9600)

def data():
    read_serial = ser.readline().decode("utf-8").rstrip()
    arduino_data = read_serial.split("-")
    dust = None
    pressure=None
    uv_intensity=None
    param_list = [dust, pressure, uv_intensity]
    for i in range(len(arduino_data)):
        param_list[i] = arduino_data[i]
   # print(len(arduino_data))
    #dust = arduino_data[0]
    #pressure = arduino_data[1]
    #uv_intensity = arduino_data[2]
    return param_list
  
    
    #return dust, pressure, uv_intensity
#    print(arduino_data)

if __name__ == "__main__":
    while True:
        # dust,pressure = data()
        # print(dust, pressure, uv_intensity)
        param_list =data()
        for val in param_list:
            print(val)
