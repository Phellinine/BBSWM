#!/usr/bin/env python3
import threading

import API
import desktop_message
import main_window

api_p_log = API.Players([])
threads: list[threading.Thread] = []
stop: threading.Event = threading.Event()


def thread_add(func, *args, **kwargs):
    global threads
    thr = threading.Thread(target=func, args=args, kwargs=kwargs)
    threads.append(thr)

def run_threads():
    global threads
    for thread in threads:
        thread.start()
    desktop_message.simple("BBSWM", "started all threads")

def add_single_thread(func, *args, **kwargs):
    global threads
    threading.Thread(target=func, args=args, kwargs=kwargs).start()
    threads.append(threading.Thread(target=func, args=args, kwargs=kwargs))


if __name__ == '__main__':
    desktop_message.simple("BBSWM", "Started BBSWM")

    main_window = main_window.build()
    thread_add(API.player_log_updater, stop)

    # Start each thread after 1 second
    main_window.after(1000, run_threads)
    main_window.mainloop()

    stop.set()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    desktop_message.simple("BBSWM", "Closed BBSWM")
