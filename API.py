import json
import traceback
from datetime import datetime
from threading import Event
from time import sleep
from typing import Any

from exaroton import Exaroton

import config as conf
import desktop_message
from old import init as ini
from configs import settings as settings

exaroton_api_token = settings.get_val(["exaroton", "api_token"])
EXA = Exaroton(exaroton_api_token)
SERVER_ID = settings.get_val(["exaroton", "server_id"])
print(SERVER_ID, exaroton_api_token)


class Mitype:
    """
    class for defining errors with type and message
    """

    def __init__(self, message: str, importance: int) -> None:
        self.type = message
        self.imp = importance


TYPE: dict[str, Mitype] = {"": Mitype("test", 0),
                           "server_response": Mitype(
                               """server did not respond correctly, probably starting/stoping. Wait. 
                               if error stays contact Admin.""",
                               1),
                           "log_file_done": Mitype(
                               f'Successfully created log file at {conf.log_full}',
                               3),
                           "int_fail": Mitype(
                               'internal error',
                               2),
                           "file_not_found": Mitype(
                               "File missing. Programm will still work.",
                               1),
                           "nextcloud_error": Mitype(
                               f"Upload of player logs failed! Upload log file from {conf.player_log_full} manually to nextcloud {conf.nc_path} !",
                               0),
                           "quit": Mitype(
                               "BBSWM was closed.",
                               3),
                           "player_log_file_done": Mitype(
                               f"Successfully created player log file at {conf.player_log_file}",
                               3),
                           "start": Mitype(
                               "Succesfully startet BBSWM.",
                               3),
                           "log_file_exists": Mitype(
                               f"Found log file at {conf.log_full}",
                               3),
                           "p_log_file_exists": Mitype(
                               f"Found player log file at {conf.player_log_full}",
                               3),
                           "p_log_file_missing": Mitype(
                               "could not find player log file, trying to create it.",
                               1)}


class Message:
    """
    can create different types of error messages from MITYPE
    """

    def __init__(self, error_type: Mitype) -> None:
        self.type = error_type
        self.error_description = error_type.type
        self.severe = error_type.imp
        self.send()

    csi = '\x1B['
    red = csi + '31;1m'
    yellow = csi + '33;1m'
    end = csi + '0m'
    md_severe = "<severe>"
    md_severe_end = "</severe>"
    md_warn = "<warn>"
    md_warn_end = "</warn>"
    md_message = "<message>"
    md_message_end = "</message>"
    timestamp = "[" + datetime.now().time().isoformat(timespec="seconds") + "]"

    def fatal(self) -> None:
        """
        Fatal Error
        impacting stability
        will write in red to log file
        :return: None
        """

        print(f"{self.red}[fatal]:    {self.error_description}{self.end}")

        # try:
        with open(conf.log_full, "a") as f:
            f.write(
                f"{self.md_severe}{self.timestamp} [fatal]:    " +
                f"{self.error_description}{self.md_severe_end}{"\n" * 2}")
            f.write(f"{traceback.format_exc()}{"\n" * 2}")
            f.close()


    def warning(self) -> None:
        """
        Warning Error
        impacting function of certain functions, not fatal
        will write in yellow to log file
        :return: None
        """

        print(f"{self.yellow}[warn]:    {self.error_description}{self.end}")

        # try:
        with open(conf.log_full, "a") as f:
            f.write(
                f"{self.md_warn}{self.timestamp} [warn]:    {self.error_description}{self.md_warn_end}{"\n" * 2}")
            f.write(f"{self.md_message}{traceback.format_exc(limit=4)}{self.md_message_end}{"\n" * 2}")
            f.close()


    def weak_warning(self) -> None:
        """
        Weak Warning Error
        impacting certain function but not overall function, for debugging only
        will only print
        :return: None
        """
        print(f"{self.yellow}[weak]:    {self.error_description}{self.end}")
        print(traceback.format_exc())

    def message(self) -> None:
        """
        Message
        information on state of the programm
        will write in white to log file
        :return: None
        """

        print(f"[info]:    {self.error_description}")

        # try:
        with open(conf.log_full, "a") as f:
            f.write(
                f"{self.md_message}{self.timestamp}[info]:    " +
                f"{self.error_description}{self.md_message_end}{"\n" * 2}")
            f.close()


    def send(self) -> None:
        try:
            open(conf.log_full, "r")
        except IOError:
            ini.norm_log()
        if self.severe == 0:
            self.fatal()
        elif self.severe == 1:
            self.warning()
        elif self.severe == 2:
            self.weak_warning()
        else:
            self.message()


