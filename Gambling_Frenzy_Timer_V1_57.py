"""GF Timer V1.57
   Gambling Frenzy Timer, Helps UK players
   avoid being flagged as a problem gambler
   by being reminded to take a break before
   the hourly pop up, or a user difined time."""

from datetime import datetime
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import webbrowser as web

from PIL import Image, ImageTk


root = tk.Tk()
root.title('GF Timer V1.57')
root.resizable(False, False)
root.attributes('-topmost', True)  # Always on top
root.eval('tk::PlaceWindow . Center')

root_frame = tk.LabelFrame(root)
root_frame.grid()

# Load logo image,making sure it exists and error trapped.
try:
    logo_image = Image.open('gft_logo.jpg')
except FileNotFoundError as file_error:
    tk.messagebox.showinfo('FileNotFoundError', file_error)
    root.destroy()
    sys.exit(1)

# Display logo in logo frame.
logo_frame = tk.LabelFrame(root_frame)
logo_frame.grid()
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

# Keep track of when the timer was started.
start_time = datetime.now()


def set_minutes():
    """ Allow user to set owm amount of time in minutes. """
    global SECONDS
    minutes = simpledialog.askinteger('Set Minutes',
                                      'Enter a number of minutes (1-240):',
                                      minvalue=1, maxvalue=240)
    if minutes is not None:
        SECONDS = minutes * 60


def about():
    """ Pop up msg box explaining what program does and how to use it."""
    tk.messagebox.showinfo('GF Timer V1.57',
                           'Gambling Frenzy Timer is a straight-forward\n'
                           'on top, countdown timer and alarm for UK\n'
                           'online casino and bingo gamblers.\n\n'
                           'The UK Gambling Commisson insist that casinos '
                           'constantly harrass players by messages, and '
                           'even bans, if they gamble for more than an\n'
                           'an hour at a time,\n\n'
                           'Run this app when you first log in to a casino\n'
                           'and it will remind you after '
                           '57 mins '
                           '(or choose your own time limit from the info '
                           'menu) to take '
                           'a break and avoid the hourly pop ups from the '
                           'casino.\n\nDoing this may help you avoid '
                           'getting flagged as a '
                           'problem gambler, though most casinos interpret '
                           'the rules differently.\n'
                           '\nThis program is FREEWARE,\nbut remains'
                           ' (c) Steve Shambles Feb 2023')


def update_countdown():
    """ Update the countdown label and remaining SECONDS."""
    global SECONDS, PAUSED, AFTER_ID, start_time

    # If the window has already been destroyed, return.
    if not root_frame.winfo_exists():
        return

    m, s = divmod(SECONDS, 60)
    h, m = divmod(m, 60)
    elapsed_time = datetime.now() - start_time
    total_seconds = int(elapsed_time.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    countdown_label.config(font=('helvetica', 10), fg='blue',
                           text='{:d}:{:02d}:{:02d}'.format(h, m, s))

    elapsed_label.config(text='Total elapsed time: {:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds))

    if not PAUSED:
        SECONDS -= 1

        if SECONDS > -1:
            AFTER_ID = root_frame.after(1000, update_countdown)
        else:
            # Cancel any pending `after` calls before destroying window.
            root_frame.after_cancel(AFTER_ID)
            messagebox.showinfo('Gambling Frenzy Timer Alert.',
                                'This is your alarm call,\n'
                                'Log out and take a break, OK?\n'
                                '\nGF Timer will now exit,\n'
                                'Run me again if needed.')

            root_frame.destroy()
            root.destroy()
            sys.exit()
    else:
        AFTER_ID = root_frame.after(1000, update_countdown)


def pause_timer():
    """ Pause or resume the countdown."""
    global PAUSED

    PAUSED = not PAUSED

    if not PAUSED:
        # Resume the countdown.
        pause_btn.config(text=' Pause ')
        update_countdown()
    else:
        # Pause the countdown.
        pause_btn.config(text='Resume')


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
        root_frame.after_cancel(AFTER_ID)

    update_countdown()


def start():
    """ Start the countdown. """
    logo_frame.destroy()
    start_btn.destroy()
    
    time_label.grid(pady=(1, 2))
    restart_btn.grid(row=4, column=1, pady=5, padx=8)
    pause_btn.grid(row=4, column=2, pady=5)
    elapsed_label.grid()
    update_countdown()
    # Place app roughly in top right corner of screen.
    root.geometry("+{}+{}".format(root_frame.winfo_screenwidth()-200, 0))


def exit_gftimer():
    """ Yes-no requestor to exit program. """
    ask_yn = messagebox.askyesno('Question',
                                 'Quit GF Timer?')
    if ask_yn is False:
        return
    root_frame.destroy()
    sys.exit()


def donate_me():
    """ User splashes the cash here! """
    web.open('https:\\paypal.me/photocolourizer')


def visit_github():
    """View my source codes on GitHub."""
    web.open('https://github.com/steve-shambles?tab=repositories')




btn_frame = tk.Frame(root_frame)
btn_frame.grid()

start_btn = tk.Button(btn_frame, font=('helvetica', 12),
                      text='Start Timer', bg='lime', command=start)
start_btn.grid(row=4, column=0, pady=(21, 0))


restart_btn = tk.Button(btn_frame, text='Restart',
                        bg='lime', command=restart)
pause_btn = tk.Button(btn_frame, text=' Pause ',
                      bg='gold', command=pause_timer)

countdown_label = tk.Label(root_frame, text='')
countdown_label.grid()

time_label = tk.Label(root_frame,
                      font=('helvetica', 8),
                      text='Started countdown at: ' +
                      datetime.now().strftime('%H:%M'))

elapsed_time = datetime.now() - start_time
elapsed_label = tk.Label(font=('helvetica', 8), text='')

# Create drop down menu.
menu_bar = tk.Menu(root_frame)
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Info', menu=file_menu)
file_menu.add_command(label='Set Minutes', command=set_minutes)
file_menu.add_separator()
file_menu.add_command(label='About', command=about)
file_menu.add_command(label='Python source code on GitHub',
                      command=visit_github)
file_menu.add_command(label='Make a small donation via PayPal',
                      command=donate_me)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=exit_gftimer)
root.config(menu=menu_bar)

# Capture user exiting the program and ask if sure.
root.protocol('WM_DELETE_WINDOW', exit_gftimer)


root_frame.mainloop()
