import hashlib
import unittest

from tools.legacy_species_mapping import (
    CANONICAL_SPECIES_COUNT,
    LEGACY_SPECIES_SLOTS,
    MAP_MAGIC,
    MISSINGNO_SLOTS,
    POKEDEX_ORDER,
    POKEDEX_ORDER_SHA256,
    build_legacy_species_map_block,
    inspect_legacy_species_map_block,
    legacy_species_to_canonical,
)


class LegacySpeciesMappingTests(unittest.TestCase):
    def test_verified_table_shape(self):
        self.assertEqual(len(POKEDEX_ORDER), LEGACY_SPECIES_SLOTS)
        self.assertEqual(POKEDEX_ORDER.count(0), MISSINGNO_SLOTS)
        self.assertEqual(hashlib.sha256(POKEDEX_ORDER).hexdigest(), POKEDEX_ORDER_SHA256)

    def test_all_official_gen1_ids_appear_once(self):
        actual = sorted(value for value in POKEDEX_ORDER if value)
        self.assertEqual(actual, list(range(1, CANONICAL_SPECIES_COUNT + 1)))

    def test_known_internal_ids(self):
        self.assertEqual(legacy_species_to_canonical(0x01), 112)
        self.assertEqual(legacy_species_to_canonical(0x15), 151)
        self.assertEqual(legacy_species_to_canonical(0x99), 1)
        self.assertEqual(legacy_species_to_canonical(0x1F), 0)

    def test_mapping_block_is_versioned_and_crc_checked(self):
        block = build_legacy_species_map_block()
        self.assertTrue(block.startswith(MAP_MAGIC))
        info = inspect_legacy_species_map_block(block)
        self.assertEqual(info["slots"], 190)
        self.assertEqual(info["canonical_count"], 151)
        self.assertEqual(info["id_width_bits"], 16)
        self.assertEqual(info["crc32_valid"], 1)


if __name__ == "__main__":
    unittest.main()
