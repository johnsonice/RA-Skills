# IMF RA skill family — audit report (2026-05-09)

Structural and behavioral audit of the four IMF RA skills, run against branch `feat/chengyu_0509_auto-testing-steps`. Findings are evidence-backed (logged test failure, production bug, or specific file/line in the source). Severity is set by either logged test failure / production bug or by structural drift caught in audit.

Evidence sources:
- Skill bodies under `.claude/skills/imf-ra*/SKILL.md` and adjacent `references/`, `scripts/`, `templates/`.
- Test harness at `tests/auto_test_instructions.md`.
- Run log at `tests/issue_tracking/ra_skills_autotest_2026-05-09.md`.
- Bug log at `tests/issue_tracking/issues.md`.
- Reference CSVs and helper scripts under `.claude/skills/imf-ra-catalog/` and `.claude/skills/imf-ra/`.

---

## Tier 1 — Critical (test evidence or known production bug)

### 1.1 `catalog_search.py` has a vintage bias that fights the LIVE-first policy
- **Evidence:** `ra_skills_autotest_2026-05-09.md` notes CAT-01 passed *"despite helper-script vintage bias"*; CAT-05 **failed** for skipping the LIVE-vs-vintage clarification on `NGDPD`.
- **Where:** `.claude/skills/imf-ra-catalog/scripts/catalog_search.py:60-208` — `database_sort_key` (line 73) and the fallback (line 186) sort vintage resources ahead of `*_LIVE`. Conflicts with the policy in `imf-ra-catalog/SKILL.md:51`.
- **Impact:** "Lucky pass" today, real failure tomorrow. The policy says LIVE-first; the helper says vintage-first; whichever wins depends on the input.

### 1.2 LIVE-vs-vintage clarification gate is buried mid-body
- **Evidence:** Same CAT-05 failure as 1.1. The relevant rule is at `imf-ra-catalog/SKILL.md:51` — a single line in the middle of a long "Priority Policy" block, easy to skim past.
- **Impact:** Even when the script returns a vintage code, the SKILL doesn't enforce a *stop-and-confirm* gate, so the agent silently proceeds.

### 1.3 Country-group codes are being used as series codes (production bug)
- **Evidence:** `tests/issue_tracking/issues.md:11-13` — `COUNTRY=G200` is being passed as a series code instead of expanding to member countries.
- **Where:** No expansion rule exists in `imf-ra-data/SKILL.md`'s key-build step. The umbrella mentions `weo_country_groups.py members` but doesn't mandate it for G-prefix inputs.
- **Coverage:** No test case in the harness exercises this path → regression can recur.

### 1.4 Two test prompts are unrunnable in fresh sessions
- **Evidence:** `ra_skills_autotest_2026-05-09.md` marks DATA-04 and DATA-10 as **Needs follow-up** because both prompts implicitly assume prior `database_id` context. The harness explicitly requires fresh sessions.
- **Where:** `tests/auto_test_instructions.md` — DATA-04 and DATA-10 prompt blocks.
- **Impact:** The behaviors these cases are *meant* to test (metadata-to-options for DATA-04, large-ALL warning for DATA-10) are never actually exercised.

### 1.5 `imf-ra-charts` is a placeholder masquerading as a working skill
- **Evidence:** `imf-ra-charts/SKILL.md` body is 24 lines and contains *"For now, defer to the user's intent"* (line 24). `imf-ra-charts/references/chart-tool-usage.md` is a stub: every section starts with *"> Document …"*. README admits it is *"scaffolded — not yet implemented"*. No test coverage.
- **Impact:** The frontmatter `description:` reads like a working skill — Claude will route chart requests here and find only deferred placeholders. Could result in invented chart commands.

---

## Tier 2 — Structural drift / redundancy

