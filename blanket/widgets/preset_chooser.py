# Copyright 2021-2022 Rafael Mardojai CM
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, GObject, Gtk

from blanket.define import RES_PATH
from blanket.main_player import MainPlayer
from blanket.preset import Preset
from blanket.settings import Settings
from blanket.widgets.preset_row import PresetRow


@Gtk.Template(resource_path=f'{RES_PATH}/preset-chooser.ui')
class PresetChooser(Gtk.MenuButton):
    __gtype_name__ = 'PresetChooser'

    selected = GObject.Property(type=Preset)

    presets_list = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        # Create GioListStore to store Presets
        self.model = Gio.ListStore.new(Preset)
        self.presets_list.bind_model(self.model, self._create_widget)
        self.connect('notify::selected', self._on_selected_changed)

        # Wire widgets
        self.presets_list.connect('row-activated', self._on_preset_activated)

        self.load_presets()

    def load_presets(self):
        presets = Settings.get().get_presets_dict()
        for preset_id in presets:
            preset = Preset(preset_id)
            self.model.append(preset)

            if preset_id == Settings.get().active_preset:
                self.selected = preset

    def _on_preset_activated(self, _listbox, row):
        index = 0 if row is None else row.get_index()
        preset = self.model.get_item(index)
        self.selected = preset

    def _on_selected_changed(self, _chooser, _pspec):
        if self.selected is not None:
            if Settings.get().active_preset != self.selected.id:
                Settings.get().active_preset = self.selected.id

        MainPlayer.get().change_preset(self.selected)

    def _create_widget(self, preset):
        widget = PresetRow(preset)
        if preset.id == Settings.get().active_preset:
            widget.selected = True
        return widget
