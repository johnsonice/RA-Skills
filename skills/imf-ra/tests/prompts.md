# Activation smoke-test prompts

Representative prompts an IMF RA might say. For each, the table below records the **expected primary skill** to activate. Run these periodically by invoking each prompt fresh in a Claude Code session and confirming the right skill activates first. If activation drifts, tighten the `description` field in the relevant `SKILL.md`.

| # | Prompt | Expected primary skill | Notes |
|---|---|---|---|
| 1 | Pull WEO real GDP growth for G20 countries, 2010-present. | `imf-ra-data` | Direct fetch intent. |
| 2 | What's the BOPS series for current account balance? | `imf-ra-catalog` | Pure discovery. |
| 3 | Chart the global current account balances by country for the last decade. | `imf-ra-charts` | Should chain: catalog → data → charts. |
| 4 | I'm starting a project on emerging market debt — orient me to what's available. | `imf-ra` | Umbrella; broad orientation. |
| 5 | Find me a quarterly inflation series for emerging markets. | `imf-ra-catalog` | Discovery with frequency constraint. |
| 6 | Download IFS exchange rates monthly for ASEAN, 2015-present. | `imf-ra-data` | Direct fetch with country group. |
| 7 | Make a panel chart of debt-to-GDP for the G7. | `imf-ra-charts` | Chained, panel layout. |
| 8 | What's the difference between WEO inflation and CPI in IFS? | `imf-ra-catalog` | Overlay knowledge — should surface both with notes. |

## How to use this file

1. Open a fresh Claude Code session.
2. For each prompt, paste it and observe which skill activates first.
3. If the activated skill differs from the "Expected primary skill" column, tighten that skill's `description` field (or the activated skill's, if it's over-claiming).
4. Record findings inline as a `## Last run` section below.
