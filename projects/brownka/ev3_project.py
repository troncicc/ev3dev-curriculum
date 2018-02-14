"""
Primary functions for ev3 end of project
"""

import ev3dev.ev3 as ev3
import robot_controller as robo
import time
import mqtt_remote_method_calls as com
import warehouse_controller

robot = robo.Snatch3r()
warehouse = warehouse_controller.WarehouseController


class DataContainer(object):

    def __init__(self):
        """Add data to be saved"""


dc = DataContainer()


class MyDelegateEv3(object):
    """Helper class to receive and send data from the pc"""

    def __init__(self):
        """Data to be transmitted"""
        self.running = True

    def say_hello(self):
        ev3.Sound.speak("Hiiii")

    def quit(self):
        dc.running = False


def main():
    mqtt_client = com.MqttClient(MyDelegateEv3)
    mqtt_client.connect_to_pc()

    wakeup()
    dc.running = True

    shutdown()


def test_connection(client):
    client.send_message("print_stuff", ["some stuff"])


def wakeup():
    ev3.Sound.speak("Hello").wait()


def shutdown():
    ev3.Sound.speak("Goodbye")
    robot.stop()


main()
