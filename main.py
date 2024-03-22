import ntptime
import onewire, ds18x20, time
from machine import Pin
import time
from machine import RTC
from lcd1602 import LCD

lcd=LCD()
lcd.clear() 

SensorPin = Pin(26, Pin.IN)
alert = Pin(15, Pin.OUT)
sensor = ds18x20.DS18X20(onewire.OneWire(SensorPin))
roms = sensor.scan()

#current_time = time.gmtime(time.time())
#print(current_time)

while True:
   current_time = time.localtime()
   hr = 0
   hr = current_time[3]
   todays_dt = str(current_time[0]) + "-" + str(current_time[1]) + "-"+ str(current_time[2])
   todays_dt += " " + str(hr) + ":"+str(current_time[4])
   sensor.convert_temp()
   lcd.clear()
   for rom in roms:
       temp_c = round(sensor.read_temp(rom),1)
       temp_f = round(temp_c * 9.0 / 5.0 + 32.0,2)
       if temp_c >= 37.8:
           warning_msg = "HIVE IS TOO HOT!!"
           warning_tmp= str(temp_f) + " F " + str(temp_c) + " C"
           lcd.write(0,0,warning_msg)
           lcd.write(0,1,warning_tmp)
           for i in range(10):
               alert.toggle()
               time.sleep(300)
       else:
           lcd.write(0,0,str(todays_dt))
           message = str(temp_f) + " F"
           lcd.write(0,1,message)
           message = " "+str(temp_c) + " C"
           col = 16 - len(message)
           lcd.write(col, 1, message)
           time.sleep(300)