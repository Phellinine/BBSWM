import datetime
import threading
import tkinter as tk
from time import sleep
from tkinter import ttk

import nextcloud_client

import API
import config
from configs import UI_style as Cfg_style

stream_options: list[tuple[str, str]] = [('Global', '0'),
                                                   ('All', '1'),
                                                   ("Warn", "2"),
                                                   ("Error", "3"),
                                                   ("chats", "4"),
                                                   ("experiment2", "5")]
stream_params: dict[str, str] = {"": "",
     "0": "[Global]",
     "1": "",
     "2": "/WARN",
     "3": "/ERROR",
     "4": ["[Server thread/INFO]", "issued server command", "chat",   "-[Server thread/INFO]: ", "-issued server command"],
     "5": ["![Server",]}


stream = API.Console([""], "[")
global console
global autoscroll

player_log_file = datetime.date.today().isoformat() + ".json"
player_log_path = "old/player_logs/"
player_log_full = player_log_path + player_log_file
NC = nextcloud_client.Client('https://gmb-cloud.wiesan.de')
nc_path = "./Minecraft mit detti/server player logs/"

font = Cfg_style.font

background = Cfg_style.background
background_sec = Cfg_style.background_sec
background_hover = Cfg_style.background_hover
background_disabled = Cfg_style.background_disabled

foreground = Cfg_style.foreground
foreground_sec = Cfg_style.foreground
foreground_hover = Cfg_style.foreground_hover
foreground_disabled = Cfg_style.foreground_disabled



def triger_update(stop_event: threading.Event) -> None:
    while not stop_event.is_set():
        update_stream()
        sleep(10)


def usr_quit(window: tk.Toplevel) -> None:
    """
    quit the window
    :param window: main window which will be destroyed
    :return: None
    """
    #try:
    #    NC.login("72361402", "mbJHD-c3WEM-3LAQC-LJTzi-F3WWf")
    #    if player_log_file in [ds.name for ds in NC.list(path=nc_path, properties="path")]:
    #        print("hii")
    #except HTTPResponseError:
    #    API.Message(API.TYPE["nextcloud_error"])
    window.destroy()
    return


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


def update_stream() -> None:
    """
    takes a tkinter text object and appends new stream output
    :return: None
    """
    global autoscroll
    global console
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


def force_update_stream(selected: tk.Variable) -> None:
    """
    takes a tkinter text object and replaces its content with the wanted stream, thereby force updating it
    :param selected: tkinter variable with the selected stream filtering parameter
    :return: None
    """
    global stream
    console['state'] = 'normal'
    console.delete('1.0', tk.END)
    console['state'] = 'disabled'
    stream = API.Console([""], stream_params[selected.get()])
    update_stream()


def build(window: tk.Toplevel) -> None:
    """
    create a window showing the current output of the server stream
    :param window:
    :return: None
    """
    global console
    global autoscroll
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

    radio_frame = ttk.Labelframe(left_frame, text=" Radio ")
    radio_frame.pack(ipady=5, fill="x")

    # create radio buttons for streams
    selected_stream = tk.Variable()
    for option in stream_options:
        r = ttk.Radiobutton(
            radio_frame,
            text=option[0],
            value=option[1],
            variable=selected_stream
        )
        r.pack(fill='x', padx=10, pady=5)

    # create update button
    ttk.Button(left_frame, text="Update", command=lambda: force_update_stream(selected_stream)).pack(pady=20)
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

    force_update_stream(selected_stream)
