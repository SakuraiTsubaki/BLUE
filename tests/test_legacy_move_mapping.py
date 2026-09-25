import unittest

from tools.legacy_move_mapping import (
    CANONICAL_MOVE_COUNT,
    LEGACY_MOVE_COUNT,
    LEGACY_MOVE_CODES,
    LOOKUP_CPU_ADDRESS,
    MAP_PAYLOAD_CPU_ADDRESS,
    build_legacy_move_map_block,
    build_lookup_routine,
    inspect_legacy_move_map_block,
    legacy_move_to_canonical,
)


class LegacyMoveMappingTests(unittest.TestCase):
    def test_identity_mapping_for_verified_gen1_moves(self):
        self.assertEqual(LEGACY_MOVE_COUNT, 165)
        for move_id in range(1, 166):
            self.assertEqual(legacy_move_to_canonical(move_id), move_id)

    def test_outside_verified_move_range_maps_to_zero(self):
        self.assertEqual(legacy_move_to_canonical(0), 0)
        self.assertEqual(legacy_move_to_canonical(166), 0)
        self.assertEqual(legacy_move_to_canonical(255), 0)

    def test_full_byte_translation_block(self):
        block = build_legacy_move_map_block()
        info = inspect_legacy_move_map_block(block)
        self.assertEqual(info["codes"], LEGACY_MOVE_CODES)
        self.assertEqual(info["canonical_count"], CANONICAL_MOVE_COUNT)
        self.assertEqual(info["id_width_bits"], 16)
        self.assertEqual(info["crc32_valid"], 1)

    def test_runtime_lookup_indexes_u16_payload(self):
        routine = build_lookup_routine()
        self.assertEqual(LOOKUP_CPU_ADDRESS, 0x4620)
        self.assertEqual(len(routine), 15)
        self.assertIn(
            bytes((0x21, MAP_PAYLOAD_CPU_ADDRESS & 0xFF, MAP_PAYLOAD_CPU_ADDRESS >> 8)),
            routine,
        )
        self.assertTrue(routine.endswith(b"\x5E\x23\x56\xC9"))


if __name__ == "__main__":
    unittest.main()
