# Move to the separate Benelux integration

Version 2026.10.1 uses `custom_components/tuya_local_benelux` and the
`tuya_local_benelux` integration domain. The original Tuya Local continues
to use `custom_components/tuya_local` and `tuya_local`.

This is a breaking, one-time migration from the earlier Benelux releases.
Updating the files does not move existing Home Assistant config entries,
devices, or entities to the new domain automatically.

1. Make a Home Assistant backup before updating. Keep the device ID, local
   key, IP address and selected protocol available privately. Do not post
   your local key or an unredacted configuration export on GitHub.
2. In Settings > Devices & services, disable the existing Tuya Local entry
   for this AC. Keep it until the new setup has been verified. This closes
   its local connection and avoids two integrations competing for the AC.
3. Update the Benelux package in HACS to 2026.10.1 and restart Home Assistant.
   Check that HACS reports the new integration folder. For a manual install,
   copy `custom_components/tuya_local_benelux` into your configuration's
   `custom_components` directory.
4. Add the **Tuya Local Benelux** integration. Use the same connection details
   and choose **Benelux air conditioner**. Verify power, temperature and swing.
5. New entities may have different entity IDs. Update dashboards and
   automations, or remove the old entry once satisfied and rename the new
   entities to the previous IDs. Do not delete the old entry before saving
   the details needed for rollback.
6. If you also want the original integration installed, install
   `make-all/tuya-local` through HACS after verifying the Benelux setup. Its
   files now have a separate folder. Keep its entry for this same AC disabled.

Both integrations can be installed, but use only one active connection to
this AC. Other devices can still use the original integration.

The HACS update picture customization on `update.tuya_local_update` is
separate from the AC integration domain. Check the actual HACS update entity
ID after migration; do not assume it has changed.

## Rollback

Disable the new Benelux AC entry. Restore the Home Assistant backup, or
reinstall the previous Benelux release and re-enable the old AC entry.
Never leave both entries connected to the same AC.
