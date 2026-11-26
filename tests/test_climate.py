"""Tests for the climate entity."""

from unittest.mock import AsyncMock, Mock

import pytest
from homeassistant.components.climate.const import ATTR_CURRENT_TEMPERATURE
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.tuya_local_benelux.climate import (
    TuyaLocalClimate,
    async_setup_entry,
)
from custom_components.tuya_local_benelux.const import (
    CONF_DEVICE_ID,
    CONF_PROTOCOL_VERSION,
    CONF_TYPE,
    DOMAIN,
)
from custom_components.tuya_local_benelux.helpers.device_config import get_config


@pytest.mark.asyncio
async def test_init_entry(hass):
    """Test the initialisation."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_TYPE: "heater",
            CONF_DEVICE_ID: "dummy",
            CONF_PROTOCOL_VERSION: "auto",
        },
    )
    # although async, the async_add_entities function passed to
    # async_setup_entry is called truly asynchronously. If we use
    # AsyncMock, it expects us to await the result.
    m_add_entities = Mock()
    m_device = AsyncMock()
    m_device.get_property = Mock(return_value=None)

    hass.data[DOMAIN] = {}
    hass.data[DOMAIN]["dummy"] = {}
    hass.data[DOMAIN]["dummy"]["device"] = m_device

    await async_setup_entry(hass, entry, m_add_entities)
    assert type(hass.data[DOMAIN]["dummy"]["climate"]) is TuyaLocalClimate
    m_add_entities.assert_called_once()


async def test_benelux_temperature_state_and_setpoint(hass):
    """Expose the AC's temperatures through Home Assistant's climate entity."""
    readings = {"1": True, "2": 240, "3": 22, "4": "cold", "110": 0}
    device = Mock(get_property=readings.get, async_set_properties=AsyncMock())
    config = get_config("benelux_airconditioner")
    climate_config = next(e for e in config.all_entities() if e.entity == "climate")
    entity = TuyaLocalClimate(device, climate_config)
    entity.hass = hass

    assert entity.native_temperature_unit is UnitOfTemperature.CELSIUS
    assert entity.state_attributes[ATTR_CURRENT_TEMPERATURE] == 22
    assert entity.state_attributes[ATTR_TEMPERATURE] == 24

    await entity.async_set_temperature(temperature=24.5)
    device.async_set_properties.assert_awaited_once_with({"2": 245})


# After removal of deprecated entities, there are no secondary climate devices to test against.
# async def test_init_entry_as_secondary(hass):
#     """Test initialisation when climate is a secondary entity"""
#     entry = MockConfigEntry(
#         domain=DOMAIN,
#         data={
#             CONF_TYPE: "goldair_dehumidifier",
#             CONF_DEVICE_ID: "dummy",
#         },
#     )
#     # although async, the async_add_entities function passed to
#     # async_setup_entry is called truly asynchronously. If we use
#     # AsyncMock, it expects us to await the result.
#     m_add_entities = Mock()
#     m_device = AsyncMock()

#     hass.data[DOMAIN] = {}
#     hass.data[DOMAIN]["dummy"] = {}
#     hass.data[DOMAIN]["dummy"]["device"] = m_device

#     await async_setup_entry(hass, entry, m_add_entities)
#     assert (
#         type(hass.data[DOMAIN]["dummy"]["climate_dehumidifier_as_climate"])
#         is TuyaLocalClimate
#     )
#     m_add_entities.assert_called_once()


@pytest.mark.asyncio
async def test_init_entry_fails_if_device_has_no_climate(hass):
    """Test initialisation when device has no matching entity"""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_TYPE: "smartplugv1",
            CONF_DEVICE_ID: "dummy",
            CONF_PROTOCOL_VERSION: "auto",
        },
    )
    # although async, the async_add_entities function passed to
    # async_setup_entry is called truly asynchronously. If we use
    # AsyncMock, it expects us to await the result.
    m_add_entities = Mock()
    m_device = AsyncMock()

    hass.data[DOMAIN] = {}
    hass.data[DOMAIN]["dummy"] = {}
    hass.data[DOMAIN]["dummy"]["device"] = m_device
    try:
        await async_setup_entry(hass, entry, m_add_entities)
        assert False
    except ValueError:
        pass
    m_add_entities.assert_not_called()


@pytest.mark.asyncio
async def test_init_entry_fails_if_config_is_missing(hass):
    """Test initialisation when device has no matching entity"""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_TYPE: "non_existing",
            CONF_DEVICE_ID: "dummy",
            CONF_PROTOCOL_VERSION: "auto",
        },
    )
    # although async, the async_add_entities function passed to
    # async_setup_entry is called truly asynchronously. If we use
    # AsyncMock, it expects us to await the result.
    m_add_entities = Mock()
    m_device = AsyncMock()

    hass.data[DOMAIN] = {}
    hass.data[DOMAIN]["dummy"] = {}
    hass.data[DOMAIN]["dummy"]["device"] = m_device
    try:
        await async_setup_entry(hass, entry, m_add_entities)
        assert False
    except ValueError:
        pass
    m_add_entities.assert_not_called()
