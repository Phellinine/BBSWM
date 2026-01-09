import json
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from typing import Any

import config as conf
from configs import UI_style as Cfg_style

path_logs = conf.player_log_path

font = Cfg_style.font

background = Cfg_style.background
background_sec = Cfg_style.background_sec
background_hover = Cfg_style.background_hover
background_disabled = Cfg_style.background_disabled

foreground = Cfg_style.foreground
foreground_sec = Cfg_style.foreground
foreground_hover = Cfg_style.foreground_hover
foreground_disabled = Cfg_style.foreground_disabled

x = '1000'
y = '500'
space_x = "-1000"
space_y = "+100"

# create window
p_log = tk.Tk()
p_log.title("BBSWM -- Player Log")  # -B-lock für -B-lock -S-erver -W-ork -M-anager
p_log.geometry(x + 'x' + y + space_x + space_y)

style = ttk.Style()
style.map("TButton", background=[("active", background_hover), ("pressed", "#ffffff")],
          foreground=[("active", foreground_hover), ("pressed", "#ffffff")], )
style.configure(style="TButton", relief="flat", background=background, font=Cfg_style.btns["font"],
                foreground=foreground)

style.configure("TLabel", background=background, foreground=foreground, font=font)

style.configure("TFrame", background=background, foreground=foreground)

style.configure("TScrollbar", background=background_sec, foreground=foreground, relief="flat")
style.map("TScrollbar", background=[("active", background_hover), ("disabled", background_disabled)])


def gettime_real(time_dec: int):
    h_real = str(time_dec)[0:2]
    min_real = str(int(int(str(time_dec)[2:4]) / (5 / 3)))
    if len(min_real) == 1:
        min_real = "0" + min_real
    time_real = h_real + min_real
    time_real = time_real[-4:-2] + ":" + time_real[-2:]
    return time_real

def gettime_dec(time_dec):
    h_dec = time_dec[0:2]
    min_dec = str(int(int(time_dec[3:5]) * (5 / 3)))
    if len(min_dec) == 1:
        min_dec = "0" + min_dec
    time_real = int(h_dec + min_dec)
    return time_real


def quick_choose(window):
    def done_cmd(selection: str) -> None:
        for widget in window.winfo_children():
            widget.destroy()

        build(path_logs + selection, window)

    toplevel = tk.Toplevel(window)
    frame = ttk.Frame(toplevel)
    label = ttk.Label(frame, text="Choose File")
    label.pack(anchor="n", padx=10, pady=10)
    path_label = ttk.Label(frame, text=os.path.abspath(path_logs))
    path_label.pack(anchor="n", padx=10, pady=10)
    listbox = tk.Listbox(frame, font=font, selectmode=tk.SINGLE, foreground=foreground_sec, background=background_sec, relief="flat", selectbackground=background_hover, selectforeground=foreground_hover, disabledforeground=foreground_disabled)
    for file in os.listdir(path_logs):
        listbox.insert(tk.END, file)
    listbox.pack()

    buttons_frame = ttk.Frame(toplevel)
    done = ttk.Button(buttons_frame, text="Done", command=lambda command=done_cmd: done_cmd(listbox.selection_get()))
    done.pack(side="left", padx=10, pady=10)
    close = ttk.Button(buttons_frame, text="Exit", command=toplevel.destroy)
    close.pack(side="right", padx=10, pady=10)
    delete = ttk.Button(buttons_frame, text="Delete", command=lambda command=delete_current_file: delete_current_file(path_logs + listbox.selection_get(), toplevel, True, window))
    delete.pack(padx=10, pady=10)

    frame.pack(expand=True, fill="both")
    buttons_frame.pack(expand=True, fill="x")
    toplevel.mainloop()


def delete_current_file(file: str, window: tk.Tk | tk.Toplevel, destroy: bool = False, main: tk.Tk = None):
    if messagebox.askokcancel("Delete File?", "Want to delete the current file?", detail="this cant be undonne"):
        print("hi")
        print(file)
        os.remove(file)
        if destroy:
            window.destroy()
            window = main
        quick_choose(window)


