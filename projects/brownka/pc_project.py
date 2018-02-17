"""Primary functions for pc end of project"""

import mqtt_remote_method_calls as com
import tkinter
from tkinter import ttk


class MyDelegatePC(object):
    """Helper class to receive and send data from the pc"""

    def __init__(self):
        """Data to be transmitted"""
        self.running = True

    def print_stuff(self, stuff_to_print):
        print(stuff_to_print)


class GUI(object):
    """The tkinter windows and buttons for GUI"""

    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
        self.root = None

    def test_connection(self):
        self.mqtt_client.send_message("say_hello")

    def send_end(self):
        self.mqtt_client.send_message("quit")
        self.mqtt_client.close()
        exit()

    def follow_line_left(self):
        self.mqtt_client.send_message("follow_line_left")

    def follow_line_right(self):
        self.mqtt_client.send_message("follow_line_right")

    def follow_line_both(self):
        self.mqtt_client.send_message("follow_line_both")

    def cancel_func(self):
        self.mqtt_client.send_message("cancel")

    def test_func(self):
        self.mqtt_client.send_message("function", ["self"])

    def wakeup_complete(self):
        self.mqtt_client.send_message("calibrate_and_continue")
        self.root.destroy()

    def reset_func(self):
        self.mqtt_client.send_message("reset")

    def main_screen(self):
        self.root = tkinter.Tk()
        self.root.title = "Test Project"

        main_frame = ttk.Frame(self.root, padding=20, relief='raised')
        main_frame.grid()

        say_hi = ttk.Button(main_frame, text="Hello")
        say_hi.grid(row=1, column=1)
        say_hi['command'] = lambda: self.test_connection()
        end = ttk.Button(main_frame, text="QUIT")
        end.grid(row=2, column=1)
        end['command'] = lambda: self.send_end()
        line_left = ttk.Button(main_frame, text="line_left")
        line_left.grid(row=1, column=2)
        line_left['command'] = lambda: self.follow_line_left()
        line_right = ttk.Button(main_frame, text="line_right")
        line_right.grid(row=2, column=2)
        line_right['command'] = lambda: self.follow_line_right()
        line_both = ttk.Button(main_frame, text="line_both")
        line_both.grid(row=3, column=2)
        line_both['command'] = lambda: self.follow_line_both()
        black = ttk.Button(main_frame, text="Calibrate Black")
        black.grid(row=1, column=3)
        black['command'] = lambda: self.mqtt_client.send_message("calibrate_black")
        white = ttk.Button(main_frame, text="Calibrate White")
        white.grid(row=2, column=3)
        white['command'] = lambda: self.mqtt_client.send_message("calibrate_white")
        btn_cancel = ttk.Button(main_frame, text="CANCEL")
        btn_cancel.grid(row=3, column=1)
        btn_cancel['command'] = lambda: self.cancel_func()
        reset = ttk.Button(main_frame, text="CANCEL")
        reset.grid(row=4, column=1)
        reset['command'] = lambda: self.reset_func()

        test = ttk.Button(main_frame, text="test")
        test.grid(row=10, column=1)
        test['command'] = lambda: self.test_func()

        self.root.mainloop()

    def wakeup_screen(self):
        self.root = tkinter.Tk()
        self.root.title = "Robot Wakeup"

        main_frame = ttk.Frame(self.root, padding=40, relief='raised')
        main_frame.grid()

        calibrate = ttk.Button(main_frame, text="Calibrate and Continue")
        calibrate.grid(row=1, column=1)
        calibrate['command'] = lambda: self.wakeup_complete()

        self.root.mainloop()


def main():
    mydelegate = MyDelegatePC()
    mqtt_client = com.MqttClient(mydelegate)
    mqtt_client.connect_to_ev3()
    gui = GUI(mqtt_client)

    gui.wakeup_screen()

    gui.main_screen()


main()
