"""Standalone tests for the registry cleanup, without a Home Assistant runtime."""

import importlib.util
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

MODULE = (
    Path(__file__).parents[1]
    / "custom_components/tuya_local_benelux/helpers/benelux.py"
)
SPEC = importlib.util.spec_from_file_location("benelux_cleanup", MODULE)
HELPER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HELPER)


class TestCleanup(unittest.TestCase):
    """Protect unrelated entries and active controls during cleanup."""

    def entity(self, suffix, entry="entry", device="device", disabled="user"):
        return SimpleNamespace(
            config_entry_id=entry,
            platform="tuya_local_benelux",
            unique_id=f"{device}-{suffix}",
            disabled_by=disabled,
            entity_id=f"select.{entry}_{device}_{suffix}",
        )

    def test_only_disabled_legacy_selectors_are_removed(self):
        entities = [
            self.entity("select_vertical_position"),
            self.entity("select_vertical_swing"),
            self.entity("select_vertical_position_swing"),
            self.entity("select_horizontal_position"),
            self.entity("select_vertical_position", entry="other"),
            self.entity("select_vertical_swing", device="other"),
            self.entity("select_vertical_swing", disabled=None),
        ]
        registry = SimpleNamespace(
            entities={e.entity_id + str(i): e for i, e in enumerate(entities)},
            async_remove=Mock(),
        )
        HELPER.cleanup_replaced_selects(registry, "entry", "device")
        self.assertEqual(
            [call.args[0] for call in registry.async_remove.call_args_list],
            [entities[0].entity_id, entities[1].entity_id],
        )

    def test_cleanup_handles_registry_mutation_and_is_repeatable(self):
        entity = self.entity("select_vertical_position")
        registry = SimpleNamespace(entities={entity.entity_id: entity})
        registry.async_remove = registry.entities.pop
        HELPER.cleanup_replaced_selects(registry, "entry", "device")
        HELPER.cleanup_replaced_selects(registry, "entry", "device")
        self.assertEqual(registry.entities, {})

    def test_original_integration_entities_are_never_removed(self):
        entity = self.entity("select_vertical_position")
        entity.platform = "tuya_local"
        registry = SimpleNamespace(
            entities={entity.entity_id: entity}, async_remove=Mock()
        )
        HELPER.cleanup_replaced_selects(registry, "entry", "device")
        registry.async_remove.assert_not_called()


if __name__ == "__main__":
    unittest.main()
