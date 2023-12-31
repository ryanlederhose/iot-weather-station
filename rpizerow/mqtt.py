import paho.mqtt.client as mqtt
import time
import socket
import json
import datetime
import pandas as pd
import csv
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport, sevensegment
import RPi.GPIO as GPIO
import sys
import signal
from htmlstring import get_html_string
import threading
import copy

SERVER = "localhost"
USER = "root"
PASSWORD = "Bluescope@01"
DATABASE = ""

PRESSURE_LIST = [0] * 720
TEMPERATURE_LIST = [0] * 720
HUMIDITY_LIST = [0] * 720
LUX_LIST = [0] * 720
TIME_LIST = [0] * 720
MOISTURE_LIST = [0] * 720
LIST_ARRAY = [PRESSURE_LIST, TEMPERATURE_LIST, HUMIDITY_LIST, 
        LUX_LIST, TIME_LIST, MOISTURE_LIST]
LIST_STRINGS = ['Pressure', 'Temperature', 'Humidity', 'Lux', 'Time', 'Soil Moisture']
timeNow = datetime.datetime.now().strftime("%H-%M-%S")
pressureNow = 0
humidityNow = 0
temperatureNow = 0
luxNow = 0
soilMoistureNow = 0

messageCount = 0

BUTTON_GPIO = 4
SPI_USED_ISR = False

displayList = ["TIME", "PRESSURE", "HUMIDITY", "SOIL MOISTURE", "TEMPERATURE", "LIGHT"]
displayIndex = 0
measurementList = [timeNow, pressureNow, humidityNow, soilMoistureNow, temperatureNow, luxNow]

html = get_html_string()

trig = 27
echo = 17

def ultrasonic_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(27, GPIO.OUT)
    GPIO.setup(17, GPIO.IN)

def get_distance():
    GPIO.output(trig, False)
    time.sleep(0.1)
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)
    while GPIO.input(echo) == 0:
        pulse_start = time.time()
    while GPIO.input(echo) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17000
    if pulse_duration >= 0.01746:
        return 0
    elif distance > 300 or distance == 0:
        return 0
    distance = round(distance, 3)
    return distance


def socket_connection(addr):
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('listening on', addr)
    return s

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected OK, Returned code=", rc)
    else:
        print("Bad connection, Returned code=", rc)

def on_subscribe(client, userdata, mid, granted_qos):
    print(str(userdata))

def on_message(client, userdata, msg):
    global LUX_LIST
    global TIME_LIST
    global TEMPERATURE_LIST
    global HUMIDITY_LIST
    global PRESSURE_LIST
    global MOISTURE_LIST

    global timeNow
    global pressureNow
    global humidityNow
    global soilMoistureNow
    global temperatureNow
    global luxNow

    global messageCount

    print(f"Message received [{msg.topic}]: {msg.payload}")
    
    message = str(msg.payload)[2:-1]
    message = message.replace("'", "\"")
    message = json.loads(message)
    message["Time"] = datetime.datetime.now().strftime("%c")

    timeNow = datetime.datetime.now().strftime("%c")
    pressureNow = message['Pressure']
    humidityNow = message['Humidity']
    soilMoistureNow = message['Soil Moisture']
    temperatureNow = message['Temperature']
    luxNow = message['Lux']

    measurementList.clear()
    measurementList.append(datetime.datetime.now().strftime("%H-%M-%S"))
    measurementList.append(pressureNow)
    measurementList.append(humidityNow)
    measurementList.append(soilMoistureNow)
    measurementList.append(temperatureNow)
    measurementList.append(luxNow)

    # seg.text = str(temperatureNow)

    if messageCount == 24:
        for i in range(len(LIST_ARRAY)):
            LIST_ARRAY[i].pop(0)
            if LIST_STRINGS[i] != 'Time':
                LIST_ARRAY[i].append(message[LIST_STRINGS[i]])
            else:
                LIST_ARRAY[i].append(datetime.datetime.now().strftime("%c"))
        messageCount = 0
    else:
        messageCount += 1

