"""Primary functions for pc end of project"""

import mqtt_remote_method_calls as com
import tkinter
from tkinter import ttk


class MyDelegatePC(object):
    """Helper class to receive and send data from the pc"""

    def __init__(self):
        """Data to be transmitted"""
        self.running = True
        self.gui_status = None
        self.gui = None

    # def status_update(self, status):
    #     print("STARTING STATUS UPDATE")
    #     self.gui_status.set(status)
    #     print("PC", status)
    #
    # def set_status(self, gui_status):
    #     print("setting gui status")
    #     self.gui_status = gui_status
    #     self.gui_status.set("TEST")
    def set_gui(self, gui):
        self.gui = gui

    def status_update(self, status):
        self.gui.status_str.set(status)


class GUI(object):
    """The tkinter windows and buttons for GUI"""

    def __init__(self, mqtt_client, my_delegate):
        self.mqtt_client = mqtt_client
        self.running = True
        self.root = None
        self.location = 0
        self.destination = 0
        self.destination_str = None
        self.confirm_label_str = None
        self.my_delegate = my_delegate
        self.status_str = None
        self.status = None

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
        self.mqtt_client.send_message("find_cargo")

    def wakeup_complete(self):
        self.mqtt_client.send_message("calibrate_and_continue")
        self.root.destroy()

    def reset_func(self):
        self.mqtt_client.send_message("reset")

    def set_destination(self, destination):
        self.destination = destination
        # self.destination_str.set("Destination {} Selected".format(destination))
        self.mqtt_client.send_message("set_destination", [destination])

    def set_location(self, location):
        self.location = location
        # self.location_str.set("Location {} Selected".format(location))
        self.mqtt_client.send_message("set_location", [location])

    def confirm_and_continue(self):
        if self.location == 0 or self.destination == 0:
            self.confirm_label_str.set("Location and/or Destination not set")
        elif self.location == self.destination:
            self.confirm_label_str.set("Invalid selection")
        else:
            self.confirm_label_str.set("Confirmed")
            self.mqtt_client.send_message("begin_retrieval")
            self.status_str.set("Beginning Retrieval")
            self.root.destroy()

    def status_update(self):
        # self.status_str.set(self.my_delegate.status)
        # self.my_delegate.set_status(self.status_str)
        self.my_delegate.set_gui(self)

    def quit_button(self):
        self.mqtt_client.send_message("quit")
        self.running = False
        self.root.destroy()

    def test_screen(self):
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
        reset = ttk.Button(main_frame, text="RESET")
        reset.grid(row=4, column=1)
        reset['command'] = lambda: self.reset_func()

        test = ttk.Button(main_frame, text="test")
        test.grid(row=10, column=1)
        test['command'] = lambda: self.test_func()

        self.root.mainloop()

    def wakeup_screen(self):
        self.root = tkinter.Tk()
        self.root.title = "Robot Wakeup"

        self.status_str = tkinter.StringVar()
        self.status_str.set('TEST0')
        self.status_update()

        main_frame = ttk.Frame(self.root, padding=40, relief='raised')
        main_frame.grid()

        calibrate = ttk.Button(main_frame, text="Calibrate")
        calibrate.grid(row=1, column=1)
        calibrate['command'] = lambda: self.wakeup_complete()

        quit_button = tkinter.ttk.Button(main_frame, text='QUIT')
        quit_button.grid(row=10, column=1)
        quit_button['command'] = lambda: self.quit_button()

        self.root.mainloop()

    def main_screen(self):
        self.root = tkinter.Tk()
        self.root.title = "Robot Wakeup"

        self.status_str = tkinter.StringVar()
        self.status_str.set('TEST1')

        main_frame = ttk.Frame(self.root, padding=20, relief='raised')
        main_frame.grid()

        loc = ttk.Label(main_frame, text="Select your Location")
        loc.grid(row=0, column=1)

        v1 = tkinter.IntVar()
        v2 = tkinter.IntVar()

        loc1 = ttk.Radiobutton(main_frame, text="Location 1", variable=v1, value=1)
        loc1.grid(row=1, column=1)
        loc1['command'] = lambda: self.set_location(1)
        loc2 = ttk.Radiobutton(main_frame, text="Location 2", variable=v1, value=2)
        loc2.grid(row=2, column=1)
        loc2['command'] = lambda: self.set_location(2)
        loc3 = ttk.Radiobutton(main_frame, text="Location 3", variable=v1, value=3)
        loc3.grid(row=3, column=1)
        loc3['command'] = lambda: self.set_location(3)
        loc4 = ttk.Radiobutton(main_frame, text="Location 4", variable=v1, value=4)
        loc4.grid(row=4, column=1)
        loc4['command'] = lambda: self.set_location(4)

        gap = ttk.Label(main_frame, text="     ")
        gap.grid(row=0, column=2)

        des = ttk.Label(main_frame, text="Select your Destination")
        des.grid(row=0, column=3)
        des1 = ttk.Radiobutton(main_frame, text="Destination 1", variable=v2, value=1)
        des1.grid(row=1, column=3)
        des1['command'] = lambda: self.set_destination(1)
        des2 = ttk.Radiobutton(main_frame, text="Destination 2", variable=v2, value=2)
        des2.grid(row=2, column=3)
        des2['command'] = lambda: self.set_destination(2)
        des3 = ttk.Radiobutton(main_frame, text="Destination 3", variable=v2, value=3)
        des3.grid(row=3, column=3)
        des3['command'] = lambda: self.set_destination(3)
        des4 = ttk.Radiobutton(main_frame, text="Destination 4", variable=v2, value=4)
        des4.grid(row=4, column=3)
        des4['command'] = lambda: self.set_destination(4)

        confirm = ttk.Button(main_frame, text="Confirm?")
        confirm.grid(row=6, column=2)
        confirm['command'] = lambda: self.confirm_and_continue()
        self.confirm_label_str = tkinter.StringVar()
        self.confirm_label_str.set(" ")
        confirm_label = ttk.Label(main_frame, textvariable=self.confirm_label_str)
        confirm_label.grid(row=7, column=2)

        quit_button = tkinter.ttk.Button(main_frame, text='QUIT')
        quit_button.grid(row=10, column=1)
        quit_button['command'] = lambda: self.quit_button()

        self.status_str = tkinter.StringVar()
        self.status_str.set("Beginning Retrieval")

        self.root.mainloop()

    def running_screen(self):
        self.root = tkinter.Tk()
        self.root.title = "Robot Running"

        self.status_str = tkinter.StringVar()
        self.status_str.set('TEST2')

        main_frame = ttk.Frame(self.root, padding=40, relief='raised')
        main_frame.grid()

        status = ttk.Label(main_frame, textvariable=self.status_str)
        status.grid(row=1, column=1)

        quit_button = tkinter.ttk.Button(main_frame, text='QUIT')
        quit_button.grid(row=10, column=1)
        quit_button['command'] = lambda: self.quit_button()

        self.root.mainloop()


def main():
    mydelegate = MyDelegatePC()
    mqtt_client = com.MqttClient(mydelegate)
    mqtt_client.connect_to_ev3()
    gui = GUI(mqtt_client, mydelegate)
    gui.status_update()

    # gui.test_screen()
    while True:
        gui.wakeup_screen()
        if not gui.running:
            break
        gui.main_screen()
        if not gui.running:
            break
        gui.running_screen()
        if not gui.running:
            break


main()
