import datetime
import tkinter as tk
from tkinter import ttk

import nextcloud_client
from nextcloud_client import HTTPResponseError

import API
import config

x = '1000'
y = '500'
space_x = "-1000"
space_y = "+100"

# create window
root = tk.Tk()
root.title("BBSWM -- Start")  # -B-lock für -B-lock -S-erver -W-ork -M-anager
root.geometry(x + 'x' + y + space_x + space_y)

stream_options = [('Global', '[Global]'),
                  ('All', '')]

# def main_window():
stream = API.Console([""], "[")
cons = tk.Text
autoscroll = tk.Variable(value="1")

player_log_file = datetime.date.today().isoformat() + ".json"
player_log_path = "old/player_logs/"
player_log_full = player_log_path + player_log_file
NC = nextcloud_client.Client('https://gmb-cloud.wiesan.de')
nc_path = "./Minecraft mit detti/server player logs/"
run = True


def usr_quit():
    global run
    try:
        NC.login("72361402", "mbJHD-c3WEM-3LAQC-LJTzi-F3WWf")
        if player_log_file in [ds.name for ds in NC.list(path=nc_path, properties="path")]:
            print("hii")
    except HTTPResponseError:
        API.Message(API.TYPE["nextcloud_error"])
    run = False
    root.quit()


def get_stream() -> str:
    global stream
    out = ""
    for line in stream.get():
        out += "\n" + line
    stream.update_hist()
    return out


def update_stream():
    global cons
    global autoscroll
    try:
        cons['state'] = 'normal'
        cons.insert(tk.END, get_stream())
        if autoscroll.get() == "1":
            cons.see(tk.END)
        cons['state'] = 'disabled'
    except tk.TclError:
        API.Message(API.TYPE["int_fail"])
    except ConnectionError:
        cons['state'] = 'normal'
        cons.delete('1.0', tk.END)
        cons.insert(tk.END,
                    "Server didn't respond correctly. Probably starting/stopping. Wait. If error stays contact admin.")
        cons['state'] = 'disabled'
    root.update()


def change_stream(selected):
    global stream
    global cons
    cons['state'] = 'normal'
    cons.delete('1.0', tk.END)
    cons['state'] = 'disabled'
    stream = API.Console([""], selected.get())
    update_stream()


# app-icon
try:
    photo = tk.PhotoImage(file=config.icon_path)
    root.iconphoto(False, photo)
except tk.TclError:
    API.Message(API.TYPE["file_not_found"])

# left frame
left_frame = tk.Frame(root)
left_frame.pack(side="left", fill="both", expand=False, padx=20)

ttk.Label(left_frame, text="Streams").pack(pady=20)

# create radio buttons for streams
selected_stream = tk.StringVar()
for option in stream_options:
    r = ttk.Radiobutton(
        left_frame,
        text=option[0],
        value=option[1],
        variable=selected_stream
    )
    r.pack(fill='x', padx=5, pady=5)

# create update button
ttk.Button(left_frame, text="Update", command=lambda: change_stream(selected_stream)).pack(pady=20)
# create auto scroll button
ttk.Checkbutton(
    left_frame,
    text="Auto Scroll",
    variable=autoscroll
).pack(pady=10)
# create quit button
ttk.Button(left_frame, text="Quit", command=usr_quit).pack(side="bottom", pady=20)

# create a vertical separator
separator = ttk.Separator(root, orient="vertical")
separator.pack(side="left", fill="y", pady=5)

# right frame
right_frame = tk.Frame(root)
right_frame.pack(side="right", fill="both", expand=True)
ttk.Label(right_frame, text="Stream output").pack(pady=20)

# create text with scrollbar
v_scrollbar = ttk.Scrollbar(right_frame)
v_scrollbar.pack(side="right", fill="y")
cons = tk.Text(right_frame, yscrollcommand=v_scrollbar.set, state="disabled")
cons.pack(expand=True, fill="both")
v_scrollbar.config(command=cons.yview)
