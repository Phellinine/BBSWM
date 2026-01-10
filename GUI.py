import datetime
import tkinter as tk
from tkinter import ttk

import nextcloud_client
from nextcloud_client import HTTPResponseError

import API
import config
from configs import UI_style as Cfg_style

stream_options: list[tuple[str, str]] = [('Global', '[Global]'),
                                         ('All', ''),
                                         ("Warn", "/WARN"),
                                         ("Error", "/ERROR")]

stream = API.Console([""], "[")

player_log_file = datetime.date.today().isoformat() + ".json"
player_log_path = "old/player_logs/"
player_log_full = player_log_path + player_log_file
NC = nextcloud_client.Client('https://gmb-cloud.wiesan.de')
nc_path = "./Minecraft mit detti/server player logs/"
run = True

font = Cfg_style.font

background = Cfg_style.background
background_sec = Cfg_style.background_sec
background_hover = Cfg_style.background_hover
background_disabled = Cfg_style.background_disabled

foreground = Cfg_style.foreground
foreground_sec = Cfg_style.foreground
foreground_hover = Cfg_style.foreground_hover
foreground_disabled = Cfg_style.foreground_disabled


def usr_quit(window: tk.Tk) -> None:
    """
    quit the window
    :param window: main window which will be destroyed
    :return: None
    """
    global run
    try:
        NC.login("72361402", "mbJHD-c3WEM-3LAQC-LJTzi-F3WWf")
        if player_log_file in [ds.name for ds in NC.list(path=nc_path, properties="path")]:
            print("hii")
    except HTTPResponseError:
        API.Message(API.TYPE["nextcloud_error"])
    run = False
    window.quit()


def get_stream() -> str:
    """
    gets the current stream from the exaroton api and seperates lines
    :return: the current stream, with lines seperated with line breaks
    """
    global stream
    out = ""
    for line in stream.get():
        out += "\n" + line
    stream.update_hist()
    return out


def update_stream(console: tk.Text, autoscroll: tk.Variable) -> None:
    """
    takes a tkinter text object and appends new stream output
    :param console: tkinter text object where the stream is displayed
    :param autoscroll: tkinter variable with bool if the window should scroll to the most recent stream output
    :return: None
    """
    try:
        console['state'] = 'normal'
        console.insert(tk.END, get_stream())
        if autoscroll.get() == "1":
            console.see(tk.END)
        console['state'] = 'disabled'
    except tk.TclError:
        API.Message(API.TYPE["int_fail"])
    except ConnectionError:
        console['state'] = 'normal'
        console.delete('1.0', tk.END)
        console.insert(tk.END,
                    "Server didn't respond correctly. Probably starting/stopping. Wait. If error stays contact admin.")
        console['state'] = 'disabled'


def force_update_stream(selected: tk.Variable, console: tk.Text, autoscroll: tk.Variable) -> None:
    """
    takes a tkinter text object and replaces its content with the wanted stream, thereby force updating it
    :param selected: tkinter variable with the selected stream filtering parameter
    :param console: tkinter text object where the stream is displayed
    :param autoscroll: tkinter variable with bool if the window should scroll to the most recent stream output
    :return: None
    """
    global stream
    console['state'] = 'normal'
    console.delete('1.0', tk.END)
    console['state'] = 'disabled'
    stream = API.Console([""], selected.get())
    update_stream(console, autoscroll)


def build(window: tk.Tk):
    """
    create a window showing the current output of the server stream
    :param window:
    :return:
    """
    x = '1000'
    y = '500'
    space_x = "-1000"
    space_y = "+100"

    # specify window
    window.title("BBSWM -- Start")  # -B-lock für -B-lock -S-erver -W-ork -M-anager
    window.geometry(x + 'x' + y + space_x + space_y)

    autoscroll = tk.Variable(value="1")



    # app-icon
    try:
        photo = tk.PhotoImage(file=config.icon_path)
        window.iconphoto(False, photo)
    except tk.TclError:
        API.Message(API.TYPE["file_not_found"])

    main_frame = ttk.Frame(window)
    main_frame.pack(fill="both", expand=True)

    # left frame
    left_frame = ttk.Frame(main_frame)
    left_frame.pack(side="left", fill="both", expand=False, pady=10, padx=10)

    ttk.Label(left_frame, text="Streams").pack(pady=20)

    radio_frame = ttk.Labelframe(left_frame, text=" Radio ")
    radio_frame.pack(ipady=5, fill="x")

    # create radio buttons for streams
    selected_stream = tk.StringVar()
    for option in stream_options:
        r = ttk.Radiobutton(
            radio_frame,
            text=option[0],
            value=option[1],
            variable=selected_stream
        )
        r.pack(fill='x', padx=10, pady=5)

    # create update button
    ttk.Button(left_frame, text="Update", command=lambda: force_update_stream(selected_stream, console,
                                                                              autoscroll)).pack(pady=20)
    # create auto scroll button
    ttk.Checkbutton(
        left_frame,
        text="Auto Scroll",
        variable=autoscroll
    ).pack(pady=10)
    # create quit button
    ttk.Button(left_frame, text="Quit", command=lambda: usr_quit(window)).pack(side="bottom", pady=20)

    # create a vertical separator
    separator = ttk.Separator(main_frame, orient="vertical")
    separator.pack(side="left", fill="y", pady=10)

    # right frame
    right_frame = ttk.Frame(main_frame)
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    ttk.Label(right_frame, text="Stream output").pack(pady=20)

    # create text with scrollbar
    v_scrollbar = ttk.Scrollbar(right_frame)
    v_scrollbar.pack(side="right", fill="y")
    console = tk.Text(right_frame, yscrollcommand=v_scrollbar.set, state="disabled", font=font, background=background_sec, foreground=foreground_sec, relief="flat", selectbackground=background_hover, selectforeground=foreground_hover)
    console.pack(expand=True, fill="both")
    v_scrollbar.config(command=console.yview)

    force_update_stream(selected_stream, console, autoscroll)
