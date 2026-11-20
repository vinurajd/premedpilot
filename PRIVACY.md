# PremedPilot — Privacy

PremedPilot is an instruction-only skill. It runs inside the AI host the user
already uses (for example Claude, ChatGPT, Gemini, or a local agent). The
author operates no server, no database, and no analytics for it.

## What it works with

To advise, the skill uses details the user types into the conversation:
grade level, GPA, test scores, class rank, extracurricular activities,
immigration status, and preferences such as location and cost. It does not
ask for names, email addresses, or postal addresses, and it does not need
them to work.

Everything shared in the conversation is treated as conversation-specific
context, used only to produce the advising output in that conversation.

## Storage and retention

The skill stores nothing and sends nothing to the author. Its outputs (the
analysis files and the recommendations CSV) are created in the user's own
environment, under the user's control, and the user decides what to keep or
delete. No data received through the skill is retained by the author, for
any length of time.

## Network access

The skill's only network behaviour is in the other direction: it may fetch
updated program datasets from this public GitHub repository, checking the
published SHA-256 hash before using a download. That request carries none
of the user's data.

## Bundled data

The datasets bundled with the skill describe colleges and BS/MD programs
from public sources. They contain no personal data.

## Who it is for

PremedPilot is intended for high school students, including students under
18, and for their parents.

## Contact

Questions about this policy: vinurajd@gmail.com
