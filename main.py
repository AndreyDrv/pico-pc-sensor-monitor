from LCD_1inch14 import *
from config import *
from font import *
from machine import Pin,SPI,PWM
import framebuf
import time
import urequests
import network
import utime
import math
import re

regex_CPU = re.compile('"CPU Package"\, "Children": \[\]\, "Min": "\d+.\d+ W", "Value": "(\d+.\d+) W')
regex_IntGPU = re.compile('"CPU Graphics", "Children": \[\], "Min": "\d+.\d+ W", "Value": "(\d+.\d+) W')
regex_GPU = re.compile('"GPU Power", "Children": \[\], "Min": "\d+.\d+ W", "Value": "(\d+.\d+) W')        
regex_CPUsage = re.compile('"CPU Total"\, "Children": \[\]\, "Min": "\d+.\d+ \%", "Value": "(\d+.\d+) \%')
regex_GPUsage = re.compile('"GPU Core"\, "Children": \[\]\, "Min": "\d+.\d+ \%", "Value": "(\d+.\d+) \%')

regex_GPUTemp = re.compile('"GPU Core"\, "Children": \[\]\, "Min": "\d+.\d+ °C", "Value": "(\d+.\d+) °C')
regex_CPUTemp = re.compile('"CPU Package"\, "Children": \[\]\, "Min": "\d+.\d+ °C", "Value": "(\d+.\d+) °C')

def do_connect():
    print('connection requested')
        
    wlan.active(True)    
    wlan.connect(AP_Name, AP_PW)
    while not wlan.isconnected():
        utime.sleep(1)
        print('waiting for connection...')
    print('connected with:', wlan.ifconfig())

def get_hw_values():
    try:
        hw_data = urequests.get("http://" + hw_data_server + "/data.json").text

        re_res = [ regex_CPUsage.search(hw_data), # 0 = CPU usage for calculations
                   regex_GPUsage.search(hw_data), # 1 = GPU usage for calculations
                   regex_CPU.search(hw_data),
                   regex_IntGPU.search(hw_data),
                   regex_GPU.search(hw_data),
                   regex_CPUTemp.search(hw_data),
                   regex_GPUTemp.search(hw_data) ]

        res = list(map(lambda re_value : math.ceil(float(re_value.group(1))) if re_value else 0, re_res))
        # add approx other devices consumption
        res += [ math.ceil(CONS[0] + (CONS[1]-CONS[0]) / 100 * max(res[0], res[1])) ]

        del(hw_data)
        return res[2:]
    except:
        print('Cannot connect to: ' + hw_data_server + '. Check OHM is alive and accessable')
        return [0]*6
        
def text_color(value):
    _value = float(value)
    
    threshold = [ CONS[0] + (CONS[1] - CONS[0])/2, CONS[1]]
    
    color = None
    if _value < threshold[0]:
        color = LCD.green
    elif _value >= threshold[0] and _value < threshold[1]:
        color = LCD.yellow
    else:
        color = LCD.red
    
    del(_value)
    return color

def print_text(lcd, text, loc_x, loc_y, value = None):
    if value:
        lcd.text(text,loc_x,loc_y,text_color(value))
    else:
        lcd.text(text,loc_x,loc_y,LCD.magenta)

def render_pixel(lcd, loc_x, loc_y, value = None):
    for i in range(10):
        lcd.hline(loc_x, loc_y+i, 10, LCD.magenta)

def print_big_text(lcd, text, loc_x, loc_y):
        
    for row in range(5):
        for char_index, text_char in enumerate(text):
            if text_char == 'w':
                num = 10
            else:
                num = int(text_char)
            for i, pixel in enumerate(numbers[num][row]):
                if pixel > 0:
                    render_pixel(lcd, loc_x + i*10 + char_index*50, loc_y + row*10)
    

if __name__=='__main__':
    pwm_duty_value = 32768
    
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(pwm_duty_value)#max 65535

    keyA = Pin(15,Pin.IN,Pin.PULL_UP)
    keyB = Pin(17,Pin.IN,Pin.PULL_UP)
        
    key_joy_up = Pin(2 ,Pin.IN,Pin.PULL_UP) 
    key_joy_center = Pin(3 ,Pin.IN,Pin.PULL_UP)
    key_joy_left = Pin(16 ,Pin.IN,Pin.PULL_UP)
    key_joy_down = Pin(18 ,Pin.IN,Pin.PULL_UP)
    key_joy_right = Pin(20 ,Pin.IN,Pin.PULL_UP)
    
    LCD = LCD_1inch14()
    LCD.fill(LCD.black)
 
    print_text(LCD, "Connecting to WIFI SSID:", 10, 10)
    print_text(LCD, str(AP_Name), 10, 25)
 
    LCD.show()
    
    wlan = network.WLAN(network.STA_IF)
    do_connect()
    
    time_key_frame = time.time()
    spent_money = 0
    view_mode = 0
            
    while(1):        
        if(keyA.value() == 0):
            new_pwm_duty_value = math.ceil(pwm_duty_value+10000)
            
            if new_pwm_duty_value>0 and new_pwm_duty_value<65535:
                pwm_duty_value = new_pwm_duty_value
                pwm.duty_u16(pwm_duty_value)#max 65535        
        
        if(keyB.value() == 0):
            new_pwm_duty_value = math.ceil(pwm_duty_value-10000)
            
            if new_pwm_duty_value>0 and new_pwm_duty_value<65535:
                pwm_duty_value = new_pwm_duty_value
                pwm.duty_u16(pwm_duty_value)#max 65535        
        
        LCD.fill(LCD.black)
        
        cpu, igpu, gpu, cpu_temp, gpu_temp, other = get_hw_values()
                
        print_text(LCD, "CPU:   " + str(cpu)   + " W", 10, 10, str(cpu))
        print_text(LCD, "iGPU:  " + str(igpu)  + " W", 10, 25, str(igpu))
        print_text(LCD, "GPU:   " + str(gpu)   + " W", 10, 40, str(gpu))
        print_text(LCD, "Other: " + str(other) + " W", 10, 55, str(other))
        
        print_text(LCD, "CPU Temp.: " + str(cpu_temp) + " C", 120, 10, cpu_temp)
        print_text(LCD, "GPU Temp.: " + str(gpu_temp) + " C", 120, 25, gpu_temp)
                        
        LCD.hline(10, 70, 220,LCD.magenta)            
         
        total = cpu + igpu + gpu + other        
        
        print_big_text(LCD, str(total)+'w', 25, 80)

        LCD.hline(120, 40, 110,LCD.magenta)
        LCD.vline(120, 40, 30,LCD.magenta)
        LCD.vline(230, 40, 30,LCD.magenta)

        total_consumption_kwh = total * 1 /1000
        cost_h = total_consumption_kwh * cost_kwh
        
        if time.time()-time_key_frame > 60:
            time_key_frame = time.time()
            spent_money += cost_h/60

        # mode 0
        #print_text(LCD, "kWh $: " + str(cost_kwh), 125, 45)
        #print_text(LCD, "$$/h   : " + str(round(cost_h,2)), 125, 55)        

        # mode 1
        print_text(LCD, "$$/h   : " + str(round(cost_h,2)), 125, 45)
        print_text(LCD, "Total $: " + str(round(spent_money,2)), 125, 55)
        #print_text(LCD, "Total $: " + str(5.37), 125, 55)        
        
        LCD.show()
            
    time.sleep(1)
    LCD.fill(0xFFFF)




