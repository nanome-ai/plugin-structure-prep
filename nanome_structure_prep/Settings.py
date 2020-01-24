import nanome
from os import path
import re

MENU_PATH = path.join(path.dirname(__file__), 'json/menus/Settings.json')
class Settings():
    def __init__(self, plugin, on_close):
        self.__plugin = plugin
        self.__menu = nanome.ui.Menu.io.from_json(MENU_PATH)
        self.__menu.register_closed_callback(on_close)

        self.__btn_bonds = self.__menu.root.find_node('Bonds Option')
        self.__btn_bonds.get_content().name = self.__btn_bonds.name
        self.__btn_bonds.get_content().register_pressed_callback(self.set_option)

        self.__btn_dssp  = self.__menu.root.find_node('DSSP Option')
        self.__btn_dssp.get_content().name = self.__btn_dssp.name
        self.__btn_dssp.get_content().register_pressed_callback(self.set_option)

        self.use_bonds = True
        self.use_dssp  = True

        self.__btn_bonds.get_content().selected = self.use_bonds
        self.__btn_dssp.get_content().selected = self.use_dssp

    def open_menu(self):
        self.__menu.enabled = True
        self.__plugin.menu = self.__menu
        self.__plugin.update_menu(self.__plugin.menu)

    def set_option(self, button):
        button.selected = not button.selected
        option_name  = re.sub(' option', '', button.name.lower())
        setattr(self, "use_"+option_name, button.selected)
        self.__plugin.update_content(button)