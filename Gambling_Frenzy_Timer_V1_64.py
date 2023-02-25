"""GF Timer V1.64
   Gambling Frenzy Timer, Cross-platform.
   Helps UK players to avoid being flagged as a
   problem gambler. Feb 2023. Steve Shambles"""

from datetime import datetime
import os
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import threading
import time
import webbrowser as web

from PIL import Image, ImageTk
import simpleaudio as sa


root = tk.Tk()
root.title('GF Timer V1.64')
root.resizable(False, False)
root.attributes('-topmost', True)


def file_missing(filename):
    """ Call with any exception when a file check fails. """
    tk.messagebox.showinfo('FileNotFoundError', file_error)
    root.destroy()
    sys.exit(1)


# Check for assests, making sure they exists and error trapped.
try:
    window_icon = Image.open('minutes.ico')
    ico_minutes = Image.open(r'icons\minutes.ico')
    ico_about = Image.open(r'icons\about-16x16.ico')
    ico_donate = Image.open(r'icons\donation-16x16.ico')
    ico_exit = Image.open(r'icons\exit-16x16.ico')
    ico_github = Image.open(r'icons\github-16x16.ico')

    if not os.path.exists('alarm.wav'):
        file_error = 'The file alarm.wav is missing.'
        raise FileNotFoundError(file_error)

    if not os.path.exists('gft_help.txt'):
        file_error = 'The file gft_help.txt is missing.'
        raise FileNotFoundError(file_error)

except FileNotFoundError as file_error:
    file_missing(file_error)

# Had to place here as needs to do file exist check first.
root.iconbitmap('minutes.ico')

global SECONDS  # 57 mins = 3420 SECONDS.
global PAUSED
SECONDS = 3420
PAUSED = False
start_time = datetime.now()
AFTER_ID = None


def set_minutes():
    """ Allow user to set owm amount of time in minutes. """
    global SECONDS
    minutes = simpledialog.askinteger('Set Minutes',
                                      'Enter a number of minutes (1-9999):',
                                      minvalue=1, maxvalue=9999)
    if minutes is not None:
        SECONDS = minutes * 60


def about():
    """ Display text file, explaining what program does and how to use it."""
    web.open('gft_help.txt')


def play_sound(wave_obj):
    """Play the alarm.wav sound when timer is zero, non-blocking."""
    play_obj = wave_obj.play()
    # play_obj.wait_done()


def update_countdown():
    """ Update the countdown label and remaining SECONDS."""
    global SECONDS, PAUSED, AFTER_ID, start_time

    # If the window has already been destroyed, return.
    if not root.winfo_exists():
        return

    m, s = divmod(SECONDS, 60)
    h, m = divmod(m, 60)
    elapsed_time = datetime.now() - start_time
    total_seconds = int(elapsed_time.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    elapsed_label.config(font=('Ariel', 10, 'bold'), bg='black', fg='lime',
                         text='Total elapsed time: {:02d}:{:02d}:{:02d}'.
                         format(hours, minutes, seconds))

    countdown_label.config(font=('helvetica', 22, 'bold'), fg='navyblue',
                           text='{:d}:{:02d}:{:02d}'.format(h, m, s))

    if not PAUSED:
        SECONDS -= 1

        if SECONDS > -1:
            AFTER_ID = root.after(1000, update_countdown)
        else:
            # Cancel any pending `after` calls before destroying window.
            root.after_cancel(AFTER_ID)

            wave_obj = sa.WaveObject.from_wave_file('alarm.wav')
            thread = threading.Thread(target=play_sound, args=(wave_obj,))
            thread.start()

            messagebox.showinfo('Gambling Frenzy Timer Alert.',
                                'This is your alarm call,\n'
                                'Log out and take a break, OK?\n'
                                '\nGF Timer will now exit,\n'
                                'Run me again if needed.')

            root.destroy()
            sys.exit()
    else:
        AFTER_ID = root.after(1000, update_countdown)


def pause_timer():
    """ Pause or resume the countdown."""
    global PAUSED, AFTER_ID

    PAUSED = not PAUSED

    if not PAUSED:
        pause_btn.config(text=' Pause ')
        AFTER_ID = root.after(1000, update_countdown)
    else:
        pause_btn.config(text='Resume')
        root.after_cancel(AFTER_ID)


def restart():
    """ Restart the countdown. """
    global SECONDS, PAUSED, AFTER_ID

    SECONDS = 3420
    PAUSED = False

    pause_btn.config(text=' Pause ')
    time_label.config(font=('helvetica', 8),
                      text='Started countdown at: ' +
                      datetime.now().strftime('%H:%M'))

    countdown_label.config(text='')

    if AFTER_ID:
        root.after_cancel(AFTER_ID)

    update_countdown()


def start():
    """ Start the countdown. """
    restart_btn.grid(row=4, column=1, pady=5, padx=8)
    pause_btn.grid(row=4, column=2, pady=5)

    time_label.grid(pady=(1, 2))
    elapsed_label.grid()

    update_countdown()

    # Place app roughly in top right corner of screen.
    root.geometry('+{}+{}'.format(root.winfo_screenwidth()-300, 0))


def exit_gftimer():
    """ Yes-no requestor to exit program. """
    ask_yn = messagebox.askyesno('Are you sure?',
                                 'Quit GF Timer?')
    if ask_yn is False:
        return
    root.destroy()
    sys.exit()


def donate_me():
    """ User splashes the cash here! """
    web.open('https:\\paypal.me/photocolourizer')


def visit_github():
    """View my source codes on GitHub."""
    web.open('https://github.com/steve-shambles?tab=repositories')


btn_frame = tk.Frame(root)
btn_frame.grid()

restart_btn = tk.Button(btn_frame, text='Restart',
                        bg='lime', command=restart)
pause_btn = tk.Button(btn_frame, text=' Pause ',
                      bg='gold', command=pause_timer)

countdown_label = tk.Label(root, text='')
countdown_label.grid()

time_label = tk.Label(root,
                      font=('helvetica', 8),
                      text='Started countdown at: ' +
                      datetime.now().strftime('%H:%M'))

elapsed_time = datetime.now() - start_time
elapsed_label = tk.Label(font=('helvetica', 8), text='')


# pre-load icons for drop-down menu.
about_icon = ImageTk.PhotoImage(file='icons/about-16x16.ico')
exit_icon = ImageTk.PhotoImage(file='icons/exit-16x16.ico')
donation_icon = ImageTk.PhotoImage(file='icons/donation-16x16.ico')
github_icon = ImageTk.PhotoImage(file='icons/github-16x16.ico')
minutes_icon = ImageTk.PhotoImage(file='icons/minutes.ico')

# Create drop down menu.
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Info', menu=file_menu)
file_menu.add_command(label='Set Minutes', compound='left',
                      image=minutes_icon, command=set_minutes)
file_menu.add_separator()
file_menu.add_command(label='About', compound='left',
                      image=about_icon, command=about)
file_menu.add_command(label='Python source code on GitHub',
                      compound='left', image=github_icon,
                      command=visit_github)
file_menu.add_command(label='Make a small donation via PayPal',
                      compound='left',
                      image=donation_icon, command=donate_me)
file_menu.add_separator()
file_menu.add_command(label='Exit', compound='left',
                      image=exit_icon, command=exit_gftimer)
root.config(menu=menu_bar)

# Capture user exiting the program and ask if sure.
root.protocol('WM_DELETE_WINDOW', exit_gftimer)

start()


root.mainloop()
