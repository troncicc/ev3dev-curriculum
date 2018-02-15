"""A library of functions designed to work in tandem with the robot_controller
 for the ev3 project. Functions are more sophisticated pieces of the puzzle,
 and many of their base components come from the robot_controller"""

import ev3dev.ev3 as ev3
import time


class WarehouseController(object):

    def __init__(self, robot, mqtt_cancel):
        """Define recurring variables"""

        self.white_level = 60
        self.black_level = 40
        self.robot = robot
        self.mqtt_cancel = mqtt_cancel
        self.color_names = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]

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
        """Follow the right edge of a line"""
        following = True

        while following is True:
            self.robot.color_sensor_get()

            if self.robot.touch_sensor.is_pressed:
                following = False
                self.robot.stop()

            elif self.mqtt_cancel is False:
                following = False
                self.robot.stop()

            if self.robot.reflected_light_intensity >= self.black_level + 30:
                self.robot.turn_left(400, 200)
            else:
                self.robot.drive_forward(400, 400)
            time.sleep(.01)

    def follow_line_left(self):
        """Follow the left edge of a line"""
        following = True

        while following is True:
            self.robot.color_sensor_get()

            if self.robot.touch_sensor.is_pressed:
                following = False
                self.robot.stop()

            elif self.mqtt_cancel is False:
                following = False
                self.robot.stop()

            if self.robot.reflected_light_intensity >= self.black_level + 30:
                self.robot.turn_right(400, 200)
            else:
                self.robot.drive_forward(400, 400)
            time.sleep(.01)

    def follow_line_both(self):
        """Follow a line regardless of the edge"""
        following = True

        while following is True:
            self.robot.color_sensor_get()

            if self.robot.touch_sensor.is_pressed:
                following = False
                self.robot.stop()

            elif self.mqtt_cancel is False:
                following = False
                self.robot.stop()

            if self.robot.reflected_light_intensity >= self.black_level + 30:
                self.robot.turn_right(400, 200)
            else:
                self.robot.turn_left(200, 400)
            time.sleep(.01)

    def turn_at(self):
        """Causes robot to turn 90deg a particular direction when at a junction based on the colour"""

        current_color = self.robot.current_color
        if current_color == self.color_names[3]:
            self.robot.turn_degrees(90, 300)

        elif current_color == self.color_names[4]:
            self.robot.turn_degrees(-90, 300)
