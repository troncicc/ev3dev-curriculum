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
        self.pixy = self.robot.pixy
        self.pixy.mode = "SIG1"
        self.color_names = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]
        self.cargo_location = 0
        self.cargo_destination = 0
        """
        Destination/Location definitions:
        0 = Home
        1 = Back Left
        2 = Back Right
        3 = Front Left
        4 = Front Right
        """
        self.carrying = False
        self.cargo_found = False

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

        self.robot.color_sensor_get()
        self.on_color()

        if self.robot.reflected_light_intensity >= self.black_level + 30:
            self.robot.turn_left(400, 200)
        else:
            self.robot.drive_forward(400, 400)

    def follow_line_left(self):
        """Follow the left edge of a line"""
        self.robot.color_sensor_get()

        self.on_color()

        if self.robot.reflected_light_intensity >= self.black_level + 30:
            self.robot.turn_right(400, 200)
        else:
            self.robot.drive_forward(400, 400)

    def follow_line_both(self):
        """Follow a line regardless of the edge"""
        self.robot.color_sensor_get()

        self.on_color()

        if self.robot.reflected_light_intensity >= self.black_level + 30:
            self.robot.turn_right(400, 200)
        else:
            self.robot.turn_left(200, 400)

    def on_color(self):
        """Causes robot to turn 90deg a particular direction when at a junction based on the colour"""

        current_color = self.robot.current_color
        print('Current colour: ', self.color_names[current_color])
        if current_color == 5:
            self.color_is_red()

        elif current_color == 2:
            self.color_is_blue()

        elif current_color == 4:
            self.color_is_yellow()

    def color_is_red(self):
        if self.cargo_location == 1:
            print("turn left")
            self.robot.turn_degrees(90, 200)
            print("inch forward")
            self.robot.drive_inches(1, 300)

        elif self.cargo_location == 2:
            print("turn right")
            self.robot.turn_degrees(-90, 300)
            print("inch forward")
            self.robot.drive_inches(1, 300)

        elif self.cargo_location == 3:
            print("drive")
            self.robot.drive_inches(2, 300)

        elif self.cargo_location == 4:
            print("drive")
            self.robot.drive_inches(2, 300)

    def color_is_blue(self):
        if self.cargo_location == 3:
            print("turn left")
            self.robot.turn_degrees(90, 300)
            print("inch forward")
            self.robot.drive_inches(1, 300)

        elif self.cargo_location == 4:
            print("turn right")
            self.robot.turn_degrees(-90, 300)
            print("inch forward")
            self.robot.drive_inches(1, 300)

        elif self.cargo_location == 1:
            print("drive")
            self.robot.drive_inches(2, 400)

        elif self.cargo_location == 2:
            print("drive")
            self.robot.drive_inches(2, 400)

    def color_is_yellow(self):
        print("on yellow")
        self.robot.stop()

    def find_cargo(self):
        """Searches for cargo. If robot does not see cargo, it turns in place until it is found"""
        turn_speed = 100

        x = self.pixy.value(1)
        y = self.pixy.value(2)
        print("(X, Y) = ({}, {})".format(x, y))

        if x == 0 and y == 0:   # Does not see cargo
            self.robot.turn_left(turn_speed, turn_speed)
        elif x > 170:
            self.robot.turn_right(turn_speed, turn_speed)
        elif x < 150:
            self.robot.turn_left(turn_speed, turn_speed)
        else:
            self.robot.stop()
            self.robot.drive_inches(3, 100)
            self.robot.arm_up()
            self.cargo_found = True

