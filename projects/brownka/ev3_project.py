"""
Primary functions for ev3 end of project
"""

import ev3dev.ev3 as ev3
import robot_controller as robo
import time
import mqtt_remote_method_calls as com
import warehouse_controller


class MyDelegateEv3(object):
    """Helper class to receive and send data from the pc"""

    def __init__(self, robot):
        """Data to be saved and/or transmitted"""
        self.running = True
        self.mqtt_cancel = True
        self.robot = robot
        self.warehouse = warehouse_controller.WarehouseController(robot, self)
        self.startup = True

    def cancel(self):
        ev3.Sound.speak("Cancel")
        self.mqtt_cancel = False
        self.robot.stop()

    def reset(self):
        self.mqtt_cancel = True

    def say_hello(self):
        ev3.Sound.speak("Do you know da wae?")

    def quit(self):
        self.running = False

    def follow_line_left(self):
        self.warehouse.destination = 1
        print("Destination: ", self.warehouse.destination)
        self.warehouse.follow_line_left()

    def follow_line_right(self):
        self.warehouse.destination = 1
        self.warehouse.follow_line_right()

    def follow_line_both(self):
        self.warehouse.follow_line_both()

    def calibrate_black(self):
        self.warehouse.calibrate_black_level()

    def calibrate_white(self):
        self.warehouse.calibrate_white_level()

    def calibrate_and_continue(self):
        # self.robot.arm_calibration()
        print("calibrated")
        self.startup = False


def main():
    robot = robo.Snatch3r()
    my_delegate = MyDelegateEv3(robot)
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()

    wakeup()

    while my_delegate.startup is True:
        time.sleep(.01)

    while my_delegate.running:

        time.sleep(.01)

    shutdown(robot)


def test_connection(mqtt_client):
    mqtt_client.send_message("print_stuff", ["some stuff"])


def wakeup():
    ev3.Sound.speak("Welcome, Captain. A new shipment has arrived. I must calibrate before we proceed.").wait()
    print("Program Start")


def shutdown(robot):
    robot.shutdown()


main()
