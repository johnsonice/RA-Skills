# IMF RA skill family — agent auto-test prompt pack

This file is written so an agent can read it directly and run a full behavioral test pass for the currently implemented IMF RA skill family:

- `imf-ra`
- `imf-ra-catalog`
- `imf-ra-data`

Chart-related tests are intentionally excluded because `imf-ra-charts` is not implemented yet.

---

## 1. Agent instructions: how to run the auto test

Use this file as the single source of truth for auto-testing routing, guardrails, and expected behavior.

### Test objective

For each test case below, verify that the agent:

1. routes to the correct primary skill,
2. follows the expected policy and guardrails,
3. avoids unsupported shortcuts or guesses,
4. produces behavior consistent with the expected reference in this file.

### Required execution method

For each case:

1. Start from a fresh session or clean reasoning context if possible.
2. Use the **Test prompt** exactly as written.
3. Record the original query verbatim in the test log so another agent can replicate the case exactly.
4. Capture the actual action trajectory, including at minimum:
	- which skill should have activated first,
	- whether the agent searched references, metadata, or helper scripts,
	- whether the agent asked a clarifying question,
	- whether the agent attempted retrieval or intentionally stopped,
	- whether the agent avoided prohibited guessing.
5. Compare the actual trajectory against both:
	- **Expected primary skill**
	- **Expected behavior reference**
6. Mark the case as one of:
	- **Pass**
	- **Fail**
	- **Needs follow-up**
7. Record short evidence from the trajectory explaining the verdict.

### How to verify against the action trajectory

When evaluating a test, the agent should look back at its own action trajectory and confirm the following:

- **Route check**: Did the first meaningful step match the expected primary skill behavior?
- **Behavior check**: Did the agent do what the policy requires?
- **Guardrail check**: Did the agent avoid inventing codes, dimensions, or unsupported claims?
- **Stop/ask check**: If clarification was required, did the agent ask instead of guessing?
- **Execution check**: If execution was allowed, did the agent use the correct data path and output policy?

### Fail conditions

Mark a case as **Fail** if any of the following happens:

- wrong primary skill behavior,
- invented database, indicator, country-group, or dimension identifiers,
- skipped a required clarification,
- used a retired or disallowed path,
- ignored explicit LIVE vs vintage handling,
- executed a fetch when the expected behavior was to clarify first,
- returned an answer that contradicts the expected behavior reference.

### Scope note

This file tests behavior, not just final wording. A case should only pass if the action trajectory and outcome both align with the reference behavior.

---

## 2. Pass criteria legend

- **Route**: the expected primary skill activates first.
- **Behavior**: the agent follows the documented policy.
- **Guardrail**: the agent avoids disallowed shortcuts or guesses.
- **Trajectory evidence**: the agent can point to its own actions as proof.

---

## 3. Smoke tests for activation and routing

Representative prompts for a quick routing check.

| ID | Test prompt | Expected primary skill | Expected behavior reference | Trajectory evidence to confirm |
|---|---|---|---|---|
| SMOKE-01 | Pull WEO real GDP growth for G20 countries, 2010-present. | `imf-ra-data` | Treats this as a direct fetch request, not a broad discovery question. | The first meaningful actions should be data-oriented: identifying required fetch inputs and preparing retrieval flow. |
| SMOKE-02 | I'm starting a project on emerging market debt — orient me to what's available. | `imf-ra` | Provides broad orientation across available sources or workflows instead of jumping straight into a narrow fetch. | The trajectory should show umbrella or orientation behavior before any narrow database-specific execution. |
| SMOKE-03 | Find me a quarterly inflation series for emerging markets. | `imf-ra-catalog` | Treats this as discovery with a frequency constraint and searches for suitable candidates. | The trajectory should show indicator or database discovery rather than immediate downloading. |
| SMOKE-04 | Download IFS exchange rates monthly for ASEAN, 2015-present. | `imf-ra-data` | Treats this as a direct retrieval task with country-group and time-range handling. | The trajectory should show data retrieval setup and any required dimension resolution. |
| SMOKE-05 | What's the difference between WEO inflation and CPI in IFS? | `imf-ra-catalog` | Surfaces both concepts with notes instead of collapsing them into one. | The trajectory should show comparative catalog or reference reasoning, not blind retrieval. |

---

