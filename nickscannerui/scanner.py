from tkcomponents import Component
from tkcomponents.extensions import GridHelper

from tkinter import Label, Button, StringVar, Entry, OptionMenu

from .constants import Constants


class Scanner(Component.with_extensions(GridHelper)):
    def __init__(self, container, config=Constants.DEFAULT_CONFIG):
        super().__init__(container)

        self._config = config

        self._item_code = StringVar()
        self._location = StringVar()
        self._action = StringVar()
        self._action_destination = StringVar()

        self._item_code.trace_add("write", lambda *args: self._validate_item_code())

        self._other_locations = self._config["locations"]

    def _render(self) -> None:
        self.children["submit"] = None

        self._frame.configure(padx=15, pady=15)

        self._apply_frame_stretch(rows=(5,), columns=(5,))
        self._apply_dividers(5, columns=(1, 3), rows=(1, 3))
        self._apply_dividers(10, columns=(5,), rows=(5,))

        location_title = Label(self._frame, text="Location", **self._config["styles"]["title"])
        location_title.grid(row=0, column=0, sticky="nswe")

        location_dropdown = OptionMenu(
            self._frame,
            self._location,
            *self._config["locations"],
            command=lambda value: self._validate_form()
        )
        location_dropdown.grid(row=0, column=2, sticky="nswe")

        item_code_title = Label(self._frame, text="Item Code", **self._config["styles"]["title"])
        item_code_title.grid(row=2, column=0, sticky="nswe")

        item_code_entry = Entry(
            self._frame,
            textvariable=self._item_code
        )
        item_code_entry.grid(row=2, column=2, sticky="nswe")

        action_title = Label(self._frame, text="Action", **self._config["styles"]["title"])
        action_title.grid(row=4, column=0, sticky="nswe")

        action_dropdown = OptionMenu(
            self._frame,
            self._action,
            *("Received", "Sent", "Disposed"),
            command=lambda value: self._validate_form()
        )
        action_dropdown.grid(row=4, column=2, sticky="nswe")

        action_connecting_label = Label(self._frame, text="to", **self._config["styles"]["title"])
        action_connecting_label.grid(row=4, column=3, sticky="nswe")

        action_destination_dropdown = OptionMenu(
            self._frame,
            self._action_destination,
            *self._other_locations,
            command=lambda value: self._validate_form()
        )
        action_destination_dropdown.grid(row=4, column=4, sticky="nswe")

        # log_title = Label(self._frame, text="Log", **self._config["styles"]["title"])  #####
        # log_title.grid(row=0, column=7, sticky="nswe")  #####

        submit_button = Button(self._frame, text="Submit", command=self._submit)
        self.children["submit"] = submit_button
        submit_button.grid(row=6, column=0, sticky="nswe")

        self._validate_form()

    def _validate_form(self):
        if (self._location.get() == "") or (self._action.get() == ""):
            self.children["submit"].config(state="disabled")
        else:
            if (self._action.get() == "Sent") and (self._action_destination.get() == ""):
                self.children["submit"].config(state="disabled")
            else:
                self.children["submit"].config(state="active")

    def _validate_item_code(self):
        result = ""

        for char in self._item_code.get():
            if char in "0123456789":
                result += char

        self._item_code.set(result)

    def _submit(self):
        pass  #####