def http_server():
    global s
    
    datalist = []
    index = 1

    intervalDict = {
            '30 mins': 15,
            '2 hours': 60,
            '12 hours': 360,
            '24 hours': 720,
            'None': 1
            }

    plottingDict = {
            'Temperature': TEMPERATURE_LIST,
            'Humidity': HUMIDITY_LIST,
            'Lux': LUX_LIST,
            'Pressure': PRESSURE_LIST,
            'Moisture': MOISTURE_LIST,
            'None': [0 for i in range(720)]
            }


    plotting = 'None'
    node = 'None'
    interval = 'None'
    
    f = open("/home/ryan/state.txt", "r+")
    txt = f.readline()
    while txt != "":
        txt = txt.strip()
        if txt.find('Node') != -1:
            j = txt.find(':')
            node = txt[j + 2:]
        elif txt.find('Plotting') != -1:
            j = txt.find(':')
            plotting = txt[j + 2:]
        elif txt.find('Interval') != -1:
            j = txt.find(':')
            interval = txt[j + 2:]
        txt = f.readline()
    f.close()

    datalist = plottingDict.get(plotting)
    index = intervalDict.get(interval)

    while True:
        try:

            newRequest = 0

            c1, addr = s.accept()

            request = c1.recv(1024)
            request = str(request)
            print(request)

            newRequest = request.find('req=on')

            if request.find('req=on') == 8:
                newRequest = 1
            elif request.find('inside=on') == 8:
                if node != 'Inside':
                    node = 'Inside'
                else:
                    node = 'None'
            elif request.find('outside=on') == 8:
                if node != 'Outside':
                    node = 'Outside'
                else:
                    node = 'None'
            elif request.find('lux=on') == 8:
                datalist = LUX_LIST
                if plotting != 'Lux':
                    plotting = 'Lux'
                else:
                    plotting = 'None'
            elif request.find('pressure=on') == 8:
                datalist = PRESSURE_LIST
                if plotting != 'Pressure':
                    plotting = 'Pressure'
                else:
                    plotting = 'None'
            elif request.find('temperature=on') == 8:
                datalist = TEMPERATURE_LIST
                if plotting != 'Temperature':
                    plotting = 'Temperature'
                else:
                    plotting = 'None'
            elif request.find('moisture=on') == 8:
                datalist = MOISTURE_LIST
                if plotting != 'Moisture':
                    plotting = 'Moisture'
                else:
                    plotting = 'None'
            elif request.find('humidity=on') == 8:
                datalist = HUMIDITY_LIST
                if plotting != 'Humidity':
                    plotting = 'Humidity'
                else:
                    plotting = 'None'
            elif request.find('30mins=on') == 8:
                index = 15
                if interval != '30 mins':
                    interval = '30 mins'
                else:
                    interval = 'None'
            elif request.find('2hours=on') == 8:
                index = 60
                if interval != '2 hours':
                    interval = '2 hours'
                else:
                    interval = 'None'
            elif request.find('12hours=on') == 8:
                index = 360
                if interval != '12 hours':
                    interval = '12 hours'
                else:
                    interval = 'None'
            elif request.find('24hours=on') == 8:
                index = 720
                if interval != '24 hours':
                    interval = '24 hours'
                else:
                    interval = 'None'
            
            TIME_LISTS_REV = copy.deepcopy(TIME_LIST)
            datalists_rev = copy.deepcopy(datalist)
            
            if plotting == 'None' or node == 'None' or interval == 'None':
                datalists_rev = [0 for i in range(720)]
            
            f = open("/home/ryan/state.txt", "r+")
            f.seek(0)
            f.truncate()
            f.writelines(['Node: ' + node + '\n',
                'Plotting: ' + plotting + '\n',
                'Interval: ' + interval + '\n'])
            f.close()

            c1.send('HTTP\1.0 200 OK\r\nCache-Control: no-cache\r\nContent-type: text/html\r\n\r\n'.encode('utf-8'))
            response = html % (timeNow, temperatureNow, humidityNow, pressureNow, soilMoistureNow, luxNow, timeNow,
                    (TIME_LISTS_REV[720 - index:]), 
                    (datalists_rev[720 - index:]))
            c1.send(response.encode('utf-8'))
            c1.close()
        except OSError as e:
            c1.close()
            print('connection closed')        
        except KeyboardInterrupt as e:
            c1.close()

def gpio_isr(channel):
    global displayIndex
    global device
    global displayList

    displayIndex += 1
    if displayIndex == len(displayList):
        displayIndex = 0
    
    show_message_vp(device, str(displayList[displayIndex]))
    

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def show_message_vp(device, msg, delay=0.1):
    global SPI_USED_ISR

    width = device.width
    padding = " " * width
    msg = padding + msg + padding
    n = len(msg)

    virtual = viewport(device, width=n, height=8)
    sevensegment(virtual).text = msg
    SPI_USED_ISR = True
    for i in reversed(list(range(n - width))):
        virtual.set_position((i, 0))
        time.sleep(delay)
    SPI_USED_ISR = False

def main():
    global device
    global s
    global displayIndex
    global displayList
    global SPI_USED_ISR

    ultrasonic_gpio()

    time.sleep(10)

    client = mqtt.Client(client_id='test_rpi', transport='tcp')
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message

    client.connect(host="192.168.20.13", port=1883, keepalive=10)

    time.sleep(4)
    print('Client Connection Status: ', client.is_connected())

    client.subscribe(topic='testTopic')
    client.loop_start()

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket_connection(addr)

    prevTime = time.time()

    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=1)
    seg = sevensegment(device)
        
    serverThread = threading.Thread(target=http_server)
    serverThread.start()

    while True:

        distance = get_distance()
        print(distance)
        if distance <= 10 and distance > 0:
            show_message_vp(device, str(displayList[displayIndex]))

        measurementList.pop(0)
        measurementList.insert(0, datetime.datetime.now().strftime("%H-%M-%S"))
        try:
            if SPI_USED_ISR == False:
                seg.text = str(measurementList[displayIndex])
        except:
            print(e)
            pass
        time.sleep(0.1)

if __name__=='__main__':
    main()




