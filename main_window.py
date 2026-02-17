import threading
import tkinter as tk
from tkinter import ttk

import API
import GUI
import P_log
from tk_windows import first_start
import config as conf
import desktop_message
from configs import UI_style as Cfg_style


def build(first_startup: bool = False):
    font = Cfg_style.font

    background = Cfg_style.background
    background_sec = Cfg_style.background_sec
    background_hover = Cfg_style.background_hover
    background_disabled = Cfg_style.background_disabled

    foreground = Cfg_style.foreground
    foreground_sec = Cfg_style.foreground
    foreground_hover = Cfg_style.foreground_hover
    foreground_disabled = Cfg_style.foreground_disabled

    tk_instance = tk.Tk()
    stop = threading.Event()

    style = ttk.Style(tk_instance)

    style.configure(style="TButton", relief="flat", background=background, font=Cfg_style.btns["font"],
                    foreground=foreground)
    style.map("TButton", background=[("active", background_hover), ("pressed", "#ffffff"), ("disabled", background_disabled)],
              foreground=[("active", foreground_hover), ("pressed", "#ffffff"), ("disabled", foreground_disabled)])

    style.configure("TLabel", background=background, foreground=foreground, font=font)

    style.configure("TFrame", background=background, foreground=foreground)

    style.configure("TScrollbar", background=background_sec, foreground=foreground, relief="flat")
    style.map("TScrollbar", background=[("active", background_hover), ("disabled", background_disabled)])

    style.configure("TRadiobutton", background=background_sec, foreground=foreground, font=font, borderwidth=0,
                    padding=2)
    style.map("TRadiobutton", background=[("active", background_hover), ("pressed", "#ffffff")],
              foreground=[("active", foreground_hover), ("pressed", "#ffffff")])

    style.configure("TCheckbutton", background=background_sec, foreground=foreground, font=font, borderwidth=0,
                    padding=2)
    style.map("TCheckbutton", background=[("active", background_hover), ("pressed", "#ffffff")],
              foreground=[("active", foreground_hover), ("pressed", "#ffffff")])

    style.configure("TLabelframe", background=background, foreground=foreground, labelmargins=5, borderwidth=2,
                    bordercolor=foreground_sec)

    style.configure("TLabelframe.Label", font=font, background=background, foreground=foreground)

    style.configure("TEntry", font=font, background=background, foreground=foreground, relief="flat")

    def create_p_log():
        P_log.build(file=conf.player_log_full, window=tk.Toplevel(tk_instance))

    def create_gui():
        GUI.build(window=tk.Toplevel(tk_instance))
        threading.Thread(target=GUI.triger_update, args=(stop,)).start()

    def startup_window():
        first_start.build(window=tk_instance)

    def quit_function():
        API.close_server()
        desktop_message.simple("BBSWM", "server sucessfully shut down")

        tk_instance.destroy()
        stop.set()

    def debugging_quit():
        tk_instance.destroy()
        stop.set()


    x = '400'
    y = '200'
    space_x = "-1000"
    space_y = "+100"

    if first_startup:
        tk_instance.title("BBSWM -- Welcome!")  # -B-lock für -B-lock -S-erver -W-ork -M-anager
        tk_instance.geometry('800' + 'x' + '700' + space_x + space_y)
        startup_window()
        return None

    tk_instance.title("BBSWM -- Choose Window")  # -B-lock für -B-lock -S-erver -W-ork -M-anager
    tk_instance.geometry(x + 'x' + y + space_x + space_y)

    main_frame = ttk.Frame(tk_instance)
    p_log = ttk.Button(main_frame, text="Player Log", command=create_p_log)
    gui = ttk.Button(main_frame, text="GUI", command=create_gui)
    quit_btn = ttk.Button(main_frame, text="Quit", command=quit_function)
    quit_deb_btn = ttk.Button(main_frame, text="Quit(unsafe, only for testing)", command=debugging_quit)

    main_frame.pack(expand=True, fill="both")
    p_log.pack()
    gui.pack()
    quit_btn.pack()
    quit_deb_btn.pack()

    return tk_instance

if __name__ == "__main__":
    build(True)
