import json

import config as cfg

with open(cfg.style_path, "r") as read_file:
    UI_styles = json.load(read_file)

extracted_style = UI_styles["style"][cfg.style]

btns = extracted_style["buttons"]