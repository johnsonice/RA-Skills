# RA Skills — Internal Showcase

A 10-slide brief feeding the ppt-master skill. Audience is mixed (RAs, technical reviewers, leadership). Tone: confident, concrete, light on jargon. Through-line: **from chatbot to colleague** — AI that does the work, not just talks about it.

---

## Slide 1 — Title

**Title:** RA Skills
**Subtitle:** Local AI agents for IMF Research Assistant workflows
**Tagline:** From chatbot to colleague.
**Footer:** Internal showcase · 2026

**Visual:** Clean cover. Suggested motif: a terminal window blending into a spreadsheet/chart, signaling "AI inside the analyst's actual tools." Reuse `assets/hero.png` if useful.

---

## Slide 2 — The Problem: AI Today Lives in a Chat Window

**Takeaway:** Chat-based AI fragments the research workflow.

**Bullets:**
- Today's AI is a separate browser tab. The RA copies a question in, copies the answer out, and stitches the rest together by hand.
- Real research work happens in iData, Excel, Stata, Jupyter — *not* in the chat window.
- The chatbot can't see your SDK, can't open your data, can't reach institutional conventions, can't reuse what it learned yesterday.
- Result: every query is a fresh copy-paste loop. Institutional knowledge stays in heads and email threads.

**Visual:** Split-screen mock — left: a chat tab with a question. Right: a real RA workspace (iData call, Excel sheet, chart). A red dashed line between them labeled "manual copy-paste."

---

## Slide 3 — The Vision: Local Agents That Automate the Work

**Takeaway:** Move from *AI you talk to* → *AI that does the work* — running locally, alongside the tools the RA already uses.

**Bullets:**
- An agent that **lives where the data lives** — inside the analyst's repo, with the SDK, the catalogs, and the conventions one cd away.
- That **speaks the SDK** natively — no copy-pasting code, no API guessing, no re-explaining country codes.
- That **encodes institutional knowledge** — WEO group memberships, LIVE-vs-vintage rules, retired endpoints — so the same question doesn't get re-asked every Monday.
- That **chains its own steps** — discovery → fetch → tidy → chart — without the human stitching it together.

**Visual:** Three icons in a row — *Local* (laptop), *Native* (Python/SDK), *Institutional* (book/CSV). Arrow underneath: "chat → colleague."

---

## Slide 4 — Introducing RA Skills

**Takeaway:** A family of project-local Claude Code skills for IMF Research Assistants — plain English in, real iData out.

**Bullets:**
- Lives under `.claude/skills/` in the analyst's repo. **Project-local**, not a global install — auto-loaded only inside RA-Skills.
- Built on Anthropic Claude Code + Claude Skills. No new app to learn; the analyst's existing Claude Code becomes the workspace.
- **Input:** natural language. *"Pull WEO real GDP growth for G20 countries, 2010–present."*
- **Output:** a refreshable Excel, a wide/long CSV, or (soon) a chart — produced by the agent, sitting in the analyst's working directory.

**Visual:** Single-line flow — `"plain English request"` → `RA Skills agent` → `tidy Excel + chart`. Underneath the agent box, four small skill tiles: `imf-ra`, `imf-ra-catalog`, `imf-ra-data`, `imf-ra-charts`.

---

## Slide 5 — Architecture: A Family of Four Sibling Skills

**Takeaway:** Four small, focused skills that chain — not one monolith.

**Bullets:**
- `imf-ra` — umbrella. Loads shared conventions: country codes, frequencies, dates, SDK setup. **No pillar-specific logic.**
- `imf-ra-catalog` — discovery. Plain English → `(database, indicator, frequency, geo)`.
- `imf-ra-data` — retrieval. Calls the internal Python SDK to fetch the resolved series.
- `imf-ra-charts` — chart handoff. *Scaffolded; not yet wired to the internal chart tool.*
- **Siblings, not nested.** Workers reference each other directly — DRY through cross-references, not through a heavy orchestrator.

**Visual:** Horizontal chain with arrows: `imf-ra (conventions)` → `imf-ra-catalog` → `imf-ra-data` → `imf-ra-charts (WIP)`. Caption underneath: "every skill is one folder + one SKILL.md."

---

## Slide 6 — Design Principle: CSVs Are the Source of Truth

**Takeaway:** The agent answers from files, not from memory. No identifier hallucinations.

**Bullets:**
- **669 datasets** and **81,035 indicators** live in CSVs the agent reads directly — `idata_full_datasets_list.csv`, `idata_full_indicators_list.csv`.
- WEO country-group memberships (Advanced Economies, EMDE, G7, ASEAN-5, …) live in `country_group_composition.csv` — *exact* membership truth.
- Same pattern for conventions, SDK reference, retired endpoints. Markdown for prose, CSV for structured truth.
- Result: **no model drift on identifiers**, **reproducible answers**, **auditable provenance** — every claim points to a file.
- *Policy:* if a CSV answers the question, read it directly. Write code only for aggregation, joins, repeated filtering.

