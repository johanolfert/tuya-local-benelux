"""Cleanup for controls replaced by the Benelux combined swing selector."""


def cleanup_replaced_selects(registry, entry_id, device_uid):
    """Remove only the two disabled legacy selectors for this device entry."""
    replaced_ids = {
        f"{device_uid}-select_vertical_position",
        f"{device_uid}-select_vertical_swing",
    }
    for entity in tuple(registry.entities.values()):
        if (
            entity.config_entry_id == entry_id
            and entity.platform == "tuya_local_benelux"
            and entity.unique_id in replaced_ids
            and entity.disabled_by is not None
        ):
            registry.async_remove(entity.entity_id)
