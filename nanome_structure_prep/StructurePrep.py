import nanome
from nanome.util import Logs

from .Settings import Settings

class StructurePrep(nanome.PluginInstance):
    def start(self):
        self.settings = Settings(self, lambda b: None)

    def on_run(self):
        self.request_complex_list(self.get_complexes_deep)

    def get_complexes_deep(self, complex_list):
        selected = [c.index for c in complex_list if c._selected]
        self.request_complexes(selected, self.step1)

    def step1(self, complex_list):
        if self.settings.use_bonds:
            self.add_bonds(complex_list, self.step2, nano=True)
        else:
            self.step2(complex_list)

    def step2(self, complex_list):
        if self.settings.use_dssp:
            self.add_dssp(complex_list, self.add_to_workspace)
        else:
            self.add_to_workspace(complex_list)

    def on_advanced_settings(self):
        self.settings.open_menu()

def main():
    plugin = nanome.Plugin("Structure Prep", "A plugin to clean up selected structures", "Structure", True)
    plugin.set_plugin_class(StructurePrep)
    plugin.run('127.0.0.1', 8888)

if __name__ == "__main__":
    main()