### 2.1 Terminology drift: "series" vs "indicator"
- **Evidence:**
  - `imf-ra/SKILL.md:14` — `(database, series, frequency, geo)`
  - `imf-ra-catalog/SKILL.md:8` — `(database, series, frequency, geo)`
  - `README.md:10` — same.
  - But `idata_full_indicators_list.csv` has columns `database_name, indicator_code, indicator_name`; both `templates/idata_template.md` files use "indicator"; `imf-ra-data/SKILL.md` and `catalog-conventions.md` consistently say "indicator".
- **Impact:** Two distinct nouns for the same catalog concept across the family. Routing prose says "search for the right indicator" but the tuple notation says "series".
- **Note:** Keep "series" *only* where it refers to time-series **values** (rows of fetched data) — that usage is correct.

### 2.2 Umbrella `imf-ra/SKILL.md` duplicates `references/conventions.md`
- **Evidence:**
  - `imf-ra/SKILL.md:25` ≈ `conventions.md:6-7` ("when to write code")
  - `imf-ra/SKILL.md:27` ≈ `conventions.md:11-13` ("material uncertainty")
  - `imf-ra/SKILL.md:42` re-states what conventions.md already covers.
- **Impact:** Same policy lives in two files. Future updates risk drift; both copies cost context every time the umbrella loads.

### 2.3 `imf-ra-data/SKILL.md` "Before you fetch" section is redundant
- **Evidence:** `imf-ra-data/SKILL.md:195-202` re-states country codes / frequencies / time range / SDK setup that are already covered by §"Skill relationships" (lines 10-17) and the family conventions.
- **Impact:** ~8 lines of pure restatement. `imf-ra-data/SKILL.md` is the longest of the four; this redundancy directly inflates context cost.

### 2.4 Helper-script-vs-CSV messaging is mixed
- **Evidence:**
  - `imf-ra/SKILL.md:25` says *"Use Python only when it is genuinely needed"*.
  - `imf-ra-catalog/SKILL.md:33,35` says the same.
  - But the family ships large helper scripts: `weo_country_groups.py` (231 lines) and `catalog_search.py` (252 lines).
  - **Quantification:** ~80% of `weo_country_groups.py` is convenience over `grep`. `catalog_search.py search` is genuinely irreducible (tokenized scoring + 11-entry synonyms map + WEO-priority fallback at lines 105-208) — Claude *cannot* easily replicate it.
- **Impact:** The current SKILL prose is too uniform. Some subcommands (`catalog_search.py search`) should be **mandatory** for the 81K-row indicators CSV; others (`weo_country_groups.py summary | countries | memberships`) are pure convenience. Conflating them produces inconsistent agent behavior.

### 2.5 Indicators-CSV context-cost is undocumented
- **Evidence:** `idata_full_indicators_list.csv` measured at **8.8 MB / 81,035 rows / ~60-80K tokens**. Nothing in `imf-ra-catalog/SKILL.md` or `catalog-conventions.md` warns against loading it whole.
- **Impact:** A fresh agent could trivially burn most of its context window by reading the file directly — exactly the kind of trap a SKILL is supposed to prevent.

### 2.6 Frontmatter `description:` boundaries are implicit
- **Evidence:** `imf-ra-catalog/SKILL.md:3` doesn't say "do not use for fetching"; `imf-ra-data/SKILL.md:3` doesn't say "only when the (database_id, indicator_code) is already known"; `imf-ra-charts/SKILL.md:3` doesn't say "only when a chart-tool target is named". Verbs overlap (`fetch / pull / load / get / chart`).
- **Impact:** Routing collisions. *"I need current account data for advanced economies"* could plausibly fire any of the three.

---

## Tier 3 — Polish

### 3.1 `imf-ra-data` Step 5 / Step 6 ordering is awkward
- **Evidence:** `imf-ra-data/SKILL.md:121-145` — Step 5 builds the iData key, Step 6 then asks for output format. Output format is an input the user should be asked about *before* you finish gathering inputs, not after.
- **Impact:** Pedagogically odd; the final fetch can feel like a re-prompt.

