import hashlib
import unittest

from tools.legacy_species_mapping import (
    CANONICAL_SPECIES_COUNT,
    LEGACY_SPECIES_SLOTS,
    LOOKUP_CPU_ADDRESS,
    MAP_MAGIC,
    MAP_PAYLOAD_CPU_ADDRESS,
    MISSINGNO_SLOTS,
    POKEDEX_ORDER,
    POKEDEX_ORDER_SHA256,
    build_legacy_species_map_block,
    build_lookup_routine,
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

    def test_lookup_routine_targets_u16_payload(self):
        routine = build_lookup_routine()
        self.assertEqual(LOOKUP_CPU_ADDRESS, 0x43A0)
        self.assertEqual(len(routine), 23)
        self.assertIn(
            bytes((0x21, MAP_PAYLOAD_CPU_ADDRESS & 0xFF, MAP_PAYLOAD_CPU_ADDRESS >> 8)),
            routine,
        )
        self.assertTrue(routine.endswith(b"\x11\x00\x00\xC9"))


if __name__ == "__main__":
    unittest.main()
