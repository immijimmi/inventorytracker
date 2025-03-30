from barcode import UPCA
from barcode.writer import SVGWriter
from tkcomponents import Component
from tkcomponents.extensions import GridHelper

from tkinter import StringVar, Label, OptionMenu, Button
import datetime


class LabelMaker(Component.with_extensions(GridHelper)):
    def __init__(self, container, item_names, styles=None):
        super().__init__(container, styles=styles)

        styles = styles or {}
        self.styles["frame"] = styles.get("frame", {})
        self.styles["title"] = styles.get("title", {})
        self.styles["row_title"] = styles.get("row_title", {})

        self._item_names = item_names

        self._item_name = StringVar()
        self._last_generated = StringVar()

    def _render(self) -> None:
        self._frame.configure(**self.styles["frame"])

        self._apply_frame_stretch(rows=(1,), columns=(1,))
        self._apply_dividers(5, rows=(1,), columns=(1,))

        item_name_title = Label(
            self._frame,
            text="Item Name",
            **self.styles["title"],
            **self.styles["row_title"]
        )
        item_name_title.grid(row=0, column=0, sticky="nswe")

        item_name_dropdown = OptionMenu(
            self._frame,
            self._item_name,
            *self._item_names,
            command=lambda value: self._validate_form()
        )
        item_name_dropdown.grid(row=0, column=2, sticky="nswe")

        generate_button = Button(self._frame, text="Generate Label", command=self._generate_barcode)
        self.children["generate_button"] = generate_button
        generate_button.grid(row=2, column=0, sticky="nswe")

        last_generated_label = Label(
            self._frame,
            textvariable=self._last_generated,
        )
        last_generated_label.grid(row=2, column=2, sticky="nswe")

        self._validate_form()

    def _validate_form(self):
        checks = []

        checks.append(
            "" not in (self._item_name.get(),)
        )  # Necessary fields are not blank

        if all(checks):
            self.children["generate_button"].config(state="active")
        else:
            self.children["generate_button"].config(state="disabled")

    def _generate_barcode(self):
        """
        The approach used to generate barcodes in this method may run into sync conflicts due to
        writing to a single shared csv file regardless of location, if new barcodes are generated from
        multiple separate machines in a short span of time
        """

        """
        For UPCA barcodes, this ID number will have a 0 added to the front for EAN compatibility,
        and a checksum digit added to the end for a total of 13 digits
        """
        barcode_id_len = 11

        csv_filename = "Inventory Barcodes.csv"
        try:  # Get last barcode entry from file
            with open(csv_filename, "r") as csv_file:
                lines = csv_file.read().splitlines()
                csv_exists = True
        except FileNotFoundError:  # Make a new file with headers if one does not exist
            csv_exists = False

        if csv_exists:
            try:
                # Creating new barcode by incrementing barcode retrieved from CSV
                last_line = lines[-1] if lines else ""
                last_barcode = last_line.split(",")[1].lstrip("#")
                # Stripping the EAN compat/checksum digits off the previous barcode
                last_barcode_id = last_barcode[1:barcode_id_len+1]
                assert len(last_barcode_id) == barcode_id_len

                new_barcode_id = f"{int(last_barcode_id)+1:0>{barcode_id_len}}"

            except Exception as ex:
                self._last_generated.set(f"Failed to generate barcode: {ex}")
                return
        else:
            new_barcode_id = "0"*barcode_id_len

        new_barcode_obj = UPCA(new_barcode_id, make_ean=True, writer=SVGWriter())
        row = [
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "#" + str(new_barcode_obj),
            self._item_name.get()
        ]
        row_csv_str = ",".join(row) + "\n"

        with open(csv_filename, "a") as csv_file:
            if not csv_exists:
                csv_file.write("Datetime,Item Code,Item Name\n")
            csv_file.write(row_csv_str)

        svg_filename = f"Barcode #{new_barcode_obj}.svg"
        with open(svg_filename, "wb") as svg_file:
            new_barcode_obj.write(svg_file)

        self._last_generated.set(f"Generated #{new_barcode_obj}")
