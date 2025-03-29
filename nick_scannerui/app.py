from tkinter import Tk
from json import loads, dumps

from .constants import Constants
from .scanner import Scanner


class App:
    def __init__(self):
        # Attempting to load config file
        try:
            with open("config.json", "r") as config_file:
                config = loads(config_file.read())
        # No config file found
        except FileNotFoundError:
            config = Constants.DEFAULT_CONFIG
            # Create new config file and write the default config to it for convenience
            with open("config.json", "w") as config_file:
                config_file.write(dumps(config))

        self._window = Tk()
        self._window.resizable(False, False)
        self._window.minsize(width=200, height=0)  # Min width so that the window remains grabbable using the cursor
        self._window.title(Constants.APP_NAME)

        # Make the window expand to fit displayed content
        self._window.columnconfigure(0, weight=1)
        self._window.rowconfigure(0, weight=1)

        s = Scanner(self._window, config=config)
        s.render().grid(sticky="nswe")

        self._window.mainloop()
