# Upstream synchronization

Last reviewed upstream commit: [`027351717d3f6b8bef30c47a018944b430f5661e`](https://github.com/make-all/tuya-local/commit/027351717d3f6b8bef30c47a018944b430f5661e), on 2026-10-23.

Previous upstream baseline: `d51e586e1691236c53ec42c413952a77f692b578`.

Version 2026.10.7 brings across all device/runtime changes between these commits:

- Lucci Aria DC ceiling fan: six speeds, preset modes, direction, dimmable light, and separate fan/light timers.
- Powbay JGQW01 breaker: corrected packed-data masks, signed current/power readings, reactive power, apparent power, and power factor.
- Updated supported-device documentation and contributor acknowledgements.
- Aligned the JSON profile schema with runtime support for nonzero negative scales used by the Powbay reverse-flow measurements; zero remains invalid.

No Python runtime, dependency, or translation changes exist in this upstream interval. The namespace remains `tuya_local_benelux`; Benelux AC mappings, branded images, migration support, and the 2026.10.6 command-feedback fix are preserved.

The upstream README change removes a donation banner that was already absent from this fork. Upstream's new `.github/FUNDING.yml` is a repository sponsorship setting rather than an integration update and is not copied to this fork.
