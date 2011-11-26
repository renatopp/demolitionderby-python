from client import Client
from sensor import Sensor
from controller import Controller
from simpledriver import SimpleDriver

client = Client()
driver = SimpleDriver()

client.loadParameters()
client.connect()

client.run(driver)