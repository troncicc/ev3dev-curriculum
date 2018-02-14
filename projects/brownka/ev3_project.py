"""
Primary functions for ev3 end of project
"""

import ev3dev.ev3 as ev3
import robot_controller as robo
import time
import mqtt_remote_method_calls as com
import warehouse_controller

robot = robo.Snatch3r()


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
    warehouse = warehouse_controller.WarehouseController(robot, mqtt_client)

    wakeup()
    wait_for_command = True
    while wait_for_command is True:

        time.sleep(.01)

    shutdown()


def test_connection(client):
    client.send_message("print_stuff", ["some stuff"])


def wakeup():
    ev3.Sound.speak("Welcome, Captain. A new shipment has arrived. Would you like me to begin sorting?").wait()


def shutdown():
    ev3.Sound.speak("Goodbye")
    robot.stop()


main()
