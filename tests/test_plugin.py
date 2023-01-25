import asyncio
import os
import unittest
from random import randint

from unittest.mock import MagicMock
from nanome.api.structure import Complex
from plugin.StructurePrep import StructurePrep
from nanome.util.enums import SecondaryStructure

fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')


def run_awaitable(awaitable, *args, **kwargs):
    loop = asyncio.get_event_loop()
    if loop.is_running:
        loop = asyncio.new_event_loop()
    loop.run_until_complete(awaitable(*args, **kwargs))
    loop.close()


class PluginFunctionTestCase(unittest.TestCase):

    def setUp(self):
        tyl_pdb = f'{fixtures_dir}/1tyl.pdb'
        self.complex = Complex.io.from_pdb(path=tyl_pdb)
        for atom in self.complex.atoms:
            atom.index = randint(1000000000, 9999999999)
        self.plugin_instance = StructurePrep()
        self.plugin_instance.start()
        self.plugin_instance._network = MagicMock()

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