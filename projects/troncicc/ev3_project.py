"""Hello, I'm Michael Scott, regional manager of a mid range paper supply company. The goal of this game
is to help Michael avoid his duties and gain enough happy points so he can survive his encounter with
Jan. (need 500 happy points)

Timer:

Calibration!: Michael's office
Auto drive/beacon: Baler
2: Jim
3: Dwight
4: Kelly
5: Pam
6:

Kelly/Ryan:
   (if time > 12)
     You have become trapped by Kelly's endless conversation about how much she loves Ryan and wants to have his
     babies. Back away SLOWLY so she doesn't notice that you're gone.
     if speed > NUM:
     (success = happy + 100)
     (failure = happy - 100)
     (time goes forward quickly... soon, an hour is gone)

Toby:
     Oh no! You have been spotted by Toby! You can either run away quickly or attempt to kill him by
     picking him up and putting him in the baler. If you succeed, you will gain 500 happy points.
     But be careful... If you miss, you will be subject to a counseling session and you will die of boredom.
     (success = happy + 500)
     (failure = cause of death: boredom)

Dwight:
     sound (Dwight: 'MICHAEL!!!')
     You hear that?? That's the sound of Dwight being a baby again. Hide in your office motionless
     until he goes away. If he sees you, he will stare in your window until you come out.
     (success = happy + 100)
     (failure = happy - 100)
     (time goes forward quickly... soon, an hour is gone)

Jimbo, Jim, Jimothy:
     You spot Jim from across the room.

Creed:
    You are disgusted by his old man smell
    (failure = happy - 100)

Ryan:
    Ryan

Pam:
    You walk over to reception and do an impression that nobody understands.

Conference Room:



 """

import ev3dev.ev3 as ev3
import robot_controller as robo
import time
import mqtt_remote_method_calls as com


class MyDelegateEV3(object):
    """Most of the functions below are self explanatory."""
    def __init__(self):
        self.robot = robo.Snatch3r()
        self.mqtt_client = com.MqttClient()

    def arm_up(self):
        print("Arm up")
        self.robot.arm_up()

    def arm_down(self):
        print("Arm down")
        self.robot.arm_down()

    def right_turn(self, left_speed_entry, right_speed_entry):
        print("Turning right")
        self.robot.turn_right(1/2*left_speed_entry, 1/2*right_speed_entry)

    def left_turn(self, left_speed_entry, right_speed_entry):
        print("Turning left")
        self.robot.turn_left(1/2*left_speed_entry, 1/2*right_speed_entry)

    def forward_drive(self, left_speed_entry, right_speed_entry):
        print("Driving forward")
        self.robot.drive_forward(left_speed_entry, right_speed_entry)

    def backward_drive(self, left_speed_entry, right_speed_entry):
        print("Driving backward")
        self.robot.drive_back(left_speed_entry, right_speed_entry)

    def brake(self):
        print("Stopping")
        self.robot.stop()

    def drop_arm(self):
        self.robot.stop()
        print('Lowering arm')
        self.robot.arm_down()

    def calibrate(self):
        self.robot.stop()
        print('Calibrating... Please wait')
        ev3.Sound.speak('Please wait')
        self.robot.arm_calibration()

    def park(self):
        """This is the function that is called when press p or click on the button that says Pick up box?
        The robot will stop and pick up the cup using the arm. After this it will drive forward some inches
        and get the color that it is on.
        1. If the color is red, its a bomb. If you find a cup with a bomb under it, the robot will say Boom!
        Loud explosion sounds. The robot will then freeze for 20 seconds simulating that you died. If you wait,
        you can "respawn" and continue the game from where you left off. Also, a GUI will pop up saying that
        you're dead.
        2. If its green, its trash and the robot will be forced to drive automatically to 'throw it away'.
        To do this it will use the Pixi cam to find the pink cup (the trash can) and it will put the
        cup down and push it into the trash pile.
        3. If the robot lands on the gold circle, it means you found the treasure and the robot will dance and
        a GUI will pop up saying that you found the treasure!
        4. If the robot finds no color or a color that is not listed, it will put the cup back down and allow
        you to keep driving."""
        print("Parking")
        self.robot.stop()
        ev3.Sound.speak("What do we have here?").wait()
        self.robot.arm_up()
        self.robot.drive_inches(7, 200)
        color_sensor = ev3.ColorSensor()
        self.robot.color_sensor_get()
        if color_sensor.color == 3:
            print('Green color found')
            ev3.Sound.speak('Ew. Trash').wait()
            self.find_trash_can()
            self.robot.drive_inches(12, 200)
        elif color_sensor.color == 5:
            print('Red color found')
            ev3.Sound.speak('Its a bomb!').wait()
            time.sleep(2)
            ev3.Sound.speak('Boom... loud explosion sounds!').wait()
            self.mqtt_client.send_message('fiery_death')
            self.robot.stop()
            self.robot.shutdown()
            time.sleep(20)
        elif color_sensor.color == 4:
            print('We found the treasure!!!')
            ev3.Sound.speak('We found the treasure!').wait()
            self.robot.turn_degrees(360, 700)
            self.mqtt_client.send_message('treasure')
        else:
            print('There is nothing here silly...')
            ev3.Sound.speak('There is nothing here silly').wait()
            self.robot.arm_down()

    def find_trash_can(self):
        """This is the function that is called when the robot is ready to find the trash can to throw the box away."""
        print("--------------------------------------------")
        print(" Finding trash can...")
        print("--------------------------------------------")

        self.robot.pixy.mode = "SIG1"
        turn_speed = 100

        while self.robot.touch_sensor.is_pressed:

            x = self.robot.pixy.value(1)
            y = self.robot.pixy.value(2)
            if x == 0 and y == 0:
                self.robot.turn_left(200, 200)
            elif x > 170:
                self.robot.turn_right(turn_speed, turn_speed)
            elif x < 150:
                self.robot.turn_left(turn_speed, turn_speed)
            else:
                self.robot.stop()
                self.robot.arm_down()

            time.sleep(0.25)

        print("Done!")
        self.robot.stop()

    def shutdown(self):
        """This program makes all motors in the robot stop."""
        self.robot.shutdown()

    def loop_forever(self):
        btn = ev3.Button()
        while not btn.backspace:
            time.sleep(0.01)
        if self.mqtt_client:
            self.mqtt_client.close()
        self.robot.shutdown()


def main():
    my_delegate = MyDelegateEV3()
    mqtt_client = com.MqttClient(my_delegate)
    my_delegate.mqtt_client = mqtt_client
    mqtt_client.connect_to_pc()
    my_delegate.loop_forever()


main()
