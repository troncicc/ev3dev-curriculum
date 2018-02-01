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

    print("Start Snatch3r")

    def drive_inches(self, inches_target, speed_dps):
        print("--------------------------------------------")
        print("  Encoder Driving 1")
        print("--------------------------------------------")
        ev3.Sound.speak("Drive using encoders").wait()

        # Connect two large motors on output ports B and C
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

        # Check that the motors are actually connected
        assert left_motor.connected
        assert right_motor.connected
        print('motors ready')

        position = inches_target * 90
        print('calculations done')

        left_motor.run_to_rel_pos(position_sp=position, speed_sp=speed_dps, stop_action='brake')
        right_motor.run_to_rel_pos(position_sp=position, speed_sp=speed_dps, stop_action='brake')
        print('motors running')
        left_motor.wait_while(ev3.Motor.STATE_RUNNING)

        ev3.Sound.beep()
        print('motors stopped')

        print("Goodbye!")
        ev3.Sound.speak("Goodbye").wait()

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        print("--------------------------------------------")
        print("  Turn degrees")
        print("--------------------------------------------")
        ev3.Sound.speak("Turn degrees").wait()

        # Connect two large motors on output ports B and C
        left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

        # Check that the motors are actually connected
        assert left_motor.connected
        assert right_motor.connected
        print('motors ready')

        position = degrees_to_turn * math.pi/180
        # position = inches_target * 90
        print('calculations done')

        left_motor.run_to_rel_pos(position_sp=position, speed_sp=-turn_speed_sp, stop_action='brake')
        right_motor.run_to_rel_pos(position_sp=position, speed_sp=turn_speed_sp, stop_action='brake')
        print('motors running')
        left_motor.wait_while(ev3.Motor.STATE_RUNNING)

        ev3.Sound.beep()
        print('motors stopped')

        print("Goodbye!")
        ev3.Sound.speak("Goodbye").wait()