def build(file: str, window: tk.Tk) -> None:
    canvas_bg = background_sec
    canvas_text = foreground
    canvas_lines = foreground_sec
    canvas_object = background_hover


    frame = ttk.Frame(window)
    frame.pack(fill="both", expand=True)

    v_scrollbar = ttk.Scrollbar(frame, orient="vertical")
    h_scrollbar = ttk.Scrollbar(frame, orient="horizontal")
    v_scrollbar.pack(side="right", fill="y", padx=10, pady=10)
    h_scrollbar.pack(side="bottom", fill="x", pady=10)

    with open(file, "r") as file_open:
        py_p_log: dict[str, dict[str, Any]] = json.load(file_open)
        file_open.close()

    meta_start = py_p_log["meta"]["start time"][0:2]
    meta_start = meta_start+"00"
    meta_end = py_p_log["meta"]["end time"][0:2]
    meta_end = int(meta_end + "00") + 100

    # create navigation menu
    menubar = tk.Menu(frame, tearoff=0, font=font, foreground=foreground_sec, background=background_sec, relief="flat",
                      activebackground=background_hover, activeforeground=foreground_hover)

    file_menu = tk.Menu(menubar, tearoff=0, relief="flat", font=font, foreground=foreground_sec,
                        background=background_sec, activebackground=background_hover, activeforeground=foreground_hover)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Quick File", command=lambda cmd=quick_choose: quick_choose(window))
    file_menu.add_separator()
    file_menu.add_command(label="Delete", command=lambda cmd=delete_current_file: delete_current_file(file, window))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=window.destroy)

    window.config(menu=menubar)

    # canvases with players playtime and time markers and a title
    frame_up = ttk.Frame(frame)
    frame_up.pack(anchor="n", fill="both")
    playtimes = tk.Canvas(frame, bg=canvas_bg, yscrollcommand=v_scrollbar.set,
                          xscrollcommand=h_scrollbar.set, scrollregion=(0, 0, meta_end, len(
            py_p_log["players"]) * conf.plog_scale_height))  # playtimes
    players = tk.Canvas(frame, yscrollcommand=v_scrollbar.set, bg=canvas_bg, width=150,
                        scrollregion=(0, 0, 0, len(py_p_log["players"]) * conf.plog_scale_height))  # players
    title_canvas = tk.Canvas(frame_up, height=100, width=150, bg=canvas_bg) # title
    time_canvas = tk.Canvas(frame_up, height=100, bg=canvas_bg, xscrollcommand=h_scrollbar.set, scrollregion=(0, 0, meta_end, 0)) # time marks

    title_canvas.pack(anchor="w", side="left", expand=False, padx=10, pady=10)
    time_canvas.pack(anchor="e", side="right", fill="x", expand=True, padx=10, pady=10)
    playtimes.pack(anchor="e", side="right", expand=True, fill="both", padx=10, pady=10)
    players.pack(anchor="w", side="left", fill="y", expand=False, padx=10, pady=10)

    # create playtime and players
    num: int = 0
    length_time = len(py_p_log["players"]) * conf.plog_scale_height + 20
    for player in py_p_log["players"]:
        players.create_text(10, (num * conf.plog_scale_height) + ((conf.plog_scale_height - 10) / 2 + 5), text=player,
                            justify="left", anchor="w", font=font, fill=canvas_text)

        for time in py_p_log["players"][player]["playtime"]:
            on = gettime_dec(time["on"])
            of = gettime_dec(time["of"])
            on: int = on - int(meta_start)
            of: int = of - int(meta_start)
            corner_up: tuple[float, float] = (on / conf.plog_scale_width, (conf.plog_scale_height * num) + 10)
            corner_down: tuple[float, float] = (of / conf.plog_scale_width,
                                                (conf.plog_scale_height * num) + conf.plog_scale_height)
            playtimes.create_rectangle(corner_up, corner_down, fill=canvas_object, outline=canvas_text, width=2)

        playtimes.create_line(0, conf.plog_scale_height * num + 5, length_time, conf.plog_scale_height * num + 5, fill=canvas_lines, width=2)
        players.create_line(0, conf.plog_scale_height * num + 5, length_time, conf.plog_scale_height * num + 5, fill=canvas_lines, width=2)
        num += 1

    playtimes.create_line(0, conf.plog_scale_height * num + 5, length_time, conf.plog_scale_height * num + 5, fill=canvas_lines, width=2)
    players.create_line(0, conf.plog_scale_height * num + 5, length_time, conf.plog_scale_height * num + 5, fill=canvas_lines, width=2)

    # create time marks
    start = int(meta_start)
    end = int(meta_end)

    for time in range(start, end, int(conf.plog_scale_width * 30)):
        time = gettime_real(time)[0:4] + "0"
        text = time
        time = gettime_dec(time)
        time_canvas.create_text(10 + ((time - start) / conf.plog_scale_width), 40, text=text, angle=40,
                                fill=canvas_text, font=font)
        time_canvas.create_line((time - start) / conf.plog_scale_width, 60, (time - start) / conf.plog_scale_width, 100,
                                dash=10, fill=canvas_lines, width=2)
        playtimes.create_line((time - start) / conf.plog_scale_width, 0, (time - start) / conf.plog_scale_width,
                              num_players * conf.plog_scale_height + 20,
                              dash=10, fill=canvas_lines, width=2)

    # create title_canvas
    title_canvas.create_line(0, 0, 150, 100, fill=canvas_lines, width=2)
    title_canvas.create_text(70, 95, text="player", anchor="s", justify="left", fill=canvas_text, font=font)
    title_canvas.create_text(135, 30, text="time", angle=90, anchor="e", justify="left", fill=canvas_text, font=font)

    # Yview Function
    def multiple_yview(*args):
        playtimes.yview(*args)
        players.yview(*args)
        # print(*args)

    def multiple_xview(*args):
        playtimes.xview(*args)
        time_canvas.xview(*args)

    v_scrollbar.config(command=multiple_yview)
    h_scrollbar.config(command=multiple_xview)


if __name__ == "__main__":
    safe_build()
