from tkcomponents import Component
from tkcomponents.extensions import GridHelper

from tkinter import Label, Button, StringVar, Entry, OptionMenu, Text, END
import datetime

from .constants import Constants


class Scanner(Component.with_extensions(GridHelper)):
    def __init__(self, container, config=Constants.DEFAULT_CONFIG):
        super().__init__(container)

        self._config = config

        self._item_code = StringVar()
        self._location = StringVar()
        self._action = StringVar()
        self._action_destination = StringVar()
        self._submit_log = StringVar()

        self._item_code.trace_add("write", lambda *args: self._validate_item_code())
        self._submit_log.trace_add("write", lambda *args: self._update_submit_log())

    def _render(self) -> None:
        self.children["submit_log_text"] = None
        self.children["submit_button"] = None

        self._frame.configure(padx=12, pady=12)

        self._apply_frame_stretch(rows=(5,), columns=(5,))
        self._apply_dividers(5, columns=(1, 3), rows=(1, 3))
        self._apply_dividers(10, columns=(5,), rows=(5,))

        location_title = Label(
            self._frame,
            text="Location",
            **self._config["styles"]["title"],
            **self._config["styles"]["row_title"]
        )
        location_title.grid(row=0, column=0, sticky="nswe")

        location_dropdown = OptionMenu(
            self._frame,
            self._location,
            *self._config["locations"],
            command=lambda value: self._validate_form()
        )
        location_dropdown.grid(row=0, column=2, sticky="nswe")

        item_code_title = Label(
            self._frame,
            text="Item Code",
            **self._config["styles"]["title"],
            **self._config["styles"]["row_title"]
        )
        item_code_title.grid(row=2, column=0, sticky="nswe")

        item_code_entry = Entry(
            self._frame,
            textvariable=self._item_code
        )
        item_code_entry.grid(row=2, column=2, sticky="nswe")

        action_title = Label(
            self._frame,
            text="Action",
            **self._config["styles"]["title"],
            **self._config["styles"]["row_title"]
        )
        action_title.grid(row=4, column=0, sticky="nswe")

        action_dropdown = OptionMenu(
            self._frame,
            self._action,
            *("Received", "Sent", "Disposed"),
            command=lambda value: self.render()
        )
        action_dropdown.grid(row=4, column=2, sticky="nswe")

        if self._action.get() == "Sent":
            action_connecting_label = Label(self._frame, text="to", **self._config["styles"]["title"])
            action_connecting_label.grid(row=4, column=3, sticky="nswe")

            action_destination_dropdown = OptionMenu(
                self._frame,
                self._action_destination,
                *self._config["locations"],
                command=lambda value: self._validate_form()
            )
            action_destination_dropdown.grid(row=4, column=4, sticky="nswe")

        submit_log_title = Label(self._frame, text="Log", **self._config["styles"]["title"])
        submit_log_title.grid(row=0, column=7, sticky="nswe")

        submit_log_text = Text(self._frame, width=75, height=10)
        submit_log_text.grid(row=2, column=7, rowspan=5, sticky="nswe")
        self.children["submit_log_text"] = submit_log_text
        self._update_submit_log()

        submit_button = Button(self._frame, text="Submit", command=self._submit)
        self.children["submit_button"] = submit_button
        submit_button.grid(row=6, column=0, sticky="nswe")

        self._validate_form()

    def _validate_form(self):
        checks = []

        checks.append(
            "" not in (self._location.get(), self._action.get(), self._item_code.get())
        )  # Necessary fields are not blank
        checks.append(
            not ((self._action.get() == "Sent") and (self._action_destination.get() == ""))
        )  # Not sending to a blank destination
        checks.append(
            not (
                    (self._action.get() == "Sent") and (self._action_destination.get() == self._location.get())
            )
        )  # Not sending to current location

        if all(checks):
            self.children["submit_button"].config(state="active")
        else:
            self.children["submit_button"].config(state="disabled")

    def _validate_item_code(self):
        old_value = self._item_code.get()
        result = ""

        for char in old_value:
            if char in "0123456789":
                result += char

        self._item_code.set(result)
        self._validate_form()

    def _update_submit_log(self):
        self.children["submit_log_text"].config(state="normal")

        self.children["submit_log_text"].delete(1.0, END)
        self.children["submit_log_text"].insert(END, self._submit_log.get())

        self.children["submit_log_text"].config(state="disabled")

    def _submit(self):
        if self._action.get() == "Sent":
            action_destination = self._action_destination.get()
        else:
            action_destination = ""

        row = [
            datetime.datetime.now().isoformat(),
            self._location.get(),
            "#"+self._item_code.get(),  # Hash symbol added to stop excel converting the number to scientific notation
            self._action.get(),
            action_destination
        ]
        row_csv_str = ",".join(row) + "\n"

        csv_filename = f"{Constants.APP_NAME} Log - {self._location.get()}.csv"
        try:  # First attempt to append to an existing file
            with open(csv_filename, "r") as csv_file:
                csv_exists = True
        except FileNotFoundError:  # Make a new file with headers if one does not exist
            csv_exists = False

        with open(csv_filename, "a") as csv_file:
            if not csv_exists:
                csv_file.write("Datetime,Location,Item Code,Action,Sent To\n")
            csv_file.write(row_csv_str)

        self._item_code.set("")
        self._submit_log.set(self._submit_log.get() + row_csv_str)
