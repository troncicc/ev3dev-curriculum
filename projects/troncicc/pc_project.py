import tkinter
from tkinter import ttk


def main():
    root = tkinter.Tk()

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

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


def close_window(root):
    root.destroy()


main()
