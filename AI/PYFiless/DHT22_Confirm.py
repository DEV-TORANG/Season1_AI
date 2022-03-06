import Adafruit_DHT as dht
import math
import datetime


def DHTvalues():
    wtime = datetime.datetime.now()
    humidity,temperature = dht.read_retry(dht.DHT22, 4)
    return round(temperature, 1), round(humidity, 1)
