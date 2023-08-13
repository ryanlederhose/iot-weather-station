import network
import socket
from time import sleep
from machine import I2C, Pin
import machine
import time
from umqtt.simple import MQTTClient
from PiicoDev_BME280 import PiicoDev_BME280

# MACROS
TEMP = "Temperature"
PRESSURE = "Pressure"
LUX = "Lux"
ALT = "Altitude"
HUMIDITY = "Humidity"
MOISTURE = "Soil Moisture"
MAX_MOISTURE = 49756
MIN_MOISTURE = 19104
MOISTURE_GRAD = 100 / (MIN_MOISTURE - MAX_MOISTURE)
MOISTURE_INT = 100 - (MOISTURE_GRAD * MIN_MOISTURE)

# Registers
_veml6030Address = 0x10
_ALS_CONF = 0x00
_REG_ALS = 0x04

_DEFAULT_SETTINGS = b"\x00"

# WLAN ssid and password
ssid = "NetComm 6222"
password = "pstaxatfha"

'''
Connect to the WLAN
'''
def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print("Waiting for connection...")
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f"Connected on {ip}")
    return ip


'''
Get the lux readings from the light sensor
'''
def get_lux(i2c, addr, res):
    try:
        data = i2c.readfrom_mem(addr, _REG_ALS, 2)
    except:
        return float("NaN")
    return int.from_bytes(data, "little") * res

'''
Form a connection with a mqtt broker
Returns:
    mqtt client object
'''
def mqtt():
    mqtt_host = "192.168.20.20"
    mqtt_publish_topic = "testTopic"
    mqtt_client_id = "test"
    mqtt_client = MQTTClient(
        client_id=mqtt_client_id,
        server=mqtt_host,
        keepalive=10
    )
    try:
        mqtt_client.connect()
    except OSError as e:
        print(e)
        return None

    return mqtt_client

'''
Main loop
'''
def main():

    # Connect to WLAN
    try:
        connect()
    except KeyboardInterrupt:
        machine.reset()

    # Make I2C object
    i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400_000)

    # Light sensor parameters
    addr = _veml6030Address
    gain = 1
    res = 0.0576

    # Atmospheric sensor object
    sensor = PiicoDev_BME280(t_mode=2, p_mode=5, h_mode=1, iir=2, i2c=i2c)
    zeroAlt = sensor.altitude(pressure_sea_level=1013.25)

    i2c.writeto_mem(addr, _ALS_CONF, _DEFAULT_SETTINGS)

    adc = machine.ADC(28)

    client = mqtt() # Connect to MQTT broker
    while client == None:
        time.sleep(3)
        client = mqtt()


    paramsDict = {
        "Temperature": 0.00,
        "Pressure" : 0.00,
        "Altitude": 0.00,
        "Lux": 0.00,
        "Humidity": 0.00,
        "Soil Moisture": 0.00,
        "Node": "Outside"
    }

    while True:

        # Get soil moisture reading
        soilReading = adc.read_u16()
        soilMoisture = MOISTURE_GRAD * soilReading + MOISTURE_INT

        # Get lux value
        lightVal = get_lux(i2c, addr, res)

        # Get temperature, pressure and humidity
        tempC, presPa, humRH = sensor.values()
        altitude = sensor.altitude()
        pres_kPa = presPa / 1000

        paramsDict[TEMP] = tempC
        paramsDict[PRESSURE] = pres_kPa
        paramsDict[ALT] = altitude
        paramsDict[HUMIDITY] = humRH
        paramsDict[LUX] = lightVal
        paramsDict[MOISTURE] = soilMoisture

        # Publish to MQTT broker
        try:
            client = mqtt() # Connect to MQTT broker
            while client == None:
                time.sleep(3)
                client = mqtt()

            client.publish("testTopic", str(paramsDict))
            client.disconnect()
        except OSError as e:
            client.disconnect()
            print(f"Failed to publish message: {e}")
            pass

        sleep(5)


if __name__ == "__main__":
    main()
