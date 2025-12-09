import os
import json
from datetime import datetime
import config as conf

def norm_log():
    print(f"\x1B[33;1m[warn]:    could not find log file, trying to create it.\x1B[0m")
    try: os.mkdir(conf.log_path)
    except FileExistsError:
        print(f"[info]:    found log directory at {conf.log_path}")
    try:
        print("hi")
        open(conf.log_full, "x").write("<style>\n"
                                       "severe { color: red }\n"
                                       "warn { color: yellow }\n"
                                       "message { color: white }\n"
                                       "</style>\n")
        open(conf.log_full).close()
        print(f"[info]:    successfully created log file at {conf.log_full}")
        with open(conf.log_full, "a") as f:
            f.write(
                f"<message>[{datetime.now().time().isoformat(timespec="seconds")}][info]:    " +
                f"successfully created log file at {conf.log_full}</message>{"\n" * 2}")
            f.close()
    except FileExistsError:
        print(f"[info]:    found log file at {conf.log_full}")
        with open(conf.log_full, "a") as f:
            f.write(
                f"<message>[{datetime.now().time().isoformat(timespec="seconds")}][info]:    " +
                f"found log file at {conf.log_full}</message>{"\n" * 2}")
            f.close()

def player_log():
    try:
        os.mkdir(conf.player_log_path)
        print(f"[info]:    successfully created player log directory at {conf.player_log_path}")
    except FileExistsError:
        print(f"[info]:    found log directory at {conf.player_log_path}")

    try:
        open(conf.player_log_full, "x")
        init = {"meta": {"start time": datetime.now().time().isoformat(timespec="seconds")},
                "players": {}}
        json.dump(init, open(conf.player_log_full, "w"))
        open(conf.player_log_full).close()
        print(f"[info]:    successfully created player log file at {conf.player_log_full}")
        try:
            with open(conf.log_full, "a") as f:
                f.write(
                    f"<message>[{datetime.now().time().isoformat(timespec="seconds")}][info]:    " +
                    f"successfully created player log file at {conf.player_log_full}</message>{"\n" * 2}")
                f.close()
        except FileNotFoundError:
            pass

    except FileExistsError:
        print(f"[info]:    found log file at {conf.player_log_full}")
        try:
            with open(conf.log_full, "a") as f:
                f.write(
                    f"<message>[{datetime.now().time().isoformat(timespec="seconds")}][info]:    " +
                    f"found player log file at {conf.player_log_full}</message>{"\n" * 2}")
                f.close()
        except FileNotFoundError:
            pass
