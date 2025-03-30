from tkcomponents import Component
from tkcomponents.extensions import GridHelper

from .constants import Constants
from .components import Scanner, LabelMaker


class Tracker(Component.with_extensions(GridHelper)):
    def __init__(self, container, config=Constants.DEFAULT_CONFIG):
        super().__init__(container)

        self._config = config

        self._is_admin_enabled = False

    def _render(self) -> None:
        self._frame.configure(padx=1, pady=1)

        self._apply_frame_stretch(rows=(0,), columns=(1,))

        Scanner(
            self._frame,
            locations=self._config["locations"],
            on_change=self._validate_admin_passnum,
            styles=self._config["theme"]["scanner"]
        ).render().grid(row=0, column=0, sticky="nswe")

        if self._is_admin_enabled:
            LabelMaker(
                self._frame,
                self._config["item_names"],
                styles=self._config["theme"]["labelmaker"]
            ).render().grid(row=0, column=2, sticky="nswe")

    def _validate_admin_passnum(self, passnum: str):
        if passnum == self._config["admin_passnum"]:
            self._is_admin_enabled = (not self._is_admin_enabled)
            self.render()
