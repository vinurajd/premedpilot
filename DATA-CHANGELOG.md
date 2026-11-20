# Data changelog — PremedPilot

## 2026-11-19 — Initial completion build

- BS/MD dataset: all 44 listed programs completed from a mostly stub state. 240 of 264 sourced fields verified from official program pages and the AAMC guide; 24 remain needs_verification with reasons recorded (chiefly acceptance rates that programs do not publish).
- Real-world changes caught and recorded: Rice/Baylor Medical Scholars discontinued (last class admitted 2022); University of Miami HPME and the GW St. Bonaventure route discontinued; SUNY Downstate BA-MD paused for the 2027–28 cycle; University of South Carolina program renamed AU-M.D.; 12 program durations corrected; Brown PLME figures upgraded to Brown's official published values and a stale test-optional claim corrected.
- Pathways dataset: 16 programs completed and 9 added (UT Austin, Texas A&M, UT Dallas, Baylor, University of Houston, Stanford, Harvard, Case Western, Rochester), for 25 total. 140 of 150 sourced fields verified; the 10 open fields are expected GPA at schools that publish no average GPA.
- Refresh protocol and staleness scanner added to the skill (`scripts/refresh_check.py`); dataset validator added (`scripts/validate_datasets.py`).

## 2026-11-19 — Repository pull mechanism added

- Installed skills now pull knowledge updates from the canonical repository: `scripts/update_knowledge.py` fetches `knowledge-manifest.json`, verifies changed datasets by SHA-256 and schema, swaps them in with a backup kept, and gates itself to one check per 7 days via a local stamp. Offline or unreachable repository leaves the bundled data in place and never fails a consultation.
- Maintainer side: `scripts/build_manifest.py` regenerates the manifest after any dataset change; a monthly scheduled check re-verifies flagged program statuses and runs the full cycle refresh when a dataset comes due.

## 2026-11-19 — BS/MD census expansion (44 → 78 programs)

- The AAMC 2025-2026 list contains exactly the 44 schools already in the dataset, so the dataset was AAMC-complete; the advertised 80+ counts arise only when undergraduate-partner routes are counted individually. At the dataset's one-entry-per-medical-school granularity, the sources support 78.
- Added 34 programs: 12 direct-entry routes schools advertise but AAMC does not list, and 22 early-assurance or sophomore-entry equivalents, each confirmed on official pages. 146 of the additions' 204 sourced fields verified; the 58 left open are unpublished acceptance rates and test floors, figures at the three discontinued additions, and structurally multi-institution fee fields.
- Three additions are themselves discontinued and are coded as such with stats left unverified: Marshall's accelerated BS/MD, Boston University's Seven-Year SMED, and WashU's University Scholars Program in Medicine. Northwestern and UNR entries were built for their live successor routes (NUPSP; PiM plus Assured Seat).
- Dataset totals now: 78 programs, 386 of 468 sourced fields verified. One flag carried forward: USC School of Medicine Greenville's early assurance route rests on partner-university pages and AAMC's 2024-cycle listing rather than the medical school's own current site; it is the first target of the monthly status recheck.

## 2026-11-19 — Renamed to PremedPilot

- The skill is renamed from Med School eCounselor to PremedPilot (slug: premedpilot), Vinuraj's choice, ahead of first publication. The skill folder, plugin and marketplace entries, README, and the knowledge-update address (now the vinurajd/premedpilot repository) all carry the new name. Datasets and advising content are unchanged.

## 2026-11-19 — End-to-end skill test and fixes

- First cold end-to-end test of the installed skill (fictional Ohio junior persona, run from the installed copy alone): the full flow completed, producing 25 BS/MD + 25 pathway rows, all classifications on the exact five-level scale, no discontinued or paused program selected, calibration held (no Guaranteed assigned).
- Fixes from the test's friction report: both datasets now carry a structured `program_status` field (BS/MD: 5 discontinued, 1 paused, 72 live; pathways: 25 live) and selection, validation, and the refresh scanner key off it instead of note text. `generate_csv.py` flattens sourced `{status, value, source}` objects itself, reads `program_duration_years`, and parses the pathways dataset's single `annual_fees` field. SKILL.md now prescribes the fallback when immigration status stays unknown, defines the student's cycle for paused programs, scopes selection by entry route and residency, and states the analysis-file flattening rule explicitly.

## 2026-11-19 — FAQ added; status rechecks move to a two-week cadence

- FAQ.md added at the package root, answering the questions students and parents ask most: the consultation, the five classifications, the data and its limits, eligibility, privacy, and updates. The README links to it.
- Maintainer status rechecks (discontinued/paused programs) move from monthly to every two weeks, Vinuraj's direction. The full dataset refresh stays once per admissions cycle.

## 2026-11-19 — FAQ embedded in the skill; PremedPilot --help

- FAQ.md moved from the package root into the skill folder (skills/premedpilot/FAQ.md), so the skill is self-contained wherever it is installed. The README links to its new home.
- SKILL.md gains a Help section: when a user types `PremedPilot --help`, or asks how to use the skill, the assistant presents the FAQ instead of starting a consultation, then offers to begin.

## 2026-11-19 — Second cold test (H4 high-scorer persona) and fixes

- Second cold end-to-end test (H4 Texas junior, 4.0 GPA, SAT 1540, top 5%): the citizenship axis passed with no failure — every citizenship-barred program in the CSV is No Chance At All with the eligibility reason, none classified on academics alone. Guaranteed discipline held: three statutory Texas pathway Guaranteed, a floated BS/MD Guaranteed (Nova Southeastern) pushed back to High Probability on review, zero BS/MD Guaranteed.
- SKILL.md now prescribes citizenship handling and slot priority (eligible programs first, then barred programs by relevance, the rest counted in the summary), the commentary contract for the two end labels, and the pause-cycle mapping (a pause stated for a school year covers students who apply during it).
- generate_csv.py splits fees on "nonresident" phrasing too; Berkeley and UCLA rows had been mislabelled as private in the out-of-state column.
- UT Austin's automatic-admission threshold updated to the top 5% for currently announced cycles (verified on UT Austin's official admissions page); the University of Houston entry now records the same Texas Education Code §51.803 statute the dataset already carried for the other Texas publics.
- All sourced fields normalised to the full {status, value, source} shape (82 BS/MD needs_verification objects gained a source key; null values became empty strings), and the validator now enforces that shape. An entry_route field is scheduled for the annual refresh; until then the route is read from each entry's notes, with the entry's own application timing governing any ambiguity.
