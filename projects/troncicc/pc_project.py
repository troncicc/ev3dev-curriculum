import mqtt_remote_method_calls as com
import tkinter
from tkinter import ttk


class DataContainer(object):

    def __init__(self):
        """"""
        self.running = True


class MyDelegatePC(object):
    """"""

    def __init__(self):
        """Data to be transmitted"""
        self.running = True

    def treasure(self):
        """This is the function that is called from the ev3 when you find one of the yellow circles.
        Yay treasure."""
        print('Hooray! You found the treasure!!!')
        window2 = tkinter.Toplevel()
        treasure_image = tkinter.PhotoImage(file='treasure.gif')
        treasure_button = ttk.Button(window2, image=treasure_image)

        treasure_button.image = treasure_image
        treasure_button.grid()
        treasure_button['command'] = lambda: print("You found the treasure and your journey"
                                                   " is complete.")

    def fiery_death(self):
        """This is the function that is called from the ev3 when you find one of the red circles.
        It's a bomb and you die."""
        print('Oh no, its a bom-...')
        print("You're dead")
        window = tkinter.Toplevel()
        dead_image = tkinter.PhotoImage(file='youredead.gif')

        dead_button = ttk.Button(window, image=dead_image)

        dead_button.image = dead_image
        dead_button.grid()
        dead_button['command'] = lambda: print("Goodbye... Better luck next time?...")


def main():
    dc = DataContainer()
    mydelegate = MyDelegatePC()
    mqtt_client = com.MqttClient(mydelegate)
    mqtt_client.connect_to_ev3()
    dc.running = True

    root = tkinter.Tk()
    root.title("THE HUNT")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()
    left_speed = 400
    right_speed = 400

    hunt_photo = tkinter.PhotoImage(file='The_Hunt (1).gif')
    hunt_button = ttk.Button(main_frame, image=hunt_photo)
    hunt_button.image = hunt_photo
    hunt_button.grid(row=1, column=4)
    hunt_button['command'] = lambda: print("Are you ready to join THE HUNT?")

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=3, column=2)
    forward_button['command'] = lambda: forward_callback(mqtt_client, left_speed, right_speed)
    root.bind('<Up>', lambda event: forward_callback(mqtt_client, left_speed, right_speed))

    down_button = ttk.Button(main_frame, text="Reverse")
    down_button.grid(row=5, column=2)
    down_button['command'] = lambda: backward_callback(mqtt_client, left_speed, right_speed)
    root.bind('<Down>', lambda event: backward_callback(mqtt_client, left_speed, right_speed))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=4, column=1)
    left_button['command'] = lambda: left_callback(mqtt_client, left_speed, right_speed)
    root.bind('<Left>', lambda event: left_callback(mqtt_client, left_speed, right_speed))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=4, column=3)
    right_button['command'] = lambda: right_callback(mqtt_client, left_speed, right_speed)
    root.bind('<Right>', lambda event: right_callback(mqtt_client, left_speed, right_speed))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=4, column=2)
    stop_button['command'] = lambda: stop_callback(mqtt_client)
    root.bind('<space>', lambda event: stop_callback(mqtt_client))

    quit_button = ttk.Button(main_frame, text="Quit")
    quit_button.grid(row=5, column=5)
    quit_button['command'] = (lambda: quit_program(mqtt_client, False))
    root.bind('<q>', lambda event: quit_program(mqtt_client, False))

    park_button = ttk.Button(main_frame, text="Pick up box?")
    park_button.grid(row=3, column=4)
    park_button['command'] = lambda: park_callback(mqtt_client)
    root.bind('<p>', lambda event: park_callback(mqtt_client))

    arm_down_button = ttk.Button()
    arm_down_button['command'] = lambda: arm_down_callback(mqtt_client)
    root.bind('<d>', lambda event: arm_down_callback(mqtt_client))

    cali_button = ttk.Button()
    cali_button['command'] = lambda: cali_callback(mqtt_client)
    root.bind('<c>', lambda event: cali_callback(mqtt_client))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=5)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))
    root.bind('<e>', lambda event: quit_program(mqtt_client, True))

    root.mainloop()


def forward_callback(mqtt_client, left_speed, right_speed):
    mqtt_client.send_message("forward_drive", [left_speed, right_speed])


def backward_callback(mqtt_client, left_speed, right_speed):
    mqtt_client.send_message("backward_drive", [left_speed, right_speed])


def left_callback(mqtt_client, left_speed, right_speed):
    mqtt_client.send_message("left_turn", [left_speed, right_speed])


def right_callback(mqtt_client, left_speed, right_speed):
    mqtt_client.send_message("right_turn", [left_speed, right_speed])


def stop_callback(mqtt_client):
    mqtt_client.send_message("brake")


def park_callback(mqtt_client):
    mqtt_client.send_message("park")


def arm_down_callback(mqtt_client):
    mqtt_client.send_message("drop_arm")


def cali_callback(mqtt_client):
    mqtt_client.send_message("calibrate")


def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


def close_window(root):
    root.destroy()


main()
