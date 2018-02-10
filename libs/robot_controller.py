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
        self.color_sensor = ev3.ColorSensor()
        assert self.color_sensor
        self.ir_sensor = ev3.InfraredSensor()
        assert self.ir_sensor
        self.remote_control = ev3.RemoteControl()
        # don't assert remote_control since it is external from the robot
        self.beacon_seeker = ev3.BeaconSeeker(channel=1)
        assert self.beacon_seeker
        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        assert self.pixy

        # Define recurring variables
        self.current_color = 0
        self.reflected_light_intensity = 0

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

    def stop(self):
        self.left_motor.stop(stop_action="brake")
        self.right_motor.stop(stop_action="brake")
        self.arm_motor.stop(stop_action="brake")

    def color_sensor_get(self):
        self.current_color = self.color_sensor.color
        self.reflected_light_intensity = self.color_sensor.reflected_light_intensity

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

    def seek_beacon(self):

        forward_speed = 300
        turn_speed = 100

        while not self.touch_sensor.is_pressed:
            # The touch sensor can be used to abort the attempt (sometimes handy during testing)

            # DONE: 3. Use the beacon_seeker object to get the current heading and distance.
            current_heading = self.beacon_seeker.heading  # use the beacon_seeker heading
            current_distance = self.beacon_seeker.distance  # use the beacon_seeker distance
            if current_distance == -128:
                # If the IR Remote is not found, robot spins in place to find beacon
                print("IR Remote not found. Distance is -128")
                self.button_right(turn_speed, turn_speed)

            elif current_distance == 100:
                # If the IR Remote is not found, robot spins in place to find beacon
                print("IR Remote not found. Distance is 100")
                self.button_right(turn_speed, turn_speed)
            else:
                if math.fabs(current_heading) < 2:
                    # Close enough of a heading to move forward
                    if current_distance == 1:
                        print("Beacon found!")
                        self.stop()
                        self.drive_inches(4, 100)
                        return True
                    else:
                        print("On the right heading. Distance: ", current_distance)
                        self.button_forward(forward_speed, forward_speed)

                elif math.fabs(current_heading) < 10:
                    if current_heading < 0:
                        print("Adjusting heading:", current_heading)
                        self.button_left(turn_speed, turn_speed)
                    else:
                        print("Adjusting heading:", current_heading)
                        self.button_right(turn_speed, turn_speed)

                else:
                    self.button_right(turn_speed, turn_speed)
                    print("Heading too far off. Heading: ", current_heading)

            time.sleep(0.05)

        # The touch_sensor was pressed to abort the attempt if this code runs.
        print("Abandon ship!")
        self.stop()
        return False



