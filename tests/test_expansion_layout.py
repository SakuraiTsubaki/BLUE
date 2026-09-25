import hashlib
import unittest

from tools.blue_expansion_layout import (
    DIRECTORY_ENTRY_SIZE,
    MAGIC,
    PROFILE_LAYOUT,
    REGISTRY_DOMAINS,
    ROM_BANK_BYTES,
    build_directory,
    inspect_directory_entry,
    inspect_header,
    install_expansion_metadata,
    metadata_file_offset,
)
from tools.legacy_species_mapping import (
    LOOKUP_BANK_OFFSET,
    LOOKUP_CPU_ADDRESS,
    MAP_BANK_OFFSET,
    MAP_CPU_ADDRESS,
    build_legacy_species_map_block,
    build_lookup_routine,
)


class ExpansionLayoutTests(unittest.TestCase):
    def test_profile_metadata_banks(self):
        self.assertEqual(PROFILE_LAYOUT["ao-jp"]["metadata_bank"], 0x20)
        for profile in ("blue-us-eu", "blue-fr", "blue-de", "blue-it", "blue-es"):
            self.assertEqual(PROFILE_LAYOUT[profile]["metadata_bank"], 0x40)

    def test_directory_is_versioned(self):
        directory = build_directory("ao-jp")
        self.assertEqual(len(directory), len(REGISTRY_DOMAINS) * DIRECTORY_ENTRY_SIZE)

    def test_install_uses_first_expansion_bank(self):
        source_sha = hashlib.sha256(b"blue-test").hexdigest()
        image = bytearray(b"\xFF" * 0x800000)
        install_expansion_metadata(image, "ao-jp", source_sha)
        base = metadata_file_offset("ao-jp")
        self.assertEqual(base, 0x20 * ROM_BANK_BYTES)
        self.assertEqual(image[base:base + 8], MAGIC)
        info = inspect_header(image, "ao-jp")
        self.assertEqual(info["schema_version"], 2)
        self.assertEqual(info["first_content_bank"], 0x21)
        self.assertEqual(info["directory_count"], 10)
        self.assertEqual(info["legacy_species_map_cpu_address"], MAP_CPU_ADDRESS)
        self.assertEqual(info["crc32_valid"], 1)

    def test_species_directory_points_to_callable_adapter(self):
        source_sha = hashlib.sha256(b"blue-dir").hexdigest()
        image = bytearray(b"\xFF" * 0x800000)
        install_expansion_metadata(image, "ao-jp", source_sha)
        species = inspect_directory_entry(image, "ao-jp", 0)
        self.assertEqual(species["domain_id"], 1)
        self.assertEqual(species["count"], 151)
        self.assertEqual(species["bank"], 0x20)
        self.assertEqual(species["address"], LOOKUP_CPU_ADDRESS)
        self.assertEqual(species["flags"] & 0x0003, 0x0003)

    def test_species_map_and_lookup_are_embedded(self):
        source_sha = hashlib.sha256(b"blue-map").hexdigest()
        image = bytearray(b"\xFF" * 0x800000)
        install_expansion_metadata(image, "ao-jp", source_sha)
        base = metadata_file_offset("ao-jp")
        block = build_legacy_species_map_block()
        routine = build_lookup_routine()
        self.assertEqual(image[base + MAP_BANK_OFFSET:base + MAP_BANK_OFFSET + len(block)], block)
        self.assertEqual(image[base + LOOKUP_BANK_OFFSET:base + LOOKUP_BANK_OFFSET + len(routine)], routine)

    def test_international_content_starts_after_original_1mib(self):
        source_sha = hashlib.sha256(b"blue-intl").hexdigest()
        image = bytearray(b"\xFF" * 0x800000)
        install_expansion_metadata(image, "blue-us-eu", source_sha)
        info = inspect_header(image, "blue-us-eu")
        species = inspect_directory_entry(image, "blue-us-eu", 0)
        self.assertEqual(info["metadata_bank"], 0x40)
        self.assertEqual(info["first_content_bank"], 0x41)
        self.assertEqual(species["bank"], 0x40)


if __name__ == "__main__":
    unittest.main()
