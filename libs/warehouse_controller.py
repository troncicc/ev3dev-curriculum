"""A library of functions designed to work in tandem with the robot_controller
 for the ev3 project. Functions are more sophisticated pieces of the puzzle,
 and many of their base components come from the robot_controller"""

import robot_controller as robo
import ev3dev.ev3 as ev3
import time

robot = robo.Snatch3r()


class WarehouseController(object):

    def __init__(self):
        """Define recurring variables"""

        self.white_level = 60
        self.black_level = 40

    def follow_line_right(self):
        following = True

        while following is True:
            robot.color_sensor_get()

            if robot.touch_sensor.is_pressed:
                following = False

            if robot.reflected_light_intensity >= self.black_level + 30:
                robot.turn_left(400, 200)
            else:
                robot.drive_forward(400, 400)
            time.sleep(.01)

    def follow_line_left(self):
        following = True

        while following is True:
            robot.color_sensor_get()

            if robot.touch_sensor.is_pressed:
                following = False

            if robot.reflected_light_intensity >= self.black_level + 30:
                robot.turn_right(400, 200)
            else:
                robot.drive_forward(400, 400)
            time.sleep(.01)

    def follow_line_both(self):
        following = True

        while following is True:
            robot.color_sensor_get()

            if robot.touch_sensor.is_pressed:
                following = False

            if robot.reflected_light_intensity >= self.black_level + 30:
                robot.turn_right(400, 200)
            else:
                robot.turn_left(200, 400)
            time.sleep(.01)
