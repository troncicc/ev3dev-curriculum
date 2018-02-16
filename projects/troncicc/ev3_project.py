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
import time

import robot_controller as robo

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


def main():
    """This is the main function that will be used to call the other functions."""
    happy = 0

    root = tkinter.Tk()

    main_frame = ttk.Frame(root, padding=20)
    main_frame.grid()

    office_sign = tkinter.PhotoImage(file='the_office_logo_jpg.gif')

    office_sign_button = ttk.Button(main_frame, image=office_sign)

    office_sign_button.image = office_sign
    office_sign_button.grid()
    office_sign_button['command'] = lambda: print('Short description of Dunder Mifflin!')

    label = ttk.Label(main_frame, text='Welcome to Dunder Mifflin!')
    label.grid()

    next_page_button = ttk.Button(main_frame, text="Next")
    next_page_button.grid()
    next_page_button['command'] = lambda: close_window(root)

    root.mainloop()

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    happy = dwight(mqtt_client, happy)
    happy = pj(mqtt_client, happy)
    happy = darryl(mqtt_client, happy)
    happy = cm(mqtt_client, happy)
    happy = toby(mqtt_client, happy)
    happy = kr(mqtt_client, happy)
    happy = koa(mqtt_client, happy)
    happy = ps(mqtt_client, happy)

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    left_speed_entry = 100
    right_speed_entry = 100

    # '<Up>' key
    forward_button = ttk.Button()
    forward_button['command'] = lambda: forward_callback(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Up>', lambda event: forward_callback(mqtt_client, left_speed_entry, right_speed_entry))

    # '<Left>' key
    left_button = ttk.Button()
    left_button['command'] = lambda: left_callback(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Left>', lambda event: left_callback(mqtt_client, left_speed_entry, right_speed_entry))

    # '<space>' key (note, does not need left_speed_entry, right_speed_entry)
    stop_button = ttk.Button()
    stop_button['command'] = lambda: stop_callback(mqtt_client)
    root.bind('<space>', lambda event: stop_callback(mqtt_client))

    # '<Right>' key
    right_button = ttk.Button()
    right_button['command'] = lambda: right_callback(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Right>', lambda event: right_callback(mqtt_client, left_speed_entry, right_speed_entry))

    back_button = ttk.Button()
    back_button.grid(row=4, column=1)
    # back_button and '<Down>' key

    back_button['command'] = lambda: back_callback(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Down>', lambda event: back_callback(mqtt_client, left_speed_entry, right_speed_entry))

    up_button = ttk.Button()
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button()
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))


def kr(mqtt_client, happy):
    """This is the function for when you encounter the desk cluster of Kelly and Ryan(the annex)."""

    root = tkinter.Tk()

    main_frame = ttk.Frame(root, padding=20)
    main_frame.grid()

    kr_photo = tkinter.PhotoImage(file='Ry_Ke.gif')

    kr_button = ttk.Button(main_frame, image=kr_photo)

    kr_button.image = kr_photo
    kr_button.grid()
    kr_button['command'] = lambda: print("Short description of Kelly Kapoor and Ryan Howard.")

    label = ttk.Label(main_frame, text='Ryan Howard and Kelly Kapoor')
    label.grid()

    next_page_button = ttk.Button(main_frame, text="Next")
    next_page_button.grid()
    next_page_button['command'] = lambda: close_window(root)

    root.mainloop()

    happy = happy + 100
    print('Michael Scott has gained 100 happy points! Your current happy score is ', happy)
    return happy


def dwight(mqtt_client, happy):
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
    return happy


def pj(mqtt_client, happy):
    """This is the function for when you encounter Pam's desk(recepetion). Jim will be there too."""

    root = tkinter.Tk()

    main_frame = ttk.Frame(root, padding=20)
    main_frame.grid()

    jim_and_pam = tkinter.PhotoImage(file='Jim_and_Pam.gif')

    pj_button = ttk.Button(main_frame, image=jim_and_pam)

    pj_button.image = jim_and_pam
    pj_button.grid()
    pj_button['command'] = lambda: print("Short description of Jim and Pam.")

    label = ttk.Label(main_frame, text='Jim Halpert and Pam Beesley')
    label.grid()

    next_page_button = ttk.Button(main_frame, text="Next")
    next_page_button.grid()
    next_page_button['command'] = lambda: close_window(root)

    root.mainloop()

    happy = happy + 100
    print('Michael Scott has gained 100 happy points! Your current happy score is ', happy)
    return happy


def darryl(mqtt_client, happy):
    """This is the function for when you encounter Darryl's office."""

    root = tkinter.Tk()

    main_frame = ttk.Frame(root, padding=20)
    main_frame.grid()

    darryl_image = tkinter.PhotoImage(file='Darryl.gif')

    darryl_button = ttk.Button(main_frame, image=darryl_image)

    darryl_button.image = darryl_image
    darryl_button.grid()
    darryl_button['command'] = lambda: print("Short description of Darryl Philbin.")

    label = ttk.Label(main_frame, text='Darryl Philbin')
    label.grid()

    next_page_button = ttk.Button(main_frame, text="Next")
    next_page_button.grid()
    next_page_button['command'] = lambda: close_window(root)

    root.mainloop()

    happy = happy + 100
    print('Michael Scott has gained 100 happy points! Your current happy score is ', happy)
    return happy


def cm(mqtt_client, happy):
    """This is the function for when you encounter the desk cluster of Creed and Meredith. It is not dependent on
    the time of day."""

    root = tkinter.Tk()

    main_frame = ttk.Frame(root, padding=20)
    main_frame.grid()

    cm_image = tkinter.PhotoImage(file='Meredith_and_Creed.gif')

    cm_button = ttk.Button(main_frame, image=cm_image)

    cm_button.image = cm_image
    cm_button.grid()
    cm_button['command'] = lambda: print("Short description of Meredith Palmer and Creed Bratton.")

    label = ttk.Label(main_frame, text='Meredith Palmer and Creed Bratton')
    label.grid()

    next_page_button = ttk.Button(main_frame, text="Next")
    next_page_button.grid()
    next_page_button['command'] = lambda: close_window(root)

    root.mainloop()

    happy = happy + 100
    print('Michael Scott has gained 100 happy points! Your current happy score is ', happy)
    return happy


def toby(mqtt_client, happy):
    """This is the function for when you encounter the desk of Toby."""
    root = tkinter.Tk()

    main_frame = ttk.Frame(root, padding=20)
    main_frame.grid()

    toby_image = tkinter.PhotoImage(file='Toby.gif')

    toby_button = ttk.Button(main_frame, image=toby_image)

    toby_button.image = toby_image
    toby_button.grid()
    toby_button['command'] = lambda: print("Short description of Toby Flenderson.")

    label = ttk.Label(main_frame, text='Toby Flenderson')
    label.grid()

    next_page_button = ttk.Button(main_frame, text="Next")
    next_page_button.grid()
    next_page_button['command'] = lambda: close_window(root)

    root.mainloop()

    happy = happy + 100
    print('Michael Scott has gained 100 happy points! Your current happy score is ', happy)
    return happy


def koa(mqtt_client, happy):
    """This is the function for when you encounter the desk cluster of Kevin, Oscar, and Angela."""

    root = tkinter.Tk()

    main_frame = ttk.Frame(root, padding=20)
    main_frame.grid()

    koa_image = tkinter.PhotoImage(file='kra.gif')

    koa_button = ttk.Button(main_frame, image=koa_image)

    koa_button.image = koa_image
    koa_button.grid()
    koa_button['command'] = lambda: print("Short description of Kevin, Oscar, and Angela.")

    label = ttk.Label(main_frame, text='Kevin, Oscar, and Angela')
    label.grid()

    next_page_button = ttk.Button(main_frame, text="Next")
    next_page_button.grid()
    next_page_button['command'] = lambda: close_window(root)

    root.mainloop()

    happy = happy + 100
    print('Michael Scott has gained 100 happy points! Your current happy score is ', happy)
    return happy


def ps(mqtt_client, happy):
    """This is the function for when you encounter the desk cluster of Phyllis and Stanley. On odd hours they
    will be sleeping."""
    root = tkinter.Tk()

    main_frame = ttk.Frame(root, padding=20)
    main_frame.grid()

    ps_image = tkinter.PhotoImage(file='ps.gif')

    ps_button = ttk.Button(main_frame, image=ps_image)

    ps_button.image = ps_image
    ps_button.grid()
    ps_button['command'] = lambda: print("Short description of Phyllis and Stanley.")

    label = ttk.Label(main_frame, text='Phyllis and Stanley')
    label.grid()

    next_page_button = ttk.Button(main_frame, text="Next")
    next_page_button.grid()
    next_page_button['command'] = lambda: close_window(root)

    root.mainloop()

    happy = happy + 100
    print('Michael Scott has gained 100 happy points! Your current happy score is ', happy)
    return happy


# Arm command callbacks
def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")


# Drive button callbacks
def forward_callback(mqtt_client, left_speed_entry, right_speed_entry):
    print("drive_forward")
    mqtt_client.send_message("drive_forward", [left_speed_entry, right_speed_entry])


def left_callback(mqtt_client, left_speed_entry, right_speed_entry):
    print("turn_left")
    mqtt_client.send_message("turn_left", [left_speed_entry, right_speed_entry])


def stop_callback(mqtt_client):
    print("stop")
    mqtt_client.send_message("stop")


def right_callback(mqtt_client, left_speed_entry, right_speed_entry):
    print("turn_right")
    mqtt_client.send_message("turn_right", [left_speed_entry, right_speed_entry])


def back_callback(mqtt_client, left_speed_entry, right_speed_entry):
    print("button_back")
    mqtt_client.send_message("button_back", [left_speed_entry, right_speed_entry])


def next_page(mqtt_client):
    print("page_forward")
    mqtt_client.send_message("page_forward")


def back_page(mqtt_client):
    print("page_back")
    mqtt_client.send_message("page_back")


# Quit and Exit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


def close_window(root):
    """"""
    root.destroy()


main()
