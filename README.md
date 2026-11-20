# PremedPilot

An AI-powered **BS/MD & pre-med pathway advisor** for high school students navigating the path to medical school, packaged as a portable agent skill.

A three-role advising system (Compass → Scholar + Pathfinder) builds a student persona, matches it against bundled datasets of BS/MD combined programs and strong undergraduate pre-med pathways, classifies every recommendation on a calibrated five-level scale (Guaranteed / High Probability / Somewhat Probable / Low Probability / No Chance At All) with commentary on what would move it up one level, and delivers one collated CSV with a counselor's summary.

The skill is a single `SKILL.md` folder, the open Agent Skills standard, so the same package installs in Claude Code, Gemini CLI, Muse, and other compatible hosts. The skill began as an opencode three-agent build; its full three-agent instructions are preserved in `skills/premedpilot/references/agent-instructions.md`.

## Install

### Claude Code

```
/plugin marketplace add vinurajd/premedpilot
/plugin install premedpilot@vinurajd-skills
```

### Muse

Ask your Muse: "Install the PremedPilot skill from the latest release of vinurajd/premedpilot on GitHub." Your Muse downloads the skill zip from the repository's Releases page and places the `premedpilot` folder in your custom skills. After that, dataset updates arrive automatically through the skill's built-in update check.

### Gemini CLI

```bash
gemini skills install https://github.com/vinurajd/premedpilot.git --path skills/premedpilot --consent
```

Or copy `skills/premedpilot/` into `~/.gemini/skills/` or `~/.agents/skills/`.

### Muse

Copy `skills/premedpilot/` into `~/workspace/custom-skills/`.

### Any other SKILL.md host

Copy `skills/premedpilot/` into the host's skills directory (for example `~/.claude/skills/` for direct Claude Code use without the plugin).

## Use

Start with a full consultation:

> Follow the instructions and help me find the right medical college for a student persona

Then ask direct questions once the persona is built:

> I'm a junior in Ohio with a 3.9 UW GPA, a 1460 SAT, and two years of hospital volunteering. What are my best BS/MD options?

> My SAT is 1520. How does that change my chances at Brown PLME and Case Western PPSP?

> Compare my fit at UT Austin vs Texas A&M for pre-med

Questions about how it works, what the classifications mean, or how current the data is? See the [FAQ](skills/premedpilot/FAQ.md), which also ships inside the skill folder itself.

## What's inside

```
├── .claude-plugin/
│   ├── marketplace.json   # makes this repo a Claude Code marketplace
│   └── plugin.json        # the plugin manifest
├── marketplace.json       # same catalog, at the root for hosts that read it there
└── skills/
    └── premedpilot/
        ├── SKILL.md                          # the skill (all hosts)
        ├── references/
        │   ├── dataset_bsmd_programs.json    # BS/MD programs (78 in this snapshot)
        │   ├── dataset_premed_pathways.json  # pre-med pathways (25 in this snapshot)
        │   └── agent-instructions.md         # original three-agent instructions, verbatim
        └── scripts/
            └── generate_csv.py               # collates the two analysis files into the final CSV
```

## Knowledge updates

The two datasets are maintained in this repository, and installed copies of the skill pull updates from here. Each refresh is also published as a GitHub Release carrying a downloadable skill zip; those release downloads are the counted install channel, so please take the zip from Releases rather than cloning when you only want the skill. The skill's `scripts/update_knowledge.py` checks `references/knowledge-manifest.json` at most once a week, verifies each changed dataset against its published SHA-256 hash and the schema, and swaps it in, keeping the previous file as a backup. Offline, the bundled data is used and its date is stated to the student. Maintainers refresh the data once per admissions cycle under the protocol in the SKILL.md, and regenerate the manifest with `scripts/build_manifest.py` after every change.

## Data

- **BS/MD programs**: AAMC 2025–2026 Official Guide to BS/MD Programs, Bridge2MD, Archimedes Advising, official program websites.
- **Pre-med pathways**: institutional data, College Scorecard, IPEDS, university Common Data Sets.
- **Tuition and residency**: Texas Higher Education Coordinating Board (SB 1528), individual university bursar pages.

The bundled datasets are a snapshot from one admissions cycle. Figures change yearly; the skill verifies a stale or missing figure against the program's official page before relying on it, labels estimates as estimates, and never fabricates a number.

## License

MIT — see `LICENSE`.
