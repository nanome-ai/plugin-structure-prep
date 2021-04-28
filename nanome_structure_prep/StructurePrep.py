from functools import partial

import nanome
from nanome.util import async_callback, Logs
from nanome.util.enums import NotificationTypes

from .Settings import Settings

class StructurePrep(nanome.AsyncPluginInstance):
    def start(self):
        self.settings = Settings(self, lambda b: None)
        self.integration.structure_prep = self.integration_request

    @async_callback
    async def on_run(self):
        complex_list = await self.request_complex_list()
        selected = [c.index for c in complex_list if c._selected]

        if not selected:
            self.send_notification(NotificationTypes.error, "Please select an entry")
            return

        self.set_plugin_list_button(self.PluginListButtonType.run, "Running...", False)
        complexes = await self.request_complexes(selected)
        complexes = await self.prep_structures(complexes)
        self.set_plugin_list_button(self.PluginListButtonType.run, "Run", True)

        await self.update_structures_deep(complexes)
        self.send_notification(NotificationTypes.success, "Structures prepped")

    @async_callback
    async def integration_request(self, request):
        complexes = await self.prep_structures(request.get_args())
        request.send_response(complexes)

    async def prep_structures(self, complexes):
        for i in range(len(complexes)):
            complex_index = complexes[i].index
            complexes[i] = complexes[i].convert_to_frames()
            complexes[i].index = complex_index

        if self.settings.use_bonds:
            # remove bonds first
            for complex in complexes:
                for atom in complex.atoms:
                    atom._bonds.clear()
                for residue in complex.residues:
                    residue._bonds.clear()
            # readd bonds
            await self.add_bonds(complexes)

        if self.settings.use_dssp:
            await self.add_dssp(complexes)

        for i in range(len(complexes)):
            index = complexes[i].index
            complexes[i] = complexes[i].convert_to_conformers()
            complexes[i].index = index

        return complexes

    def on_advanced_settings(self):
        self.settings.open_menu()

def main():
    plugin = nanome.Plugin("Structure Prep", "Select your structures from the Entry List, then press Run to regenerate bonds and secondary structure.", "Structure", True)
    plugin.set_plugin_class(StructurePrep)
    plugin.run()

if __name__ == "__main__":
    main()
