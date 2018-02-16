"""
Primary functions for ev3 end of project
"""

import ev3dev.ev3 as ev3
import robot_controller as robo
import time
import mqtt_remote_method_calls as com
import warehouse_controller


class DataContainer(object):

    def __init__(self):
        """Add data to be saved"""


class MyDelegateEv3(object):
    """Helper class to receive and send data from the pc"""

    def __init__(self, dc, robot):
        """Data to be transmitted"""
        self.running = True
        self.dc = dc
        self.robot = robot
        self.warehouse = warehouse_controller.WarehouseController(robot, self)

    def say_hello(self):
        ev3.Sound.speak("Hiiii")

    def quit(self):
        self.dc.running = False


def main():
    robot = robo.Snatch3r()
    dc = DataContainer()
    my_delegate = MyDelegateEv3(dc, robot)
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()
    warehouse = warehouse_controller.WarehouseController(robot, mqtt_client)

    wakeup()
    dc.running = True
    while dc.running is True:

        time.sleep(.01)

    shutdown(robot)


def test_connection(client):
    client.send_message("print_stuff", ["some stuff"])


def wakeup():
    ev3.Sound.speak("Hello").wait()


def shutdown(robot):
    ev3.Sound.speak("Goodbye")
    robot.stop()
    exit()


main()
