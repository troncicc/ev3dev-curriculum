"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    def __init__(self):
        # Connect two large motors on output ports B and C
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

        # Check that the motors are actually connected
        assert self.left_motor.connected
        assert self.right_motor.connected

        # Connect and assert connection of medium motor to output port A
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        assert self.arm_motor.connected

        # Define and check sensors are connected
        self.touch_sensor = ev3.TouchSensor()
        assert self.touch_sensor

        # Define and check connection of Color Sensor
        self.color_sensor = ev3.ColorSensor()
        assert self.color_sensor

        # Define recurring variables
        self.current_color = 0

        self.running = True

    def drive_inches(self, inches_target, speed_dps):
        """A simple program that causes the robot to drive in a straight line given a speed and a distance"""

        # Check that the motors are actually connected
        assert self.left_motor.connected
        assert self.right_motor.connected

        position = inches_target * 90

        self.left_motor.run_to_rel_pos(position_sp=position, speed_sp=speed_dps, stop_action='brake')
        self.right_motor.run_to_rel_pos(position_sp=position, speed_sp=speed_dps, stop_action='brake')
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        """Causes the robot to turn given a speed and angle"""

        # Check that the motors are actually connected
        assert self.left_motor.connected
        assert self.right_motor.connected

        position = (degrees_to_turn*(math.pi/180)*3)*90

        self.left_motor.run_to_rel_pos(position_sp=(position*-1), speed_sp=turn_speed_sp, stop_action='brake')
        self.right_motor.run_to_rel_pos(position_sp=position, speed_sp=turn_speed_sp, stop_action='brake')
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm_calibration(self):
        assert self.touch_sensor
        assert self.arm_motor

        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action='brake')
        ev3.Sound.beep().wait()

        arm_revolutions_for_full_range = 14.2 * 360
        self.arm_motor.run_to_rel_pos(position_sp=arm_revolutions_for_full_range * -1)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

        self.arm_motor.position = 0

    def arm_up(self):
        assert self.arm_motor
        assert self.touch_sensor

        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action='brake')
        ev3.Sound.beep().wait()

    def arm_down(self):
        assert self.arm_motor

        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=900)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes running
        ev3.Sound.beep().wait()

    def button_forward(self, left_motor_speed, right_motor_speed):
        self.left_motor.run_forever(speed_sp=left_motor_speed)
        self.right_motor.run_forever(speed_sp=right_motor_speed)

    def button_back(self, left_motor_speed, right_motor_speed):
        self.left_motor.run_forever(speed_sp=-left_motor_speed)
        self.right_motor.run_forever(speed_sp=-right_motor_speed)

    def button_left(self, left_motor_speed, right_motor_speed):
        self.left_motor.run_forever(speed_sp=-left_motor_speed)
        self.right_motor.run_forever(speed_sp=right_motor_speed)

    def button_right(self, left_motor_speed, right_motor_speed):
        self.left_motor.run_forever(speed_sp=left_motor_speed)
        self.right_motor.run_forever(speed_sp=-right_motor_speed)

    def button_stop(self):
        self.left_motor.stop(stop_action="brake")
        self.right_motor.stop(stop_action="brake")

    def brake(self):
        self.left_motor.stop(stop_action="brake")
        self.right_motor.stop(stop_action="brake")

    def color_sensor(self):
        self.current_color = self.color_sensor.color()

    def shutdown(self):
        self.right_motor.stop(stop_action='coast')
        self.left_motor.stop(stop_action='coast')
        self.arm_motor.stop(stop_action='coast')

        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)

        print("Goodbye")
        ev3.Sound.speak("Goodbye").wait()
        self.running = False

    def loop_forever(self):
        # This is a convenience method that I don't really recommend for most programs other than m5.
        #   This method is only useful if the only input to the robot is coming via mqtt.
        #   MQTT messages will still call methods, but no other input or output happens.
        # This method is given here since the concept might be confusing.
        self.running = True
        while self.running:
            time.sleep(0.1)  # Do nothing (except receive MQTT messages) until an MQTT message calls shutdown.

