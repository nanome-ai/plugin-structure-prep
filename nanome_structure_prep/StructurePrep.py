from functools import partial

import nanome
from nanome.util import Logs

from .Settings import Settings

class StructurePrep(nanome.PluginInstance):
    def start(self):
        self.settings = Settings(self, lambda b: None)
        self.integration.structure_prep = self.integration_request

    def on_run(self):
        self.request_complex_list(self.get_complexes_deep)

    def get_complexes_deep(self, complex_list):
        selected = [c.index for c in complex_list if c._selected]
        if not selected:
            self.send_notification(nanome.util.enums.NotificationTypes.error, "Please select an entry")
            return
        self.set_plugin_list_button(self.PluginListButtonType.run, "Running...", False)
        self.request_complexes(selected, self.start_step1)

    def replace_conformers(self, complexes, callback):
        for i in range(len(complexes)):
            complex_index = complexes[i].index
            Logs.debug('converting complex', i, 'to frames')
            complexes[i] = complexes[i].convert_to_frames()
            complexes[i].index = complex_index
        callback(complexes)

    def replace_frameds(self, complexes, callback):
        for i in range(len(complexes)):
            index = complexes[i].index
            Logs.debug('converting complex', i, 'to conformers')
            complexes[i] = complexes[i].convert_to_conformers()
            complexes[i].index = index

        callback(complexes)

    def integration_request(self, request):
        def sender(complex_list):
            request.send_response(complex_list)
        self.start_step1(request.get_args(), sender)

    def start_step1(self, complex_list, sender=None):
        self.replace_conformers(complex_list, partial(self.step1, sender=sender or self.done))

    def step1(self, complex_list, sender):
        if self.settings.use_bonds:
            # remove bonds first
            for complex in complex_list:
                for atom in complex.atoms:
                    atom._bonds.clear()
                for residue in complex.residues:
                    residue._bonds.clear()
            # readd bonds
            def start_step2(complex_list):
                self.step2(complex_list, sender)
            self.add_bonds(complex_list, start_step2)
        else:
            self.step2(complex_list, sender)

    def step2(self, complex_list, sender):
        if self.settings.use_dssp:
            self.add_dssp(complex_list, partial(self.replace_frameds, callback=sender))
        else:
            self.replace_frameds(complex_list, sender)

    def done(self, complex_list):
        self.set_plugin_list_button(self.PluginListButtonType.run, "Run", True)
        self.update_structures_deep(complex_list, lambda: self.send_notification(nanome.util.enums.NotificationTypes.success, "Structures prepped"))

    def on_advanced_settings(self):
        self.settings.open_menu()

def main():
    plugin = nanome.Plugin("Structure Prep", "Select your structures from the Entry List, then press Run to regenerate bonds and secondary structure.", "Structure", True)
    plugin.set_plugin_class(StructurePrep)
    plugin.run()

if __name__ == "__main__":
    main()