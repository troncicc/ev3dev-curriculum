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
    say_hi.grid(row=2, column=1)
    say_hi['command'] = lambda: test_connection(mqtt_client)
    end = ttk.Button(main_frame, text="Quit")
    end.grid(row=2, column=1)
    end['command'] = lambda: send_end(mqtt_client)

    root.mainloop()


def test_connection(mqtt_client):
    mqtt_client.send_message("Say_hello", ["self"])


def send_end(mqtt_client):
    mqtt_client.send_message("quit", ["self"])


main()