## 4. Shared conventions and umbrella behavior

| ID | Area | Test prompt | Expected primary skill | Expected behavior reference | Trajectory evidence to confirm |
|---|---|---|---|---|---|
| CONV-01 | No unnecessary code | "Which countries are in the WEO advanced economies group?" | `imf-ra` | Answers from the WEO group reference or CSV contents instead of writing code if simple inspection is enough. | The trajectory should show direct reference lookup or file inspection, not unnecessary script writing. |
| CONV-02 | Country-group translation | "For IMF purposes, what does EMDE mean here?" | `imf-ra` | Uses the WEO group reference instead of guessing from memory. | The trajectory should show reference-backed interpretation of the group label. |
| CONV-03 | Uncertainty policy | "Get me the IMF inflation series." | `imf-ra` | Does not guess; asks a clarifying question because multiple plausible indicators or databases exist. | The trajectory should stop for clarification rather than selecting one inflation series on its own. |

---

## 5. Catalog skill behavior

| ID | Area | Test prompt | Expected primary skill | Expected behavior reference | Trajectory evidence to confirm |
|---|---|---|---|---|---|
| CAT-01 | WEO-first policy | "Find the IMF indicator for real GDP growth." | `imf-ra-catalog` | Searches WEO Live first for a common annual macro concept. | The trajectory should start with WEO-oriented discovery before considering broader search. |
| CAT-02 | Frequency mismatch | "Find a quarterly WEO inflation series." | `imf-ra-catalog` | Flags that WEO is generally annual and either asks for confirmation or suggests a better-suited database such as IFS if supported. | The trajectory should show awareness of the mismatch instead of pretending quarterly WEO is straightforward. |
| CAT-03 | Ambiguous candidates | "Find the current account balance series." | `imf-ra-catalog` | Returns multiple plausible candidates with short distinction notes instead of collapsing them into one. | The trajectory should show candidate comparison and a refusal to over-commit to one series without support. |
| CAT-04 | Cross-database search only when needed | "Find a financial soundness indicator for bank capital adequacy." | `imf-ra-catalog` | Searches beyond WEO when the concept is outside normal WEO coverage. | The trajectory should show expansion beyond WEO because the concept requires it. |
| CAT-05 | Vintage clarification | "Find me the WEO series for nominal GDP in USD." | `imf-ra-catalog` | If a concrete fetch path would require choosing LIVE vs vintage and the user did not specify, asks which they want rather than silently picking one. | The trajectory should show a clarification point on LIVE vs vintage when needed. |
| CAT-06 | No invented identifiers | "Find the exact IMF code for a custom concept that may not exist." | `imf-ra-catalog` | Surfaces the gap and asks for a hint or clarification; does not invent a code. | The trajectory should show explicit uncertainty handling rather than fabricated identifiers. |

---

## 6. Data skill behavior

| ID | Area | Test prompt | Expected primary skill | Expected behavior reference | Trajectory evidence to confirm |
|---|---|---|---|---|---|
| DATA-01 | Requires confirmed identifier | "Pull the IMF data for inflation." | `imf-ra-data` | If the identifier is not confirmed, routes through catalog logic first rather than inventing an indicator code. | The trajectory should show a handoff to discovery or a clarification step before retrieval. |
| DATA-02 | Always confirm time range | "Download IFS CPI for the United States." | `imf-ra-data` | Explicitly asks for `start` and `end` before fetching. | The trajectory should show a stop for missing time-range parameters. |
| DATA-03 | Ask only for unresolved multi-value dimensions | "Download [confirmed db/indicator], annual, U.S., 2010-2024." | `imf-ra-data` | Uses already supplied dimensions, auto-resolves any single-value dimensions silently, and asks only for unresolved multi-value dimensions. | The trajectory should show targeted follow-up only for unresolved dimensions, not a full re-ask of already known inputs. |
| DATA-04 | Dimension options on request | "What frequencies are available for this database?" | `imf-ra-data` | Uses dimension metadata and presents readable options like Annual (`A`), Quarterly (`Q`), Monthly (`M`) instead of a raw dump when possible. | The trajectory should show metadata inspection and readable normalization of options. |
| DATA-05 | LIVE vs vintage explicit live | "Use live WEO data for real GDP growth." | `imf-ra-data` | Uses the LIVE database directly and does not substitute a vintage. | The trajectory should preserve the explicit LIVE instruction through the retrieval path. |
| DATA-06 | Vintage loose date mapping | "Use the April 2024 WEO vintage for nominal GDP." | `imf-ra-data` | Maps the request to the nearest matching vintage without asking again if the intent is clear. | The trajectory should show vintage resolution rather than unnecessary extra clarification. |
| DATA-07 | Output format confirmation | "Download the series once you have the key." | `imf-ra-data` | Asks which output format the user wants: Refreshable, Wide, or Long; for Wide or Long also confirms CSV vs Excel. | The trajectory should pause for output-format confirmation before execution. |
| DATA-08 | Refreshable distinction | "Give me the raw wide file." | `imf-ra-data` | Does not substitute refreshable output for raw wide output. | The trajectory should preserve the requested raw wide output semantics. |
| DATA-09 | EcOS retired policy | "Use EcOS retrieval to get this IMF series." | `imf-ra-data` | Explains that EcOS retrieval is retired and provides the iData-equivalent path instead. | The trajectory should explicitly reject retired EcOS retrieval and redirect correctly. |
| DATA-10 | Safe query policy | "Pull all countries, all indicators, all frequencies from this database." | `imf-ra-data` | Avoids broad `ALL` pulls unless explicitly confirmed and warns or narrows the request where appropriate. | The trajectory should show a warning or narrowing step instead of launching a huge pull immediately. |

