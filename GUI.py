import datetime
import tkinter as tk
from tkinter import ttk

import nextcloud_client
from nextcloud_client import HTTPResponseError

import API
import config
from configs import UI_style as Cfg_style

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

font = ("JetBrainsMono", 12)

background = "#182827"
background_sec = "#212323"
background_hover = "#16333a"
background_disabled = "#272d2e"
foreground = "#199CA8"
foreground_sec = "#6b1b1f"
foreground_hover = "#9a2c31"
foreground_disabled = "#1f2a29"

style = ttk.Style()
style.map("TButton", background=[("active", background_hover),("pressed", "#ffffff")], foreground=[("active", foreground_hover),("pressed", "#ffffff")],)
style.configure(style="TButton", relief="flat", background=background_sec, font=Cfg_style.btns["font"], foreground=foreground)

style.configure("TLabel", background=background, foreground=foreground, font=font)

style.configure("TFrame", background=background, foreground=foreground)

style.configure("TScrollbar", background=background_sec, foreground=foreground, relief="flat")
style.map("TScrollbar", background=[("active", background_hover), ("disabled", background_disabled)])

style.map("TRadiobutton", background=[("active", background_hover),("pressed", "#ffffff")], foreground=[("active", foreground_hover),("pressed", "#ffffff")])
style.configure("TRadiobutton", background=background_sec, foreground=foreground, font=font, borderwidth=0, padding=2)

style.map("TCheckbutton", background=[("active", background_hover),("pressed", "#ffffff")], foreground=[("active", foreground_hover),("pressed", "#ffffff")])
style.configure("TCheckbutton", background=background_sec, foreground=foreground, font=font, borderwidth=0, padding=2)

style.configure("TLabelframe", background=background, foreground=foreground, labelmargins=5, borderwidth=2, bordercolor=foreground_sec)
style.configure("TLabelframe.Label", font=font, background=background, foreground=foreground)


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

main_frame = ttk.Frame(root)
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
separator = ttk.Separator(main_frame, orient="vertical")
separator.pack(side="left", fill="y", pady=10)

# right frame
right_frame = ttk.Frame(main_frame)
right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
ttk.Label(right_frame, text="Stream output").pack(pady=20)

# create text with scrollbar
v_scrollbar = ttk.Scrollbar(right_frame)
v_scrollbar.pack(side="right", fill="y")
cons = tk.Text(right_frame, yscrollcommand=v_scrollbar.set, state="disabled", font=font, background=background_sec, foreground=foreground_sec, relief="flat", selectbackground=background_hover, selectforeground=foreground_hover)
cons.pack(expand=True, fill="both")
v_scrollbar.config(command=cons.yview)
