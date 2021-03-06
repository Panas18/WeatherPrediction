#import rpiLcd as lcdScreen
import dth11 as dth
from time import sleep
import sys
import datetime
import time
import arduino
import rpiLcd

line_number=None
time_to_write_file = 5
counter =0

try:
    with open("data.csv", "r") as f:
        lines_in_file = len(f.readlines())
        line_number= lines_in_file

except FileNotFoundError:
    with open("data.csv", "w") as f:
        f.write("SN,Date,Time,Temperature,Humidity,Dust_density,Pressure,uv_intensity" )
        line_number=1
       
def data_total():
    humidity, temperature = dth.dthData()
    lcd_1 = f"humidity:{humidity}\ntemperature:{temperature}"
    rpiLcd.displayLcd(lcd_1)
    #param_list=arduino.data()
    #dustDensity = None
    #pressure=None
    #uv_intensity=None
    #final_list = [dustDensity, pressure, uv_intensity]
    #for i in range(len(param_list)):
     #   final_list[i] = param_list[i]
    dustDensity, pressure, uv_intensity = arduino.data()
    lcd_2 = f"Dust:{dustDensity}\nPressure:{pressure}"
    lcd_3 = f"uv:{uv_intensity}"
    rpiLcd.displayLcd(lcd_2)
    sleep(1)
    rpiLcd.displayLcd(lcd_3)
    #print(dustDensity)
    #print(pressure)
    #print(uv_intensity)
    return humidity, temperature, dustDensity, pressure, uv_intensity

if __name__ =="__main__":
    while True:
        try:
            tic = 0
            tic = time.perf_counter()
            time_data = str(datetime.datetime.now())
            date_clock = time_data.split(" ")[0]
            time_clock = (time_data.split(" ")[1]).split(".")[0]
            #dust, pressure, uv_intensity = arduino.data()
            #humidity, temperature = dth.dthData()
            humidity, temperature, dust, pressure, uv_intensity = data_total()
            print(f"Temperature = {temperature} , Humidity= {humidity}, Dust Density= {dust}, Pressure = {pressure}, Uv={uv_intensity}")
            #lcd_message = f"Temperatue={temperature}\n Humidity={humidity}"
            data=f"{line_number},{date_clock},{time_clock},{temperature},{humidity},{dust},{pressure},{uv_intensity}"
            if (counter >= time_to_write_file):
                with open("data.csv", "a") as f:
                    f.write("\n")
                    f.write(data)
                    print(f"Written in file after {int(counter)} seconds\n")
                    line_number+=1 
                    counter = 0 
            #rpiLcd.displayLcd(lcd_message)     
        # time.sleep(0.44)
            toc = time.perf_counter()
            print(f"{toc-tic} seconds\n")
            counter +=toc-tic

            
        except KeyboardInterrupt:
            print("\nUser Interrupt")
            sys.exit()
