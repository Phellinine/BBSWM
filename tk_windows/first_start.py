import json
import tkinter as tk
from tkinter import ttk
from typing import Any


def build(window: tk.Tk) -> None:
    """
    takes a window and creates a setup gui for setting up the settings for first startup or if a new version requires new settings
    :param window: a tk instance to create the settup GUI
    :return: None
    """
    config: dict[str, Any] = {"exaroton": {"api_token": "Exaroton API token",
                                           "server_id": "Exaroton server SERVER_ID"
                                           },
                              "nextcloud": {"user_id": "Nextcloud user SERVER_ID",
                                            "password": "Nextcloud password",
                                            "server_adress": "Nextcloud server adress",
                                            "data_path": "Nextcloud data path",
                                            },
                              "general": {"meta": {"settings_version": "0.1"
                                                   },
                                          "p_log_vis_opt": {"scale_width": 0.1, "scale_height": 50
                                                        },
                                          "gui_opt": {"stream_names": [('Global', '0'),
                                                                       ('All', '1'),
                                                                       ("Warn", "2"),
                                                                       ("Error", "3"),
                                                                       ("chats", "4"),
                                                                       ("experiment2", "5")
                                                                       ],
                                                      "stream_options": {"0": "[Global]",
                                                                         "1": "",
                                                                         "2": "/WARN",
                                                                         "3": "/ERROR",
                                                                         "4": ["[Server thread/INFO]", "issued server command", "chat",   "-[Server thread/INFO]: ", "-issued server command"],
                                                                         "5": ["![Server"]
                                                                         }
                                                      }
                                  }
                              }

    def save() -> None:
        """
        save the settings to a JSON file
        :return: None
        """
        with open("./configs/settings.json", "w") as file:
            json.dump(config, file, indent=2)

    steps:int = 2
    def clear_window(window_instance: tk.Tk) -> None:
        """
        clear the window instance
        :param window_instance: tk instance to clear
        :return: None
        """
        for widget in window_instance.winfo_children():
            widget.destroy()

    def navigation(window_instance: tk.Tk, step_no: int, prev = None) -> ttk.Frame:
        """
        creates a basic structure to navigate through the setup
        :param window_instance: tk instance to create navigation for
        :param step_no: index of the step you are at
        :param prev: function for the previous step, if empty back button will be deactivated
        :return: a ttk Frame where content can be displayed
        """
        def back():
            clear_window(window_instance)
            prev(window_instance)

        def forward():
            clear_window(window_instance)
            window_instance.quit()

        top_info = ttk.Frame(window_instance)
        main_content = ttk.Frame(window_instance)

        top_info.pack(side="top", fill="x")

        nav = ttk.Frame(top_info)

        back_arrow = ttk.Button(nav, text="Back", command=back)
        step_display = ttk.Label(top_info, text=f"{step_no} / {steps}")
        forward_arrow = ttk.Button(nav, text="Forward", command=forward)

        if prev is None:
            back_arrow.config(state="disabled")

        back_arrow.pack(side="left")
        forward_arrow.pack(side="right")

        step_display.pack(side="top")
        nav.pack(side="bottom", fill="x")

        return main_content

    def step_1(window_instance: tk.Tk) -> None:
        """
        creates the first step of the setup, exaroton configuration
        :param window_instance: tk instance to create the step
        :return: None
        """
        content_frame: ttk.Frame = navigation(window_instance, 1)

        exaroton_api_key = tk.Variable(window_instance, value=config["exaroton"]["api_token"])
        axaroton_server_id = tk.Variable(window_instance, value=config["exaroton"]["server_id"])

        explanation = ttk.Label(content_frame,
                                 text="Please input your Exaroton details."
                                      " Your API token and the server SERVER_ID of the server you want to track",
                                 wraplength=700, justify="center")
        explanation1 = ttk.Label(content_frame,
                                 text="'Exaroton API token': you get this token in your account settings",
                                 wraplength=400, justify="center")
        explanation2 = ttk.Label(content_frame,
                                 text="'Exaroton server SERVER_ID': the server SERVER_ID is the string under your server name "
                                      "with the '#'. don't copy the '#'.",
                                 wraplength=400, justify="center")

        exaroton_api_key_input = ttk.Entry(content_frame, width=20, textvariable=exaroton_api_key)
        exaroton_server_id_input = ttk.Entry(content_frame, width=20, textvariable=axaroton_server_id)

        explanation.pack(anchor="center", pady=10, padx=10)
        explanation1.pack(anchor="center", pady=10, padx=10)
        exaroton_api_key_input.pack(anchor="center", pady=10, padx=10)
        explanation2.pack(anchor="center", pady=10, padx=10)
        exaroton_server_id_input.pack(anchor="center", pady=10, padx=10)

        content_frame.pack(expand=True, fill="both")
        window_instance.mainloop()

        config["exaroton"]["api_token"] = exaroton_api_key.get()
        config["exaroton"]["server_id"] = axaroton_server_id.get()

        step_2(window_instance)

    def step_2(window_instance: tk.Tk):
        """
        creates the second step of the setup, nextcloud configuration
        :param window_instance: tk instance to create the step
        :return: None
        """
        content_frame: ttk.Frame = navigation(window_instance, 2, prev=step_1)

        nextcloud_user_id = tk.Variable(window_instance, value=config["nextcloud"]["user_id"])
        nextcloud_password = tk.Variable(window_instance, value=config["nextcloud"]["password"])
        nextcloud_server_adress = tk.Variable(window_instance, value=config["nextcloud"]["server_adress"])
        nextcloud_path = tk.Variable(window_instance, value=config["nextcloud"]["data_path"])

        explanation = ttk.Label(content_frame,
                                 text="Please input your Nextcloud details.",
                                 wraplength=700, justify="center")
        explanation1 = ttk.Label(content_frame,
                                 text="'User SERVER_ID': you get the id as the first field "
                                      "when creating a new Nextcloud app Password in the security settings",
                                 wraplength=400, justify="center")
        explanation2 = ttk.Label(content_frame,
                                 text="'Password': you get the password as the second field.",
                                 wraplength=400, justify="center")
        explanation3 = ttk.Label(content_frame,
                                 text="'Server Adress': you get the server adress in the address line of your browser "
                                      "when accessing the nextcloud. "
                                      "you dont need things after the first slash: "
                                      "https://address.com/'you dont need this'.",
                                 wraplength=400, justify="center")
        explanation4 = ttk.Label(content_frame,
                                 text="'File Path': the file path where you want to remotely store log files, "
                                      "probably a shared folder. "
                                      "The path should be something like this: './minecraft_server/log_files'",
                                 wraplength=400, justify="center")

        nextcloud_user_id_input = ttk.Entry(content_frame, width=20, textvariable=nextcloud_user_id)
        nextcloud_password_input = ttk.Entry(content_frame, width=20, textvariable=nextcloud_password)
        nextcloud_server_adress_input = ttk.Entry(content_frame, width=20, textvariable=nextcloud_server_adress)
        exaroton_data_path_input = ttk.Entry(content_frame, width=20, textvariable=nextcloud_path)

        explanation.pack(anchor="center", pady=10, padx=10)

        explanation1.pack(anchor="center", pady=10, padx=10)
        nextcloud_user_id_input.pack(anchor="center", pady=10, padx=10)

        explanation2.pack(anchor="center", pady=10, padx=10)
        nextcloud_password_input.pack(anchor="center", pady=10, padx=10)

        explanation3.pack(anchor="center", pady=10, padx=10)
        nextcloud_server_adress_input.pack(anchor="center", pady=10, padx=10)

        explanation4.pack(anchor="center", pady=10, padx=10)
        exaroton_data_path_input.pack(anchor="center", pady=10, padx=10)

        content_frame.pack(expand=True, fill="both")
        window_instance.mainloop()


        config["nextcloud"]["user_id"] = nextcloud_user_id.get()
        config["nextcloud"]["password"] = nextcloud_password.get()
        config["nextcloud"]["server_adress"] = nextcloud_server_adress.get()
        config["nextcloud"]["data_path"] = nextcloud_path.get()

        save()

    step_1(window)
    window.destroy()