**Visual:** Three stacked rows — `669 datasets`, `81,035 indicators`, `country groups`. Each row points to a CSV icon. A small "no hallucination" stamp.

---

## Slide 7 — Capability 1: Natural Language → Exact Identifier

**Takeaway:** The catalog skill turns a sentence into the four things you actually need to call the SDK.

**Walk-through:**

> *"Pull WEO real GDP growth for G20 countries, 2010–present."*

The agent resolves to:

| Field | Value |
|---|---|
| Database | `WEO_LIVE` |
| Indicator | `NGDP_RPCH` |
| Frequency | `A` (annual) |
| Geo | `G20` member ISO3 list, auto-expanded |

**Bullets:**
- **LIVE vs vintage** is explicit. Latest data unless the user says *"April 2024 WEO vintage"* — then it locks to that snapshot.
- **Country groups expand by name or code** — *"advanced economies"* → `G110` member list.
- **Ambiguous?** The agent surfaces top candidates with distinguishing notes and asks. Never guesses an identifier.
- **Retired endpoints** (EcOS) are refused with a pointer to the current iData equivalent.

**Visual:** Left: a chat bubble with the user query. Right: the resolved 4-tuple table. Connecting arrow labeled "catalog."

---

## Slide 8 — Capability 2: Pull Data Locally via the iData SDK

**Takeaway:** Resolved query → real time-series, on the analyst's machine, in the format they need.

**Bullets:**
- **Seven-step protocol:** catalog handoff → explore dimensions → resolve country/frequency/time range → build iData key → confirm output format → fetch → return tidy file.
- Calls the pre-built internal wrapper `fetch_idata.py` — no ad-hoc SDK code, no re-implementing private-access boilerplate.
- **Three output formats**, user picks:
  - **Refreshable RA Excel** — enriched with country names, ISO3, IFS codes; updates on refresh.
  - **Wide** CSV/Excel — dates as rows, countries as columns (raw API shape).
  - **Long** CSV/Excel — one observation per row (analytics-ready).
- **Data stays local.** The SDK runs on the analyst's machine; no cloud round-trip for IMF data.
- EcOS retired — iData is the exclusive pathway.

**Visual:** Vertical pipeline: `(database, indicator, freq, geo)` → `fetch_idata.py` → three output icons (Excel, wide CSV, long CSV). Caption: "data never leaves your laptop."

---

## Slide 9 — End-to-End Workflow Walkthrough

**Takeaway:** One sentence in → tidy panel out. What the RA *didn't* have to do.

**Sequence (left-to-right or top-to-bottom):**

1. **RA types:** *"Pull WEO real GDP growth for G20 countries, 2010–present."*
2. **`imf-ra-catalog` resolves:** `WEO_LIVE / NGDP_RPCH / A / G20-members`. Confirms with the RA.
3. **`imf-ra-data` fetches:** 7-step protocol → `fetch_idata.py` → refreshable Excel with countries enriched.
4. **`imf-ra-charts` (soon) hands off** to the internal chart tool.
5. **RA opens the Excel** — ready for Stata, the chart tool, or the next memo.

**What the RA never had to do:**
- Look up an indicator code.
- Remember which ISO3s are in the G20.
- Read the iData SDK docs.
- Reformat a wide-API response into a long panel.
- Re-ask the same question they asked last Monday.

**Visual:** A horizontal "swimlane" — top row: RA actions (one sentence + one Enter). Middle row: skill chain doing the work. Bottom row: time saved.

---

## Slide 10 — What's Next

**Takeaway:** This is Phase 1. The roadmap turns the same chain into a full RA cockpit.

**Bullets:**
- **`imf-ra-charts` wiring.** Connect to the internal chart tool — close the discovery → fetch → chart loop end-to-end.
- **More sources beyond iData.** Haver (priority), Bloomberg, Datastream, EDSS — add as additional `imf-ra-*` workers, no rework of the chain.
- **Curated overlays.** Institutional knowledge as data — *"use IFS quarterly, not WEO annual, for X"* — captured in `overlays/` so the agent stops re-learning it.
- **Downstream automation.** Notebook templates, reusable modules, scheduled refresh pipelines.
- **Closing line:** *From chatbot to colleague — and the colleague keeps getting better.*

**Visual:** Roadmap timeline — Phase 1 (done: catalog + data), Phase 2 (charts + more sources), Phase 3 (overlays + automation). End slide also doubles as the closer.

---

## Style notes for ppt-master

- **Color palette:** professional/institutional — deep blue + warm accent (gold or coral). Not pastel, not playful.
- **Type:** clean sans-serif; large slide titles, restrained body.
- **Density:** keep each slide to one big idea + 3–5 supporting bullets. Use the visual side of the slide for the diagram.
- **Diagrams over decoration:** every slide that mentions a chain or pipeline gets a real diagram, not generic stock art.
- **No emojis. No clip art.** Use simple geometric icons if needed.
