import json

import config as cfg

with open(cfg.style_path, "r") as read_file:
    UI_styles = json.load(read_file)

extracted_style = UI_styles["style"][cfg.style]

btns = extracted_style["buttons"]

font = ("JetBrainsMono", 12)

background = "#182827"
background_sec = "#212323"
background_hover = "#16333a"
background_disabled = "#272d2e"

foreground = "#199CA8"
foreground_sec = "#6b1b1f"
foreground_hover = "#9a2c31"
foreground_disabled = "#1f2a29"
