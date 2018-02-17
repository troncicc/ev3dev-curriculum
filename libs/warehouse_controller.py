"""A library of functions designed to work in tandem with the robot_controller
 for the ev3 project. Functions are more sophisticated pieces of the puzzle,
 and many of their base components come from the robot_controller"""

# import ev3dev.ev3 as ev3
import time


class WarehouseController(object):

    def __init__(self, robot, my_delegate):
        """Define recurring variables"""

        self.white_level = 60
        self.black_level = 40
        self.robot = robot
        self.my_delegate = my_delegate
        self.color_names = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]
        self.destination = 0
        """
        Destination definitions:
        0 = Home
        1 = Back Left
        2 = Back Right
        3 = Front Left
        4 = Front Right
        """

    def calibrate_white_level(self):
        print("Calibrate the white light level")
        self.robot.color_sensor_get()
        self.white_level = self.robot.reflected_light_intensity

        print("New white level is {}.".format(self.white_level))

    def calibrate_black_level(self):
        print("Calibrate the black light level")
        self.robot.color_sensor_get()
        self.black_level = self.robot.reflected_light_intensity

        print("New black level is {}.".format(self.black_level))

    def follow_line_right(self):
        """Follow the right edge of a line"""
        following = True

        while following is True:
            self.robot.color_sensor_get()

            self.on_color()

            if self.robot.touch_sensor.is_pressed:
                following = False
                self.robot.stop()

            elif self.my_delegate.mqtt_cancel is False:
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

            self.on_color()

            if self.robot.touch_sensor.is_pressed:
                following = False
                self.robot.stop()

            elif self.my_delegate.mqtt_cancel is False:
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

            self.on_color()

            if self.robot.touch_sensor.is_pressed:
                following = False
                self.robot.stop()

            elif self.my_delegate.mqtt_cancel is False:
                following = False
                self.robot.stop()

            if self.robot.reflected_light_intensity >= self.black_level + 30:
                self.robot.turn_right(400, 200)
            else:
                self.robot.turn_left(200, 400)
            time.sleep(.01)

    def on_color(self):
        """Causes robot to turn 90deg a particular direction when at a junction based on the colour"""

        current_color = self.robot.current_color
        print('Current colour: ', self.color_names[current_color])
        if current_color == 5:
            if self.destination == 1:
                print("turn left")
                self.robot.turn_degrees(90, 300)

            elif self.destination == 2:
                print("turn right")
                self.robot.turn_degrees(-90, 300)

            elif self.destination == 3:
                print("drive")
                self.robot.drive_inches(2, 400)

            elif self.destination == 4:
                print("drive")
                self.robot.drive_inches(2, 400)

        elif current_color == 2:
            if self.destination == 3:
                print("turn left")
                self.robot.turn_degrees(90, 300)

            elif self.destination == 4:
                print("turn right")
                self.robot.turn_degrees(-90, 300)

            elif self.destination == 1:
                print("drive")
                self.robot.drive_inches(2, 400)

            elif self.destination == 2:
                print("drive")
                self.robot.drive_inches(2, 400)

        elif current_color == 4:
            self.robot.stop()
            while True:
                print("on yellow")
                time.sleep(1)