class Console:
    def __init__(self, hist: list[str], arg: str | list[str]) -> None:

        self.hist = hist
        self.arg = arg

        self.console_part()
        self.get()

    def console_part(self) -> list[str]:
        try:
            console = (EXA.get_server_logs(SERVER_ID))  # get server logs
            console = console.splitlines()
            console = [item for item in console if item not in self.hist]  # remove history from console
        except TypeError:
            Message(TYPE["server_response"])
            console = [""]
        except AttributeError:
            Message(TYPE["server_response"])
            raise ConnectionError

        filtered = []
        if type(self.arg) == list:
            # - + !
            filtered = console
            for action in self.arg:
                if action[:1] == "-":
                    replaced: list[str] = []
                    for line in filtered:
                        replaced.append(line.replace(action[1:], "", 1))
                    filtered = replaced

                elif action[:1] == "+":
                    pass

                elif action[:1] == "!":
                    filtered = [line for line in filtered if action[1:] not in line]

                else:
                    filtered = [line for line in filtered if action in line]

            return filtered

        else:
            for line in console:
                if self.arg in line[:50]:  # check for keyword
                    filtered.append(line)
            return filtered

    def get(self):
        return self.console_part()  # get the new part of the console

    def update_hist(self) -> None:
        try:
            hist = EXA.get_server_logs(SERVER_ID).splitlines()
        except (TypeError, AttributeError):
            Message(TYPE["server_response"])
            raise ConnectionError
        self.hist = hist
        return None


class Players:
    def __init__(self, hist: list[str]) -> None:
        self.hist = hist

    def update_log(self):
        player_list = EXA.get_server(SERVER_ID).players.list
        new_players = [player for player in player_list if player not in self.hist]
        gone_players = [player for player in self.hist if player not in player_list]
        self.hist = player_list
        time: str = datetime.now().time().isoformat(timespec="seconds")
        try:
            with open(conf.player_log_full, mode="r") as file:
                json_p_log: dict[str, Any] = json.load(file)
                file.close()
        except FileNotFoundError:
            Message(TYPE["p_log_file_missing"])
            ini.player_log()
            with open(conf.player_log_full, mode="r") as file:
                json_p_log: dict[str, Any] = json.load(file)
                file.close()

        for player in new_players:
            if player in json_p_log["players"]:
                json_p_log["players"][player]["playtime"].append({'on': time})
            else:
                json_p_log["players"][player] = {"playtime": [{'on': time}]}

        for player in gone_players:
            json_p_log["players"][player]["playtime"][-1]["of"] = time

        with open(conf.player_log_full, "w") as file:
            json.dump(json_p_log, file, indent=2)
            file.close()

    def close_log(self):
        try:
            with open(conf.player_log_full, mode="r") as file:
                json_p_log: dict[str, Any] = json.load(file)
                file.close()
        except FileNotFoundError:
            Message(TYPE["p_log_file_missing"])
            ini.player_log()
            with open(conf.player_log_full, mode="r") as file:
                json_p_log: dict[str, Any] = json.load(file)
                file.close()
        time: str = datetime.now().time().isoformat(timespec="seconds")
        gone_players = [player for player in self.hist]
        for player in gone_players:
            json_p_log["players"][player]["playtime"][-1]["of"] = time

        json_p_log["meta"]["end time"] = time
        with open(conf.player_log_full, "w") as file:
            json.dump(json_p_log, file, indent=2)
            file.close()

def close_server() -> None:
    def branch_if_stopped() -> bool:
        if EXA.get_server(SERVER_ID).status == "Offline":
            return True
        else:
            return False

    if branch_if_stopped(): return
    #statii = ('0: "Offline", 1: "Online", 2: "Starting", 3: "Stopping", 4: "Restarting", 5: "Saving", 6: "Loading", '
    #          '7: "Crashed", 8: "Pending", 10: "Preparing",')
    EXA.command(SERVER_ID, 'title @a subtitle {"text":"Server wird in 5 min gestoppt","color":"red"}')
    EXA.command(SERVER_ID, 'title @a title {"text":"Server Stopp","color":"dark_red"}')
    sleep(60*3)
    if branch_if_stopped(): return
    EXA.command(SERVER_ID, 'title @a subtitle {"text":"Server wird in 2 min gestoppt","color":"red"}')
    EXA.command(SERVER_ID, 'title @a title {"text":".","color":"dark_red"}')
    sleep(60*2)
    if branch_if_stopped(): return
    EXA.command(SERVER_ID, 'kick @a Der Server wurde gestoppt')
    EXA.stop(SERVER_ID)
    server_done = False
    while not server_done:
        sleep(5)
        status = EXA.get_server(SERVER_ID).status
        if status == "Offline":
            server_done = True
        elif status == "Online":
            EXA.stop(SERVER_ID)
        else:
            pass
        sleep(5)

    return

def player_log_updater(stop_event: Event) -> None:
    players = Players([])
    retry = 0
    max_retrys = 5
    while not stop_event.is_set():
        try:
            EXA.command(SERVER_ID, 'player log')
        except ConnectionError:
            retry += 1
        players.update_log()
        sleep(10)

    players.close_log()
    desktop_message.simple("BBSWM", "closed player log")
