"""Primary functions for pc end of project"""

import mqtt_remote_method_calls as com
import tkinter
from tkinter import ttk


class DataContainer(object):

    def __init__(self):
        """Add data to be saved"""


class MyDelegatePC(object):
    """Helper class to receive and send data from the pc"""

    def __init__(self):
        """Data to be transmitted"""
        self.running = True

    def print_stuff(self, stuff_to_print):
        print(stuff_to_print)


def main():
    dc = DataContainer()
    mydelegate = MyDelegatePC()
    mqtt_client = com.MqttClient(mydelegate)
    mqtt_client.connect_to_ev3()
    dc.running = True

    root = tkinter.Tk()
    root.title = "Test Project"

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    say_hi = ttk.Button(main_frame, text="Hello")
    say_hi.grid(row=1, column=1)
    say_hi['command'] = lambda: test_connection(mqtt_client)
    end = ttk.Button(main_frame, text="QUIT")
    end.grid(row=2, column=1)
    end['command'] = lambda: send_end(mqtt_client)
    line_left = ttk.Button(main_frame, text="line_left")
    line_left.grid(row=1, column=2)
    line_left['command'] = lambda: follow_line_left(mqtt_client)
    line_right = ttk.Button(main_frame, text="line_right")
    line_right.grid(row=2, column=2)
    line_right['command'] = lambda: follow_line_right(mqtt_client)
    line_both = ttk.Button(main_frame, text="line_both")
    line_both.grid(row=3, column=2)
    line_both['command'] = lambda: follow_line_both(mqtt_client)
    btn_cancel = ttk.Button(main_frame, text="CANCEL")
    btn_cancel.grid(row=3, column=1)
    btn_cancel['command'] = lambda: cancel_func(mqtt_client)

    test = ttk.Button(main_frame, text="test")
    test.grid(row=4, column=1)
    test['command'] = lambda: test_func(mqtt_client)

    root.mainloop()


def test_connection(mqtt_client):
    mqtt_client.send_message("say_hello")


def send_end(mqtt_client):
    mqtt_client.send_message("quit")
    mqtt_client.close()
    exit()


def follow_line_left(mqtt_client):
    mqtt_client.send_message("follow_line_left")


def follow_line_right(mqtt_client):
    mqtt_client.send_message("follow_line_right")


def follow_line_both(mqtt_client):
    mqtt_client.send_message("follow_line_both")


def cancel_func(mqtt_client):
    mqtt_client.send_message("cancel")


def test_func(mqtt_client):
    mqtt_client.send_message("function", ["self"])


main()
