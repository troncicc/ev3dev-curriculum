"""
Primary functions for ev3 end of project
"""

import ev3dev.ev3 as ev3
import robot_controller as robo
import time
import mqtt_remote_method_calls as com
import warehouse_controller


class MyDelegateEv3(object):
    """Class that performs most of the robot's functions with relation to the PC"""

    def __init__(self, robot):
        """Data to be saved and/or transmitted"""
        self.robot = robot
        self.warehouse = warehouse_controller.WarehouseController(robot, self)
        self.running = True
        self.startup = True
        self.main = True
        self.following = False
        self.seeking = False
        self.carrying = False
        self.status = "Start"

    def cancel(self):
        pass

    def reset(self):
        self.running = True
        self.startup = True
        self.main = True
        self.following = False
        self.seeking = False
        self.carrying = False
        self.status = "Start"

    def say_hello(self):
        ev3.Sound.speak("Doo yoo know de way?")

    def quit(self):
        self.startup = False
        self.main = False
        self.running = False
        self.robot.stop()
        self.robot.shutdown()
        quit()

    def follow_line_left(self):
        print("Destination: ", self.warehouse.cargo_location)
        self.following = True
        while self.following:
            self.warehouse.follow_line_left()
            if self.warehouse.robot.current_color == 4:
                self.following = False
            time.sleep(.01)
        self.robot.stop()

    def follow_line_right(self):
        self.warehouse.cargo_location = 1
        print("Destination: ", self.warehouse.cargo_location)
        self.following = True
        while self.following:
            self.warehouse.follow_line_right()
            if self.warehouse.robot.current_color == 4:
                self.following = False
            time.sleep(.01)
        self.robot.stop()

    def follow_line_both(self):
        print("Destination: ", self.warehouse.cargo_location)
        self.following = True
        while self.following:
            self.warehouse.follow_line_both()
            if self.warehouse.robot.current_color == 3:
                self.following = False
            time.sleep(.01)
        self.robot.stop()

    def calibrate_black(self):
        self.warehouse.calibrate_black_level()

    def calibrate_white(self):
        self.warehouse.calibrate_white_level()

    def calibrate_and_continue(self):
        self.robot.arm_calibration()
        print("calibrated")
        self.startup = False

    def find_cargo(self):
        # print("search")
        self.seeking = True
        while self.seeking:
            self.warehouse.find_cargo()
            if self.warehouse.cargo_found is True:
                self.seeking = False
            time.sleep(.1)
        self.robot.stop()
        self.carrying = True
        ev3.Sound.beep()

    def set_location(self, location):
        self.warehouse.cargo_location = location
        print("Cargo location is: ", self.warehouse.cargo_location)

    def set_destination(self, destination):
        self.warehouse.cargo_destination = destination
        print("Cargo destination is: ", self.warehouse.cargo_destination)

    def begin_retrieval(self):
        self.main = False
        self.status = ("Moving to location ", self.warehouse.cargo_location)
        ev3.Sound.speak("Moving cargo from location {} to destination {}".format(self.warehouse.cargo_location,
                                                                                 self.warehouse.cargo_destination)).wait()
        self.follow_line_both()
        self.status = "Searching for cargo"
        self.find_cargo()
        self.status = ("Cargo retrieved. Moving to destination ", self.warehouse.cargo_destination)
        ev3.Sound.speak("I have the cargo. Moving to the destination point.")
        self.follow_line_both()
        self.status = "Destination reached. Placing cargo"
        self.robot.arm_down()
        self.robot.drive_inches(-4, 200)
        self.status = "Objective complete"
        ev3.Sound.speak("Objective complete, Captain.")
        self.running = False

    def check_status(self):
        pass


class Delegate2(object):
    """Delegate that cancels ongoing functions in the primary delegate and ignore all other commands"""

    def __init__(self, robot, my_delegate, mqtt_client):
        """Data to be saved and/or transmitted"""
        self.robot = robot
        self.my_delegate = my_delegate
        self.mqtt_client = mqtt_client

    def cancel(self):
        self.my_delegate.following = False
        self.my_delegate.seeking = False
        self.robot.stop()
        ev3.Sound.speak("Cancel")

    def reset(self):
        pass

    def say_hello(self):
        pass

    def quit(self):
        self.my_delegate.startup = False
        self.my_delegate.main = False
        self.my_delegate.running = False
        self.robot.stop()
        self.robot.shutdown()
        quit()

    def follow_line_left(self):
        pass

    def follow_line_right(self):
        pass

    def follow_line_both(self):
        pass

    def calibrate_black(self):
        pass

    def calibrate_white(self):
        pass

    def calibrate_and_continue(self):
        pass

    def find_cargo(self):
        pass

    def set_location(self, location):
        pass

    def set_destination(self, destination):
        pass

    def begin_retrieval(self):
        pass

    def check_status(self):
        if self.my_delegate.carrying:
            self.my_delegate.status = "Moving cargo to destination"
        elif self.my_delegate.following:
            self.my_delegate.status = "Moving to cargo location"
        elif self.my_delegate.seeking:
            self.my_delegate.status = "Searching for cargo"


def main():
    robot = robo.Snatch3r()
    my_delegate = MyDelegateEv3(robot)
    mqtt_client = com.MqttClient(my_delegate)
    my_delegate2 = Delegate2(robot, my_delegate, mqtt_client)
    mqtt_client2 = com.MqttClient(my_delegate2)
    mqtt_client.connect_to_pc()
    mqtt_client2.connect_to_pc()

    while True:
        wakeup()

        while my_delegate.startup:
            time.sleep(.01)

        print("robot done with startup")

        while my_delegate.main:

            time.sleep(.01)

        print("robot done with main")

        while my_delegate.running:
            my_delegate2.check_status()
            print("EV3", my_delegate.status)
            mqtt_client2.send_message("status_update", [my_delegate.status])

            time.sleep(.01)

        print("robot done with running")

        robot.shutdown()
        time.sleep(5)
        my_delegate.reset()


def wakeup():
    ev3.Sound.speak("Welcome, Captain. A new shipment has arrived. I must calibrate before we proceed.").wait()
    print("Program Start")


main()
