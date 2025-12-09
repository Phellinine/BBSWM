import json
import tkinter as tk
from tkinter import ttk
from typing import Any

import config as conf

x = '1000'
y = '500'
space_x = "-1000"
space_y = "+100"

# create window
p_log = tk.Tk()
p_log.title("BBSWM -- Player Logs")  # -B-lock für -B-lock -S-erver -W-ork -M-anager
p_log.geometry(x + 'x' + y + space_x + space_y)

frame = ttk.Frame(p_log)
frame.pack(padx=10, pady=10, fill="both", expand=True)

v_scrollbar = ttk.Scrollbar(frame, orient="vertical")
h_scrollbar = ttk.Scrollbar(frame, orient="horizontal")
v_scrollbar.pack(side="right", fill="y")
h_scrollbar.pack(side="bottom", fill="x")

def gettime_real(time_dec: int):
    h_real = str(time_dec)[0:2]
    min_real = str(int(int(str(time_dec)[2:4])/(5/3)))
    if len(min_real) == 1:
        min_real = "0"+min_real
    time_real = h_real + min_real
    time_real = time_real[-4:-2] + ":" + time_real[-2:]
    return time_real

def gettime_dec(time_dec):
    h_dec = time_dec[0:2]
    min_dec = str(int(int(time_dec[3:5]) * (5 / 3)))
    if len(min_dec) == 1:
        min_dec = "0"+min_dec
    time_dec = int(h_dec + min_dec)
    return time_dec


with open(conf.player_log_full, "r") as file:
    py_p_log: dict[str, dict[str, Any]] = json.load(file)
    file.close()

meta_start = py_p_log["meta"]["start time"][0:2]
print(meta_start)
meta_start = meta_start+"00"
meta_end = py_p_log["meta"]["end time"][0:2]
print(meta_end)
meta_end = int(meta_end + "00") + 100


# canvases with players playtime and time markers
canv_up = tk.Canvas(frame)
canv_up.pack(anchor="n", fill="both")
playtimes = tk.Canvas(frame, bg='grey', yscrollcommand=v_scrollbar.set,
                      xscrollcommand=h_scrollbar.set, scrollregion=(0, 0, meta_end, len(
        py_p_log["players"]) * conf.plog_scale_height))  # playtimes
players = tk.Canvas(frame, yscrollcommand=v_scrollbar.set, bg="grey", width=150,
                    scrollregion=(0, 0, 0, len(py_p_log["players"]) * conf.plog_scale_height))  # players
title_canvas = tk.Canvas(canv_up, height=100, width=150, bg="grey") # title
time_canvas = tk.Canvas(canv_up, height=100, bg="grey", xscrollcommand=h_scrollbar.set, scrollregion=(0, 0, meta_end, 0)) # time marks

title_canvas.pack(anchor="w", side="left", expand=False)
time_canvas.pack(anchor="e", side="right", fill="x", expand=True)
playtimes.pack(anchor="e", side="right", expand=True, fill="both")
players.pack(anchor="w", side="left", fill="y", expand=False)

# create playtime and players
num: int = 0
for player in py_p_log["players"]:
    players.create_text(10, (num * conf.plog_scale_height) + ((conf.plog_scale_height - 10) / 2 + 5), text=player,
                        justify="left", anchor="w")

    for time in py_p_log["players"][player]["playtime"]:
        on = gettime_dec(time["on"])
        of = gettime_dec(time["of"])
        on: int = on - int(meta_start)
        of: int = of - int(meta_start)
        corner_up: tuple[float, float] = (on / conf.plog_scale_width, (conf.plog_scale_height * num) + 10)
        corner_down: tuple[float, float] = (of / conf.plog_scale_width,
                                            (conf.plog_scale_height * num) + conf.plog_scale_height)
        playtimes.create_rectangle(corner_up, corner_down, fill="green", outline="blue")

    playtimes.create_line(0, conf.plog_scale_height * num + 5, 1000, conf.plog_scale_height * num + 5)
    players.create_line(0, conf.plog_scale_height * num + 5, 1000, conf.plog_scale_height * num + 5)
    num += 1

playtimes.create_line(0, conf.plog_scale_height * num + 5, 1000, conf.plog_scale_height * num + 5)
players.create_line(0, conf.plog_scale_height * num + 5, 1000, conf.plog_scale_height * num + 5)

# create time marks
start = int(meta_start)
end = int(meta_end)

print(meta_start, meta_end)
print(start, end)
for time in range(start, end, int(conf.plog_scale_width*30)):
    time = gettime_real(time)[0:4] + "0"
    text = time
    print(text)
    time = gettime_dec(time)
    time_canvas.create_text(10 + ((time-start)/conf.plog_scale_width), 40, text=text, angle=40)
    time_canvas.create_line((time-start)/conf.plog_scale_width, 60, (time-start)/conf.plog_scale_width, 100, dash=10, fill="darkgrey")
    playtimes.create_line((time - start) / conf.plog_scale_width, 0, (time - start) / conf.plog_scale_width, len(
        py_p_log["players"]) * conf.plog_scale_height + 20,
                            dash=10, fill="darkgrey", )


# create title_canvas
title_canvas.create_line(0, 0, 150, 100)
title_canvas.create_text(90, 100, text="player", anchor="s", justify="left")
title_canvas.create_text(125, 40, text="time", angle=90, anchor="e", justify="left")


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

p_log.mainloop()
