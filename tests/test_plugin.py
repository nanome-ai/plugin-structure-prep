import asyncio
import os
import unittest
from random import randint
import multiprocessing

from unittest.mock import MagicMock
from nanome.api.structure import Complex
from plugin.StructurePrep import StructurePrep
from nanome.util.enums import SecondaryStructure
from plugin.Settings import Settings


fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')


def run_awaitable(awaitable, *args, **kwargs):
    loop = asyncio.get_event_loop()
    if loop.is_running:
        loop = asyncio.new_event_loop()
    loop.run_until_complete(awaitable(*args, **kwargs))
    loop.close()


class StructurePrepTestCase(unittest.TestCase):

    def setUp(self):
        tyl_pdb = f'{fixtures_dir}/1tyl.pdb'
        self.complex = Complex.io.from_pdb(path=tyl_pdb)
        for atom in self.complex.atoms:
            atom.index = randint(1000000000, 9999999999)
        self.plugin_instance = StructurePrep()
        self.plugin_instance.start()

    def tearDown(self) -> None:
        self.plugin_instance.on_stop()
        return super().tearDown()

    def test_prep_structures(self):
        # Make sure get_clean_pdb_file function returns valid pdb can be parsed into a Complex structure.
        loop = asyncio.get_event_loop()
        # Validate zero bonds, and all secondary structures are unknown
        self.assertEqual(len(list(self.complex.bonds)), 0)
        self.assertTrue(all([
            res.secondary_structure == SecondaryStructure.Unknown
            for res in self.complex.residues
        ]))
        result = loop.run_until_complete(self.plugin_instance.prep_structures([self.complex]))
        prepped_complex = result[0]
        # Assert Bonds are added, and secondary structures are assigned
        self.assertTrue(len(list(prepped_complex.bonds)) > 0)
        known_secondary_structures = [
            res for res in prepped_complex.residues
            if res.secondary_structure != SecondaryStructure.Unknown
        ]
        self.assertTrue(len(known_secondary_structures) > 0)

    def test_on_run(self):
        async def validate_on_run(self):
            self.complex._selected = True
            req_list_fut = asyncio.Future()
            req_list_fut.set_result([self.complex])
            req_comp_fut = asyncio.Future()
            req_comp_fut.set_result([self.complex])
            prep_struc_fut = asyncio.Future()
            prep_struc_fut.set_result([self.complex])

            self.plugin_instance.request_complex_list = MagicMock(return_value=req_list_fut)
            self.plugin_instance.request_complexes = MagicMock(return_value=req_comp_fut)
            self.plugin_instance.prep_structures = MagicMock(return_value=prep_struc_fut)
            self.plugin_instance.set_plugin_list_button = MagicMock()
            self.plugin_instance.update_structures_deep = MagicMock(return_value=req_list_fut)
            self.plugin_instance.send_notification = MagicMock()
            await self.plugin_instance.on_run()
            # Assert that the prep_complex and update calls are made
            self.plugin_instance.prep_structures.assert_called_once()
            self.plugin_instance.update_structures_deep.assert_called_once()
        run_awaitable(validate_on_run, self)


class SettingsMenuTestCase(unittest.TestCase):

    def setUp(self):
        self.plugin = unittest.mock.MagicMock()
        self.settings = Settings(self.plugin)
    
    def test_set_option(self):
        """Test that bonds and dssp settings can be toggled."""
        # Assert settings are Enabled
        btn_bonds = self.settings.btn_bonds
        btn_dssp = self.settings.btn_dssp
        self.assertTrue(btn_bonds.selected)
        self.assertTrue(btn_dssp.selected)
        self.assertTrue(self.settings.use_bonds)
        self.assertTrue(self.settings.use_dssp)
        # Toggle settings
        self.settings.set_option(btn_bonds)
        self.settings.set_option(btn_dssp)
        # Assert settings are disabled
        self.assertFalse(btn_bonds.selected)
        self.assertFalse(btn_dssp.selected)
        self.assertFalse(self.settings.use_bonds)
        self.assertFalse(self.settings.use_dssp)
    
