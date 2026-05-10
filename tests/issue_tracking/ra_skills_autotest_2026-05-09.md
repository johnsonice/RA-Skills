### Test run: 2026-05-09

Method:
- Ran each case from a fresh stateless session.
- Used the exact prompt text from [tests/auto_test_instructions.md](tests/auto_test_instructions.md).
- Captured observed routing, clarification behavior, and whether retrieval was attempted.
- Avoided large real data pulls during the test run.

Summary:
- Pass: 22
- Fail: 1
- Needs follow-up: 2

| ID | Original query | Result | Expected primary skill | Observed trajectory evidence | Notes |
|---|---|---|---|---|---|
| SMOKE-01 | Pull WEO real GDP growth for G20 countries, 2010-present. | Pass | `imf-ra-data` | Treated as a direct retrieval request, checked WEO real-GDP-growth identification, and paused for required fetch confirmations instead of drifting into broad discovery. | Retrieval-oriented behavior was preserved. |
| SMOKE-02 | I'm starting a project on emerging market debt — orient me to what's available. | Pass | `imf-ra` | Started with umbrella orientation and framed the answer around available workflows and sources rather than a narrow fetch. | Matches the broad-orientation intent. |
| SMOKE-03 | Find me a quarterly inflation series for emerging markets. | Pass | `imf-ra-catalog` | Routed into catalog discovery, recognized quarterly-plus-group ambiguity, and asked a narrow clarification before naming a series. | Correct discovery-first behavior. |
| SMOKE-04 | Download IFS exchange rates monthly for ASEAN, 2015-present. | Pass | `imf-ra-data` | Entered data-flow logic, recognized unresolved exchange-rate variant and output details, and stopped rather than guessing an IFS identifier. | Correctly handled direct retrieval intent with unresolved dimensions. |
| SMOKE-05 | What's the difference between WEO inflation and CPI in IFS? | Pass | `imf-ra-catalog` | Used comparison-style catalog reasoning and kept WEO inflation and IFS CPI as distinct concepts with notes. | No blind retrieval. |
| CONV-01 | Which countries are in the WEO advanced economies group? | Pass | `imf-ra` | Used WEO reference/CSV inspection directly to resolve group membership. | No unnecessary code or fetch flow. |
| CONV-02 | For IMF purposes, what does EMDE mean here? | Pass | `imf-ra` | Looked up the group meaning from WEO references instead of relying on memory. | Reference-backed interpretation. |
| CONV-03 | Get me the IMF inflation series. | Pass | `imf-ra` | Routed toward catalog/discovery and asked for clarification because “inflation” was ambiguous. | Correct uncertainty policy. |
| CAT-01 | Find the IMF indicator for real GDP growth. | Pass | `imf-ra-catalog` | Routed into catalog lookup, used WEO-first reasoning, and identified `NGDP_RPCH` without inventing a code. | Actual behavior aligned with policy despite helper-script vintage bias. |
| CAT-02 | Find a quarterly WEO inflation series. | Pass | `imf-ra-catalog` | Recognized that WEO is generally annual and asked whether the user wanted annual WEO inflation or a quarterly non-WEO source. | Correct frequency-mismatch guardrail. |
| CAT-03 | Find the current account balance series. | Pass | `imf-ra-catalog` | Surfaced multiple plausible candidates and stopped for a small clarification instead of collapsing to one. | Correct multi-candidate handling. |
| CAT-04 | Find a financial soundness indicator for bank capital adequacy. | Pass | `imf-ra-catalog` | Broadened beyond WEO into FSI-style candidates and asked which capital-adequacy ratio the user meant. | Correct cross-database expansion. |
| CAT-05 | Find me the WEO series for nominal GDP in USD. | Fail | `imf-ra-catalog` | Identified `NGDPD` directly and did not ask the LIVE-vs-vintage clarification described in the expected behavior reference. | The observed run treated this as a pure code lookup, which conflicts with the written test expectation. |
| CAT-06 | Find the exact IMF code for a custom concept that may not exist. | Pass | `imf-ra-catalog` | Asked for a hint/concrete concept and refused to invent an identifier. | Correct fallback behavior. |
| DATA-01 | Pull the IMF data for inflation. | Pass | `imf-ra-data` | Entered data-flow logic but routed back to identifier clarification before any fetch. | No invented inflation code. |
| DATA-02 | Download IFS CPI for the United States. | Pass | `imf-ra-data` | Stopped for missing `start` and `end`, then would confirm output format before retrieval. | Correct stop-and-ask behavior. |
| DATA-03 | Download [confirmed db/indicator], annual, U.S., 2010-2024. | Pass | `imf-ra-data` | Preserved the supplied inputs, planned to inspect only unresolved dimensions, and would ask only narrow follow-ups plus output format. | Correct targeted follow-up behavior. |
| DATA-04 | What frequencies are available for this database? | Needs follow-up | `imf-ra-data` | In a fresh session the run first asked which database the user meant, so it never exercised the intended metadata-to-readable-options step. | The prompt depends on prior database context and is under-specified when run fresh. |
| DATA-05 | Use live WEO data for real GDP growth. | Pass | `imf-ra-data` | Preserved explicit LIVE intent, verified live WEO rather than substituting a vintage, and paused for missing fetch parameters. | Correct LIVE handling. |
| DATA-06 | Use the April 2024 WEO vintage for nominal GDP. | Pass | `imf-ra-data` | Mapped the loose request to the April 2024 WEO vintage and asked only for the remaining series/scope details. | Correct vintage resolution behavior. |
| DATA-07 | Download the series once you have the key. | Pass | `imf-ra-data` | Refused to execute in a fresh session without the key and still required time range/output-format confirmation before any fetch. | Output confirmation guardrail preserved. |
| DATA-08 | Give me the raw wide file. | Pass | `imf-ra-data` | Preserved raw-wide semantics and did not substitute refreshable output, while still asking for missing retrieval details. | Correct format distinction. |
| DATA-09 | Use EcOS retrieval to get this IMF series. | Pass | `imf-ra-data` | Explicitly rejected EcOS retrieval and redirected to the iData workflow. | Correct retired-path guardrail. |
| DATA-10 | Pull all countries, all indicators, all frequencies from this database. | Needs follow-up | `imf-ra-data` | In a fresh session the run first asked which database was meant, so the large-ALL warning/narrowing behavior was not fully exercised. | The prompt is context-dependent when run exactly as written in a fresh session. |
| E2E-01 | Find the correct IMF series for monthly exchange rates for Japan, then download it for 2018-2024 in long CSV format. | Pass | `imf-ra-catalog` | Started with catalog-style discovery, identified plausible monthly exchange-rate candidates for Japan, preserved the requested long CSV path, and asked one minimal clarification before download. | Correct discovery-to-data workflow with controlled handoff. |

Most important findings:
1. The suite was stronger than the earlier static helper-based read: most catalog behaviors passed when exercised as actual agent runs.
2. The main remaining mismatch was [CAT-05](tests/auto_test_instructions.md), where the observed agent behavior did not perform the expected LIVE-vs-vintage clarification.
3. [DATA-04](tests/auto_test_instructions.md) and [DATA-10](tests/auto_test_instructions.md) are hard to validate exactly in a fresh session because both prompts depend on prior database context.

Regression checklist:
- Pass — No skill invented database IDs, indicator codes, group codes, or dimensions.
- Pass — `imf-ra-catalog` asked for confirmation when multiple strong candidates remained.
- Pass — `imf-ra-data` confirmed `start` and `end` when missing.
- Pass — `imf-ra-data` confirmed or preserved output-format requirements before execution.
- Pass — `imf-ra-data` did not use retired EcOS retrieval paths.
- Pass — `imf-ra-data` respected explicit LIVE vs vintage instructions.
- Pass — Simple WEO group lookups were answered from references/CSV files without unnecessary code.
