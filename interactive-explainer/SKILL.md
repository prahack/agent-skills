---
name: interactive-explainer
description: Build an interactive, gamified HTML explainer that teaches how a system, process or codebase area works end to end, written in ASD-STE100 Simplified Technical English with clickable diagrams, a step-through walkthrough and a quiz. Use when the user asks to understand something end to end, asks for an explainer, guide, walkthrough or visual explanation page, or says they want to answer any question about a topic after reading it. Not for a short answer in chat.
---

# Interactive explainer

The reader finishes the page able to answer any question about the subject. Every
section serves that **mastery** bar: a fact the page omits is a question the reader
cannot answer, and a fact the page invents is a wrong answer they will repeat.

[assets/template.html](assets/template.html) is a working explainer filled with
sample data about a fictional online shop. Build from it: keep its CSS tokens and
renderer functions and replace every sample. [references/components.md](references/components.md)
describes each section, its data shape and its traps. [references/ste.md](references/ste.md)
is the writing standard.

## 1. Ground every fact

Read the subject's real sources: code, config, pipelines, READMEs, `--help`
output, contracts. Fan out with an `Explore` agent when the sources span many
directories. Build a fact sheet in the scratchpad with these headings:
components, connections between them, processes (trigger, inputs, steps, result,
error behaviour), one end-to-end run in sequence, variants, stored items, terms,
and the questions a newcomer asks.

**Done when** every fact names the file or command it came from, and the open
unknowns are listed. An unknown stays an unknown on the page, stated as one.

## 2. Choose the sections

Structure is information: a section earns its place when the subject has that
shape. Take them in this order, and drop the ones the facts do not support.

| Section | Include when |
| --- | --- |
| Model: 3 to 5 leading concepts | always |
| Architecture diagram | two or more components connect |
| Process map with detail panel | three or more processes |
| Step-through walkthrough | an end-to-end sequence exists |
| Comparison toggle | the subject has variants |
| Reference tables | states, stored items, settings |
| Glossary with filter | ten or more terms |
| Quiz, 8 to 10 questions | always |
| Questions and answers, 8 or more | always |
| Sources footer | always |

**Done when** each fact on the sheet has a home section, and each section has facts.

## 3. Write in STE

Write every visible sentence to [references/ste.md](references/ste.md): approved
words, active voice, imperatives for instructions, procedural sentences at 20
words or fewer and descriptive ones at 25 or fewer. Names, paths, commands and
code stay exactly as the source writes them.

Each quiz question tests a fact from the page, and each wrong option is a real
misunderstanding the reader could hold. The reason shown after an answer teaches
the fact again.

## 4. Build the page

Copy `assets/template.html`. Replace the data objects between the two `SAMPLE DATA`
and `renderers` markers (`ZONES`, `NODES`, `EDGES`, `LANES`, `PROCESSES`, `ACTORS`,
`STEPS`, `CMP`, `TERMS`, `QUIZ`, `FAQ`), the static sections, the title and the
footer. Delete the markup, data and init call of any section step 2 dropped.
Remove the `SAMPLE DATA` comment. Keep one self-contained file: inline CSS and
JS, Google Fonts only, no other network request.

Save it where the user names. With no location named, save it beside the
project, outside the repository, so it adds no untracked file to their branch.

## 5. Verify, then report

Run `scripts/verify.sh <file> <out-dir>`. It checks the script parses, renders
the page headless to a screenshot, and runs the STE lint. Read the screenshot
once and fix what it shows: a clipped diagram, a badge on a label, text over the
frame. Fix each STE finding, or confirm it is a technical noun or verb of the
subject and run again with `--allow word,word` so only open findings remain.

**Done when** the script parses, the screenshot shows every diagram whole, no
sample text remains, and the lint reports nothing you have not confirmed. Report
the path, the sections the page has, and in one line offer to publish it as an
Artifact.
