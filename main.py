#!/usr/bin/env python3
import json
from datetime import datetime
from time import sleep

import API
import GUI
import config as conf
import desktop_message

api_p_log = API.Players([])

def loop_main(interval: int, update_ratio: int) -> None:
    GUI.update_stream()
    api_p_log.update_log()
    for i in range(update_ratio):
        GUI.root.update()
        sleep(interval / update_ratio)
        if not GUI.run:
            return None
    return None


if __name__ == '__main__':
    desktop_message.simple("BBSWM", "Starting BBSWM")
    API.Message(API.TYPE["start"])
    API.Players.update_log(api_p_log)
    while GUI.run:
        loop_main(10, 600)

    try:
        open(conf.player_log_full, "x")
    except FileExistsError:
        with open(conf.player_log_full) as f:
            end = json.load(f)
            end["meta"]["end time"] = datetime.now().time().isoformat(timespec="seconds")
            json.dump(end, open(conf.player_log_full, "w"), indent=2)
            f.close()
    API.Players.close_log(api_p_log)

    desktop_message.simple("BBSWM", "Closed BBSWM")
    API.Message(API.TYPE["quit"])
