""""""
import mqtt_remote_method_calls as com
import tkinter
from tkinter import ttk


def main():
    # happy = 0

    print('Does this print???')
    #
    # """The code below is the code that will show the opening window that says welcome to
    # Dunder Mifflin and has the office sign below it."""
    #
    # root = tkinter.Tk()
    #
    # main_frame = ttk.Frame(root, padding=20)
    # main_frame.grid()
    #
    # office_sign = tkinter.PhotoImage(file='the_office_logo_jpg.gif')
    #
    # office_sign_button = ttk.Button(main_frame, image=office_sign)
    #
    # office_sign_button.image = office_sign
    # office_sign_button.grid()
    # office_sign_button['command'] = lambda: print('Short description of Dunder Mifflin!')
    #
    # label = ttk.Label(main_frame, text='Welcome to Dunder Mifflin!')
    # label.grid()
    #
    # next_page_button = ttk.Button(main_frame, text="Next")
    # next_page_button.grid()
    # next_page_button['command'] = lambda: close_window(root)
    #
    # root.mainloop()
    #
    # happy = dwight(mqtt_client, happy)
    # happy = pj(mqtt_client, happy)
    # happy = darryl(mqtt_client, happy)
    # happy = cm(mqtt_client, happy)
    # happy = toby(mqtt_client, happy)
    # happy = kr(mqtt_client, happy)
    # happy = koa(mqtt_client, happy)
    # happy = ps(mqtt_client, happy)

    # mqtt_client = com.MqttClient()
    # mqtt_client.connect_to_ev3()
    #
    # root = tkinter.Tk()
    # root.title("MQTT Remote")
    #
    # left_speed_entry = 400
    # right_speed_entry = 400
    #
    # # '<Up>' key
    # forward_button = ttk.Button()
    # forward_button['command'] = lambda: forward_callback(mqtt_client, left_speed_entry, right_speed_entry)
    # root.bind('<Up>', lambda event: forward_callback(mqtt_client, left_speed_entry, right_speed_entry))
    #
    # # '<Left>' key
    # left_button = ttk.Button()
    # left_button['command'] = lambda: left_callback(mqtt_client, left_speed_entry, right_speed_entry)
    # root.bind('<Left>', lambda event: left_callback(mqtt_client, left_speed_entry, right_speed_entry))
    #
    # # '<space>' key (note, does not need left_speed_entry, right_speed_entry)
    # stop_button = ttk.Button()
    # stop_button['command'] = lambda: stop_callback(mqtt_client)
    # root.bind('<space>', lambda event: stop_callback(mqtt_client))
    #
    # # '<Right>' key
    # right_button = ttk.Button()
    # right_button['command'] = lambda: right_callback(mqtt_client, left_speed_entry, right_speed_entry)
    # root.bind('<Right>', lambda event: right_callback(mqtt_client, left_speed_entry, right_speed_entry))
    #
    # back_button = ttk.Button()
    # back_button.grid(row=4, column=1)
    # # back_button and '<Down>' key
    #
    # back_button['command'] = lambda: back_callback(mqtt_client, left_speed_entry, right_speed_entry)
    # root.bind('<Down>', lambda event: back_callback(mqtt_client, left_speed_entry, right_speed_entry))
    #
    # up_button = ttk.Button()
    # up_button['command'] = lambda: send_up(mqtt_client)
    # root.bind('<u>', lambda event: send_up(mqtt_client))
    #
    # down_button = ttk.Button()
    # down_button['command'] = lambda: send_down(mqtt_client)
    # root.bind('<j>', lambda event: send_down(mqtt_client))
    #
    # root.mainloop()

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=1, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=0, column=2)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=1, column=2)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)

    forward_button['command'] = lambda: forward_callback(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Up>', lambda event: forward_callback(mqtt_client, left_speed_entry, right_speed_entry))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    # left_button and '<Left>' key

    left_button['command'] = lambda: left_callback(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Left>', lambda event: left_callback(mqtt_client, left_speed_entry, right_speed_entry))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)

    stop_button['command'] = lambda: stop_callback(mqtt_client)
    root.bind('<space>', lambda event: stop_callback(mqtt_client))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    # right_button and '<Right>' key

    right_button['command'] = lambda: right_callback(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Right>', lambda event: right_callback(mqtt_client, left_speed_entry, right_speed_entry))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    # back_button and '<Down>' key

    back_button['command'] = lambda: back_callback(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Down>', lambda event: back_callback(mqtt_client, left_speed_entry, right_speed_entry))

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=6, column=0)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    root.mainloop()


def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")


# Drive button callbacks
def forward_callback(mqtt_client, left_speed_entry, right_speed_entry):
    print("button_forward")
    mqtt_client.send_message("drive_forward", [int(left_speed_entry.get()), int(right_speed_entry.get())])


def left_callback(mqtt_client, left_speed_entry, right_speed_entry):
    print("button_left")
    mqtt_client.send_message("turn_left", [int(left_speed_entry.get()), int(right_speed_entry.get())])


def stop_callback(mqtt_client):
    print("button_stop")
    mqtt_client.send_message("stop")


def right_callback(mqtt_client, left_speed_entry, right_speed_entry):
    print("button_right")
    mqtt_client.send_message("turn_right", [int(left_speed_entry.get()), int(right_speed_entry.get())])


def back_callback(mqtt_client, left_speed_entry, right_speed_entry):
    print("button_back")
    mqtt_client.send_message("drive_back", [int(left_speed_entry.get()), int(right_speed_entry.get())])


# Quit and Exit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


# def kr(mqtt_client, happy):
#     """This is the function for when you encounter the desk cluster of Kelly and Ryan(the annex)."""
#
#     root = tkinter.Tk()
#
#     main_frame = ttk.Frame(root, padding=20)
#     main_frame.grid()
#
#     kr_photo = tkinter.PhotoImage(file='Ry_Ke.gif')
#
#     kr_button = ttk.Button(main_frame, image=kr_photo)
#
#     kr_button.image = kr_photo
#     kr_button.grid()
#     kr_button['command'] = lambda: print("Short description of Kelly Kapoor and Ryan Howard.")
#
#     label = ttk.Label(main_frame, text='Ryan Howard and Kelly Kapoor')
#     label.grid()
#
#     next_page_button = ttk.Button(main_frame, text="Next")
#     next_page_button.grid()
#     next_page_button['command'] = lambda: close_window(root)
#
#     root.mainloop()
#
#     happy = happy + 100
#     print('Michael Scott has gained 100 happy points! Your current happy score is ', happy)
#     return happy
#
#
# def dwight(mqtt_client, happy):
#     """This is the function for when you encounter the desk cluster of Jim and Dwight. Jim is at reception, but
#     Dwight is ALWAYS there."""
#
#     root = tkinter.Tk()
#
#     main_frame = ttk.Frame(root, padding=20)
#     main_frame.grid()
#
#     photo = tkinter.PhotoImage(file='20090925_office_560x375.gif')
#
#     dwight_button = ttk.Button(main_frame, image=photo)
#
#     dwight_button.image = photo
#     dwight_button.grid()
#     dwight_button['command'] = lambda: print("Short description of Dwight.")
#
#     label = ttk.Label(main_frame, text='Dwight Schrute')
#     label.grid()
#
#     next_page_button = ttk.Button(main_frame, text="Next")
#     next_page_button.grid()
#     next_page_button['command'] = lambda: close_window(root)
#
#     root.mainloop()
#
#     happy = happy + 100
#     print('Michael Scott has gained 100 happy points! Your current happy score is ', happy)
#     return happy
#
#
# def pj(mqtt_client, happy):
#     """This is the function for when you encounter Pam's desk(recepetion). Jim will be there too."""
#
#     root = tkinter.Tk()
#
#     main_frame = ttk.Frame(root, padding=20)
#     main_frame.grid()
#
#     jim_and_pam = tkinter.PhotoImage(file='Jim_and_Pam.gif')
#
#     pj_button = ttk.Button(main_frame, image=jim_and_pam)
#
#     pj_button.image = jim_and_pam
#     pj_button.grid()
#     pj_button['command'] = lambda: print("Short description of Jim and Pam.")
#
#     label = ttk.Label(main_frame, text='Jim Halpert and Pam Beesley')
#     label.grid()
#
#     next_page_button = ttk.Button(main_frame, text="Next")
#     next_page_button.grid()
#     next_page_button['command'] = lambda: close_window(root)
#
#     root.mainloop()
#
#     happy = happy + 100
#     print('Michael Scott has gained 100 happy points! Your current happy score is ', happy)
#     return happy
#
#
# def darryl(mqtt_client, happy):
#     """This is the function for when you encounter Darryl's office."""
#
#     root = tkinter.Tk()
#
#     main_frame = ttk.Frame(root, padding=20)
#     main_frame.grid()
#
#     darryl_image = tkinter.PhotoImage(file='Darryl.gif')
#
#     darryl_button = ttk.Button(main_frame, image=darryl_image)
#
#     darryl_button.image = darryl_image
#     darryl_button.grid()
#     darryl_button['command'] = lambda: print("Short description of Darryl Philbin.")
#
#     label = ttk.Label(main_frame, text='Darryl Philbin')
#     label.grid()
#
#     next_page_button = ttk.Button(main_frame, text="Next")
#     next_page_button.grid()
#     next_page_button['command'] = lambda: close_window(root)
#
#     root.mainloop()
#
#     happy = happy + 100
#     print('Michael Scott has gained 100 happy points! Your current happy score is ', happy)
#     return happy
#
#
# def cm(mqtt_client, happy):
#     """This is the function for when you encounter the desk cluster of Creed and Meredith. It is not dependent on
#     the time of day."""
#
#     root = tkinter.Tk()
#
#     main_frame = ttk.Frame(root, padding=20)
#     main_frame.grid()
#
#     cm_image = tkinter.PhotoImage(file='Meredith_and_Creed.gif')
#
#     cm_button = ttk.Button(main_frame, image=cm_image)
#
#     cm_button.image = cm_image
#     cm_button.grid()
#     cm_button['command'] = lambda: print("Short description of Meredith Palmer and Creed Bratton.")
#
#     label = ttk.Label(main_frame, text='Meredith Palmer and Creed Bratton')
#     label.grid()
#
#     next_page_button = ttk.Button(main_frame, text="Next")
#     next_page_button.grid()
#     next_page_button['command'] = lambda: close_window(root)
#
#     root.mainloop()
#
#     happy = happy + 100
#     print('Michael Scott has gained 100 happy points! Your current happy score is ', happy)
#     return happy
#
#
# def toby(mqtt_client, happy):
#     """This is the function for when you encounter the desk of Toby."""
#     root = tkinter.Tk()
#
#     main_frame = ttk.Frame(root, padding=20)
#     main_frame.grid()
#
#     toby_image = tkinter.PhotoImage(file='Toby.gif')
#
#     toby_button = ttk.Button(main_frame, image=toby_image)
#
#     toby_button.image = toby_image
#     toby_button.grid()
#     toby_button['command'] = lambda: print("Short description of Toby Flenderson.")
#
#     label = ttk.Label(main_frame, text='Toby Flenderson')
#     label.grid()
#
#     next_page_button = ttk.Button(main_frame, text="Next")
#     next_page_button.grid()
#     next_page_button['command'] = lambda: close_window(root)
#
#     root.mainloop()
#
#     happy = happy + 100
#     print('Michael Scott has gained 100 happy points! Your current happy score is ', happy)
#     return happy
#
#
# def koa(mqtt_client, happy):
#     """This is the function for when you encounter the desk cluster of Kevin, Oscar, and Angela."""
#
#     root = tkinter.Tk()
#
#     main_frame = ttk.Frame(root, padding=20)
#     main_frame.grid()
#
#     koa_image = tkinter.PhotoImage(file='kra.gif')
#
#     koa_button = ttk.Button(main_frame, image=koa_image)
#
#     koa_button.image = koa_image
#     koa_button.grid()
#     koa_button['command'] = lambda: print("Short description of Kevin, Oscar, and Angela.")
#
#     label = ttk.Label(main_frame, text='Kevin, Oscar, and Angela')
#     label.grid()
#
#     next_page_button = ttk.Button(main_frame, text="Next")
#     next_page_button.grid()
#     next_page_button['command'] = lambda: close_window(root)
#
#     root.mainloop()
#
#     happy = happy + 100
#     print('Michael Scott has gained 100 happy points! Your current happy score is ', happy)
#     return happy
#
#
# def ps(mqtt_client, happy):
#     """This is the function for when you encounter the desk cluster of Phyllis and Stanley. On odd hours they
#     will be sleeping."""
#     root = tkinter.Tk()
#
#     main_frame = ttk.Frame(root, padding=20)
#     main_frame.grid()
#
#     ps_image = tkinter.PhotoImage(file='ps.gif')
#
#     ps_button = ttk.Button(main_frame, image=ps_image)
#
#     ps_button.image = ps_image
#     ps_button.grid()
#     ps_button['command'] = lambda: print("Short description of Phyllis and Stanley.")
#
#     label = ttk.Label(main_frame, text='Phyllis and Stanley')
#     label.grid()
#
#     next_page_button = ttk.Button(main_frame, text="Next")
#     next_page_button.grid()
#     next_page_button['command'] = lambda: close_window(root)
#
#     root.mainloop()
#
#     happy = happy + 100
#     print('Michael Scott has gained 100 happy points! Your current happy score is ', happy)
#     return happy
#
#
# # Arm command callbacks
#
#
# def next_page(mqtt_client):
#     print("page_forward")
#     mqtt_client.send_message("page_forward")
#
#
# def back_page(mqtt_client):
#     print("page_back")
#     mqtt_client.send_message("page_back")


def close_window(root):
    """"""
    root.destroy()


main()