---

## 7. End-to-end workflow cases

| ID | Area | Test prompt | Expected primary skill | Expected behavior reference | Trajectory evidence to confirm |
|---|---|---|---|---|---|
| E2E-01 | Discovery → fetch | "Find the correct IMF series for monthly exchange rates for Japan, then download it for 2018-2024 in long CSV format." | `imf-ra-catalog` | Resolves the identifier first, then hands off to data flow, asks for any missing dimensions, and confirms the requested long CSV output. | The trajectory should show catalog resolution first, then controlled transition into retrieval with output-format handling. |

---

## 8. Regression checklist for future edits

Use this checklist after changing any of the skill files.

- [ ] No skill invents database IDs, indicator codes, group codes, or dimensions.
- [ ] `imf-ra-catalog` asks for confirmation when multiple strong candidates remain.
- [ ] `imf-ra-data` always confirms `start` and `end` if missing.
- [ ] `imf-ra-data` always confirms output format before execution.
- [ ] `imf-ra-data` does not use retired EcOS retrieval paths.
- [ ] `imf-ra-data` respects LIVE vs vintage policy.
- [ ] Simple WEO group lookups are answered from references or CSV files without unnecessary code.

---

## 9. Result log template for an agent test run

Copy and fill this template when running the suite.

```markdown
### Test run: YYYY-MM-DD

| ID | Original query | Result | Expected primary skill | Observed trajectory evidence | Notes |
|---|---|---|---|---|---|
| SMOKE-01 | Pull WEO real GDP growth for G20 countries, 2010-present. | Pass | `imf-ra-data` | Asked for retrieval inputs and treated prompt as direct fetch. | |
| CONV-01 | Which countries are in the WEO advanced economies group? | Pass | `imf-ra` | Used reference files directly; no unnecessary code. | |
| CAT-01 | Find the IMF indicator for real GDP growth. | Pass | `imf-ra-catalog` | Started with WEO-oriented discovery. | |
| DATA-01 | Pull the IMF data for inflation. | Pass | `imf-ra-data` | Did not invent an indicator; routed through discovery or clarification first. | |
| E2E-01 | Find the correct IMF series for monthly exchange rates for Japan, then download it for 2018-2024 in long CSV format. | Pass | `imf-ra-catalog` | Resolved identifier first, then moved to download flow. | |
```

Recommended note style:

- copy the original query exactly as written in the test table,
- cite the key trajectory checkpoint,
- mention any clarification asked,
- mention any policy violation if the case fails.

---

## 10. Maintenance notes

- Keep this file concise enough for routine review, but broad enough to cover routing, behavior, and guardrails.
- If a case is only about activation, keep it in the smoke-test section rather than duplicating a full feature test.
- If a new policy is added to a skill, add at least one focused case here with an explicit expected behavior reference and trajectory evidence target.
- Do not add chart-related cases until `imf-ra-charts` is implemented.