### 3.2 Cross-skill backlinks are asymmetric
- **Evidence:** Umbrella `imf-ra/SKILL.md:21,23` uses real markdown links to references. Workers refer to the umbrella in **prose only** — `imf-ra-catalog/SKILL.md:12` ("See the umbrella `imf-ra` for shared conventions"), `imf-ra-charts/SKILL.md:12` (same), no clickable link.
- **Impact:** Minor. Asymmetric reference graph in the docs.

### 3.3 Country-group CSV redundancy
- **Evidence:** `imf-ra/references/Country Group/csv/`:
  - `group_dummies_idata.csv` (198 × 51 group columns) and `group_dummies_old_codes.csv` (198 × 51 cols) encode **identical** membership in different naming.
  - `country_group_composition.csv` (1,945 rows) repeats `grouptype, groupcode, groupname, groupcode_s, groupname_s` in every row.
  - `countries.csv` and both `group_dummies_*.csv` redundantly re-encode the 4-column country identity in every row.
- **Impact:** Source-of-truth ambiguity — three files all encode the same axis. If one is stale, no test catches it. (Helper script reads `country_group_composition.csv` and `countries.csv`; the dummies files might be unused.)

### 3.4 Coverage gap: ambiguous-multi-database matches
- **Evidence:** CAT-03 tests one ambiguous concept; no case covers the same concept living in 2+ databases (e.g. real GDP growth in WEO *and* IFS).
- **Impact:** Cross-database disambiguation is untested.

### 3.5 Coverage gap: charts skill assertion case
- **Evidence:** `tests/auto_test_instructions.md:9` explicitly excludes chart cases ("not implemented yet"). Zero coverage.
- **Impact:** No regression detection if the charts skill starts inventing commands or auto-firing on vague inputs.

### 3.6 Fragile passes worth noting
- **CAT-01:** passed but the rerun log explicitly notes it was *despite* the vintage bias — i.e. not robust.
- **SMOKE-04:** marked Pass but only verified that the agent stopped, not that the follow-up clarification correctly resolves the dimensions.
- **E2E-01:** marked Pass but the test confirms the *presence* of a hand-off, not that state is preserved across catalog → data.

---

## Cross-cutting observations

- **Templates vs CSV columns:** perfect alignment — both `idata_template.md` files match the actual CSV headers exactly. Not a defect.
- **Dataset CSV (`idata_full_datasets_list.csv`):** 76 KB / 669 rows / clean. Loadable in context. No issues.
- **`check_references.sh`:** validates SKILL→reference markdown links resolve. Currently passes. Useful but limited — does not validate frontmatter, does not validate that referenced sections actually exist within target files, does not catch terminology drift.
- **Helper-script verdicts:**
  - `catalog_search.py search` — irreducible value, keep and emphasize as default for indicator lookups.
  - `catalog_search.py datasets / latest-weo` — borderline, could be replaced with grep.
  - `weo_country_groups.py groups / members / group-a` — kept for the 52-entry `GROUP_ALIASES` map (the only non-trivial logic).
  - `weo_country_groups.py summary / countries / memberships` — convenience; CSV reads suffice.
  - `fetch_idata.py` — SDK wrapper, not a reference-data helper; out of scope but does encode irreducible refreshable-format pivot logic.

---

## Summary by severity

| Severity | Count | Areas |
|---|---|---|
| **Critical** (test/prod evidence) | 5 | LIVE-vs-vintage policy and helper-script bias, country-group expansion, untestable prompts, charts placeholder |
| **Structural** (drift / redundancy) | 6 | Terminology, umbrella duplication, mixed messaging, context cost, frontmatter boundaries |
| **Polish** | 5 + 1 | Step ordering, backlinks, CSV dedup, coverage gaps, fragile passes |

**Highest-leverage single fix:** flip the vintage sort in `catalog_search.py` and add a clear stop-and-confirm gate in `imf-ra-catalog/SKILL.md`. That alone closes the only logged Fail (CAT-05) and makes CAT-01 a robust pass instead of a lucky one.
