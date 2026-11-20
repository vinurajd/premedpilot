# PremedPilot — Frequently Asked Questions

## Getting started

**What is PremedPilot?**
An AI advising skill for high school students aiming at medical school. It builds a profile of the student, matches it against bundled datasets of BS/MD combined programs and strong undergraduate pre-med pathways, and classifies every option on a five-level probability scale, with commentary on what would move each option up one level.

**What do I receive at the end of a consultation?**
One CSV file, `medical_college_recommendations.csv`, with up to 25 BS/MD rows and up to 25 pre-med pathway rows, plus a short counselor's summary naming the headline takeaways, one or two standout options, and grade-appropriate next steps.

**Which AI assistants can run it?**
Any host that supports the open SKILL.md standard: Claude Code (as a plugin or a skill folder), Gemini CLI, Muse, and other compatible hosts. Installation commands for each are in the README.

**Does it cost anything?**
No. The skill and its datasets are published under the MIT licence. You need your own account with whichever AI host you run it on.

## The consultation

**What information does it ask for?**
Grade level, school district, unweighted and weighted GPA, class rank, SAT or ACT scores (official, or PSAT and predicted scores if that is what you have), extracurriculars such as clinical experience, research, and volunteering, immigration status, and any location or cost preferences. It asks a few questions at a time and skips anything you have already volunteered.

**Why does it ask about immigration status?**
Because it is decisive for eligibility. Many BS/MD programs require U.S. citizenship or permanent residency, so a student on a visa such as H4 or F1 is not eligible for those seats no matter how strong the rest of the profile is. The skill asks plainly, uses the answer only for advising in that conversation, and never guesses it.

**What if I do not know, or do not want to share, one of the answers?**
Say so. The consultation proceeds on the remaining evidence, the gap is recorded, and any classification that depends on the missing field is flagged in the summary so it can be rechecked once the information is known.

**Can I ask about one specific program instead of doing a full consultation?**
Yes. Once a profile exists, you can ask how a score change affects a named program, or ask for a comparison between two schools. The classifications still come from the same datasets and the same scale.

## Classifications

**What are the five classifications?**
Guaranteed, High Probability, Somewhat Probable, Low Probability, and No Chance At All, in that order. Each is reasoned from the specific program's published profile against the specific student's profile. None is assigned generically.

**Does Guaranteed mean I will definitely be admitted?**
No. It means the profile meets or exceeds every known published threshold with a wide margin. It is used sparingly, because true guarantees are rare in selective admissions, and no classification in this skill is a promise of admission.

**Why did a program come out as No Chance At All?**
Usually a hard barrier rather than a weak profile: a score below a program's published floor, a residency restriction the student does not meet, a citizenship requirement, or a grade-level mismatch. The commentary on the row states the reason, and where a barrier can be removed, such as a test score, it says what would restore eligibility.

**What does the commentary column tell me?**
One to three sentences specific to the student, naming the change that would move that program up one classification level: a score target, a class-rank threshold, an experience gap to close.

**What is the difference between the BS/MD and Pre-Med Pathway tracks?**
A BS/MD program links undergraduate admission to a medical school seat, usually with conditions. A pre-med pathway is a strong undergraduate route with no linked seat; the student applies to medical school in the normal way. The CSV keeps the two in separate tracks and never blends them.

## The data

**Where does the program data come from?**
The BS/MD dataset is built from the AAMC Official Guide listings plus direct-entry and early-assurance routes verified on official program websites. The pathways dataset comes from institutional data, College Scorecard, IPEDS, and university Common Data Sets. Every figure carries a source, and figures that could not be verified are marked as such rather than filled in.

**How many programs are covered?**
The current snapshot holds 78 BS/MD programs and 25 pre-med pathways.

**How current is the data?**
The datasets are a snapshot from one admissions cycle; the snapshot date is recorded in each dataset and stated in the delivery. Tuition, cutoffs, and acceptance rates change yearly, so verify any figure that matters with the program itself. If a figure the classification turns on looks stale, or a program you name is missing from the snapshot, the skill verifies that one figure against the program's official page before classifying.

**What does "Not publicly available — verify with program" mean in the CSV?**
The figure could not be verified from a public source, so it was carried through honestly instead of being estimated or left blank. Treat it as an action item: ask the program directly.

**What happens to programs that have closed?**
They stay in the dataset with their status recorded, so the record stays honest, but they are excluded from recommendations entirely. Programs paused for the student's application cycle are excluded for that cycle, and if a student names one directly, the skill explains its status instead of classifying it.

## Privacy and limits

**What happens to the information I share in a consultation?**
It is treated as conversation-specific context, used only for the advising in that conversation.

**Can the skill be wrong?**
Yes, and it is built to be honest about that. Figures can go stale between refreshes, some published figures are a university's own claims rather than audited numbers, and a classification is a calibrated judgment from published data, not a reading of an admissions committee. Use it to build and prioritise a list, then confirm the decisive details with each program.

**Does it replace a school counselor or an admissions consultant?**
No. It gives a family a sourced, structured starting list and a realistic read on competitiveness. School counselors know the student's school context, and programs themselves are the final authority on their own requirements.

## Keeping current

**How do installed copies stay up to date?**
Automatically. At the start of a consultation, the skill checks the repository for a newer dataset, verifies the download against its published SHA-256 hash and the schema, and swaps it in, keeping the previous file as a backup. The check runs at most once a week per installation, and if the repository is unreachable the bundled data is used and its date is stated.

**How is the data itself maintained?**
Program statuses (open, paused, discontinued) are rechecked every two weeks, and the full dataset is refreshed once per admissions cycle: stale figures re-verified, unresolved fields retried, new and closed programs reconciled against the AAMC census. Every change is recorded in the project changelog in the repository.
