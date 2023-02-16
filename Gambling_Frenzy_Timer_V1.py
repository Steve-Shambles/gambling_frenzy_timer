"""GF Timer V1.0
   Gambling Frenzy Timer, Helps UK players
   avoid being flagged as a problem gambler
   by taking a break before the hourly pop up."""

from datetime import datetime
import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


root = tk.Tk()
root.title("GF Timer V1.0")
root.resizable(False, False)
root.attributes("-topmost", True)

logo_frame = tk.LabelFrame(root)
logo_frame.grid()

# Display logo in logo frame.
try:
    logo_image = Image.open("logo.jpg")
except FileNotFoundError as e:
    tk.messagebox.showinfo("FileNotFoundError",
                           "logo.jpg not found.")
    root.destroy()
    sys.exit(1)

logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(logo_frame, image=logo_photo)
logo_label.logo_image = logo_photo
logo_label.grid(padx=2, pady=2, row=0, column=0)

# 57 mins = 3420 SECONDS.
global SECONDS
SECONDS = 3420
# Keep track of whether the timer is PAUSED.
global PAUSED
PAUSED = False
# Keep track of the scheduled call to update_countdown().
AFTER_ID = None


def about():
    """Pop up msg box explaining what program does and how to use it."""
    tk.messagebox.showinfo('GF Timer V1.0',
                           'Gambling Frenzy Timer is a straight-forward\n'
                           'on top, countdown timer and alarm for UK\n'
                           'online casino and bingo gamblers.\n\n'
                           'The UK Gambling Commisson insist that casinos '
                           'constantly harrass players by messages, and '
                           'even bans, if they gamble for more than an\n'
                           'an hour at a time,\n\n'
                           'Run this app when you first log in to a casino\n'
                           'and it will remind you after 57 mins to take'
                           ' a break and avoid the hourly pop ups and this '
                           'may help avoid you getting flagged as a '
                           'problem gambler.\n'
                           '\nThis program is FREEWARE,\nbut remains'
                           ' (c) Steve Shambles Feb 2023')


def update_countdown():
    """ Update the countdown label and remaining SECONDS."""
    global SECONDS, PAUSED, AFTER_ID

    if not PAUSED:
        m, s = divmod(SECONDS, 60)
        h, m = divmod(m, 60)
        countdown_label.config(font=("helvetica", 14), fg="indianred",
                               text='{:d}:{:02d}:{:02d}'.format(h, m, s))
        SECONDS -= 1

        if SECONDS > -1:
            AFTER_ID = root.after(1000, update_countdown)
        else:
            messagebox.showinfo('Gambling Frenzy Timer Alert.',
                                '57 mins have passed,\n'
                                'Log out and take a break, OK?')
            root.destroy()


def pause_timer():
    """ Pause or resume the countdown."""
    global PAUSED

    PAUSED = not PAUSED

    if not PAUSED:
        # Resume the countdown.
        pause_btn.config(text=" Pause ")
        update_countdown()
    else:
        # Pause the countdown.
        pause_btn.config(text="Resume")


def restart():
    """ Restart the countdown. """
    global SECONDS, PAUSED, AFTER_ID

    SECONDS = 3420
    PAUSED = False

    pause_btn.config(text=" Pause ")
    time_label.config(font=("helvetica", 11),
                      text="Started countdown at: " +
                      datetime.now().strftime('%H:%M'))

    countdown_label.config(text="")

    if AFTER_ID:
        root.after_cancel(AFTER_ID)

    update_countdown()


time_label = tk.Label(root,
                      font=("helvetica", 11),
                      text="Started countdown at: " +
                      datetime.now().strftime('%H:%M'))
time_label.grid(pady=(10, 5))

countdown_label = tk.Label(root, text="")
countdown_label.grid()

btn_frame = tk.Frame(root)
btn_frame.grid()

restart_btn = tk.Button(btn_frame, text="Restart",
                        bg="lime", command=restart)
restart_btn.grid(row=4, column=0, pady=10)

pause_btn = tk.Button(btn_frame, text=" Pause ",
                      bg="gold", command=pause_timer)
pause_btn.grid(row=4, column=1, pady=10)


# Create drop down menu.
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Info', menu=file_menu)
file_menu.add_command(label='About', command=about)
root.config(menu=menu_bar)


# Start the countdown.
update_countdown()


root.mainloop()
