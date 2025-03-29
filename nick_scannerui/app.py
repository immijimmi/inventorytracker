from tkinter import Tk
from json import loads

from .constants import Constants
from .scanner import Scanner


class App:
    def __init__(self):
        config = Constants.DEFAULT_CONFIG

        # Attempting to load custom config
        try:
            with open("config.json", "r") as config_file:
                custom_config = loads(config_file.read())
        except FileNotFoundError:
            custom_config = {}

        # Applying custom config
        for config_key in custom_config:
            config[config_key] = custom_config[config_key]

        self._window = Tk()
        self._window.resizable(False, False)
        self._window.minsize(width=200, height=0)  # Min width so that the window remains grabbable using the cursor
        self._window.title(Constants.WINDOW_TITLE)

        # Make the window expand to fit displayed content
        self._window.columnconfigure(0, weight=1)
        self._window.rowconfigure(0, weight=1)

        s = Scanner(self._window, config=config)
        s.render().grid(sticky="nswe")

        self._window.mainloop()
