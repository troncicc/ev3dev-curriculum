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


def main():
    happy = 0

    dc = DataContainer()
    mydelegate = MyDelegatePC()
    mqtt_client = com.MqttClient(mydelegate)
    mqtt_client.connect_to_ev3()
    dc.running = True

    root = tkinter.Tk()
    root.title("driving")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()
    left_speed = 400
    right_speed = 400

    forward_button = ttk.Button()
    forward_button['command'] = lambda: forward_callback(mqtt_client, left_speed, right_speed)
    root.bind('<Up>', lambda event: forward_callback(mqtt_client, left_speed, right_speed))

    down_button = ttk.Button()
    down_button['command'] = lambda: backward_callback(mqtt_client, left_speed, right_speed)
    root.bind('<Down>', lambda event: backward_callback(mqtt_client, left_speed, right_speed))

    left_button = ttk.Button()
    left_button['command'] = lambda: left_callback(mqtt_client, left_speed, right_speed)
    root.bind('<Left>', lambda event: left_callback(mqtt_client, left_speed, right_speed))

    right_button = ttk.Button()
    right_button['command'] = lambda: right_callback(mqtt_client, left_speed, right_speed)
    root.bind('<Right>', lambda event: right_callback(mqtt_client, left_speed, right_speed))

    stop_button = ttk.Button()
    stop_button['command'] = lambda: stop_callback(mqtt_client)
    root.bind('<space>', lambda event: stop_callback(mqtt_client))

    q_button = ttk.Button()
    q_button['command'] = (lambda: quit_program(mqtt_client, False))
    root.bind('<q>', lambda event: quit_program(mqtt_client, False))

    park_button = ttk.Button()
    park_button['command'] = lambda: park_callback(mqtt_client, happy)
    root.bind('<p>', lambda event: park_callback(mqtt_client, happy))

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


def park_callback(mqtt_client, happy):
    mqtt_client.send_message("park", happy)


def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


def dwight(happy):
    """This is the function for when you encounter the desk cluster of Jim and Dwight. Jim is at reception, but
    Dwight is ALWAYS there."""

    root = tkinter.Tk()

    main_frame = ttk.Frame(root, padding=20)
    main_frame.grid()

    photo = tkinter.PhotoImage(file='20090925_office_560x375.gif')

    dwight_button = ttk.Button(main_frame, image=photo)

    dwight_button.image = photo
    dwight_button.grid()
    dwight_button['command'] = lambda: print("Short description of Dwight.")

    label = ttk.Label(main_frame, text='Dwight Schrute')
    label.grid()

    next_page_button = ttk.Button(main_frame, text="Next")
    next_page_button.grid()
    next_page_button['command'] = lambda: close_window(root)

    root.mainloop()

    happy = happy + 100
    print('Michael Scott has gained 100 happy points! Your current happy score is ', happy)


def close_window(root):
    root.destroy()


main()
