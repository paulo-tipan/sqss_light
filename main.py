wifiName = 'Smart_Bro_C4A8F'
wifiPass = 'smartbro'

# Client Database
database = 'harbest'
# SQSS O - Oxygen Only
name = 'client_sqss_L'

# Sensor Number
sid = 1
# Read Key
rk = 111

o2xx = 0

# Imports
import machine
import time

import urequests as requests

# SCD 30
from SCD30 import SCD30
i2c = machine.SoftI2C(machine.Pin(32), machine.Pin(33))
scd30 = SCD30(i2c, 0x61)

# Light Sensor
import veml7700
i2c_l = machine.I2C(0)
i2c_l = machine.I2C(1, scl=machine.Pin(22), sda=machine.Pin(21), freq=10000)

veml = veml7700.VEML7700(address=0x10, i2c=i2c_l, it=100, gain=1/8)

# LCD
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
lcd_I2C_ADDR = 0x27
totalRows = 4
totalColumns = 20
lcd_i2c = machine.SoftI2C(scl=Pin(26), sda=Pin(27), freq=10000)
lcd = I2cLcd(lcd_i2c, lcd_I2C_ADDR, totalRows, totalColumns)
lcd.clear()
lcd.putstr("Connecting to WiFi")

# Network Settings
import network
do_connect(wifiName,wifiPass)
lcd.clear()
lcd.putstr("Connected to: " + wifiName + " ")

time.sleep(3)


def loop():
    start_time = time.time()

    lux = veml.read_lux()

    while scd30.get_status_ready() != 1:
        time.sleep_ms(200)
    scd30_data = scd30.read_measurement()
    co2x, temp, humi = scd30_data[0], scd30_data[1], scd30_data[2]
    temp_string = str(temp)[:4] + " degC - " +  str(humi)[:5] + " %%"
    
    html = send_data(database, name, sid, temp, humi, co2x, o2xx, lux, rk)
    no_par = html
    
    res = requests.get(f'{no_par}')
    print(res.text)
    
    text = res.text
    find_date = text.find('Date : ')
    time_show = text[find_date+7:find_date+26]
    
    lcd.clear()
    lcd.putstr(time_show + " " + temp_string + "CO2: " + str(co2x)[:8] + " ppm  " + " O2: " + str(o2xx) + " % vol")
    
    print("=========================")
    
    run_time = time.time() - start_time
    print("Run Time: ", run_time)
    time.sleep(300-run_time)


if __name__ == "__main__":
    while True:
        try:
            wlan = network.WLAN(network.STA_IF)
            if not wlan.isconnected():
                print("not connected to WiFi...")
                do_connect(wifiName,wifiPass,staticIP)
                #Wait after connecting to WiFi
                time.sleep(300)
            loop()
        except Exception as e:
            text = str(e)
            print("There was a problem")
            print(text)
            lcd.clear()
            lcd.putstr("No WiFi, wait for 5 minutes to reconnect")
            time.sleep(300)