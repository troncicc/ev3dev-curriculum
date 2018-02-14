"""A library of functions designed to work in tandem with the robot_controller
 for the ev3 project. Functions are more sophisticated pieces of the puzzle,
 and many of their base components come from the robot_controller"""

import robot_controller as robo
import ev3dev.ev3 as ev3
import time


class WarehouseController(object):

    def __init__(self, robot, mqtt_client):
        """Define recurring variables"""

        self.white_level = 60
        self.black_level = 40
        self.robot = robot
        self.mqtt_client = mqtt_client

    def calibrate_white_level(self):
        print("Calibrate the white light level")
        self.robot.color_sensor_get()
        self.white_level = self.robot.reflected_light_intensity

        print("New white level is {}.".format(self.white_level))

    def calibrate_black_level(self):
        print("Calibrate the black light level")
        self.robot.color_sensor_get()
        self.black_level = self.robot.reflected_light_intensity

    def follow_line_right(self):
        following = True

        while following is True:
            self.robot.color_sensor_get()

            if self.robot.touch_sensor.is_pressed:
                following = False

            if self.robot.reflected_light_intensity >= self.black_level + 30:
                self.robot.turn_left(400, 200)
            else:
                self.robot.drive_forward(400, 400)
            time.sleep(.01)

    def follow_line_left(self):
        following = True

        while following is True:
            self.robot.color_sensor_get()

            if self.robot.touch_sensor.is_pressed:
                following = False

            if self.robot.reflected_light_intensity >= self.black_level + 30:
                self.robot.turn_right(400, 200)
            else:
                self.robot.drive_forward(400, 400)
            time.sleep(.01)

    def follow_line_both(self):
        following = True

        while following is True:
            self.robot.color_sensor_get()

            if self.robot.touch_sensor.is_pressed:
                following = False

            if self.robot.reflected_light_intensity >= self.black_level + 30:
                self.robot.turn_right(400, 200)
            else:
                self.robot.turn_left(200, 400)
            time.sleep(.01)
