# ASD-STE100 Simplified Technical English

The rules the explainer's visible text follows. Source: ASD-STE100 Issue 9
(January 2025), about 900 approved words and 53 writing rules. The dictionary
itself is licensed by ASD and is not reproduced here; when a word's status is
unsure, take the substitution below or a plainer word.

## What the rules cover

Every sentence a reader sees: headings, body, table cells, panel text, quiz
questions, answers and reasons, button labels. Names stay exactly as the source
writes them and are exempt: product and file names, paths, commands, flags,
code, field names and identifiers.

## Words

- Use one word for one meaning, and keep it. Pick the word once (`start` for a
  process, `operate` for a running system, `examine` for a check) and use only
  that word for that meaning on the whole page.
- **Technical nouns** of the subject are allowed: `server`, `queue`, `invoice`,
  `sensor`.
- **Technical verbs** of the subject are allowed where no approved verb carries the
  meaning, for example `compile`, `install` or `run` for software. Say in the
  report which ones the page relies on.
- Noun clusters have three words or fewer. Break a longer one with `of` or `for`.

| Write | Not |
| --- | --- |
| make, make sure | create, ensure, verify |
| examine | check (verb), inspect, review |
| receive | get, obtain |
| start | launch, kick off, trigger |
| stop | halt, abort, kill |
| use | utilize, leverage, employ |
| show | display, indicate, depict |
| necessary, must | need, needed, require (as a requirement) |
| if an error occurs; is not satisfactory | fail, fails |
| keep | retain, store (as a verb), hold |
| remove | delete (unless it is a command name), tear down |
| put back | restore (unless it is a command name), revert |
| continue | carry on, proceed, resume |
| about | approximately, around |
| thus | therefore, so (as a connector) |
| for example | e.g., such as |

## Verbs

- Allowed forms: infinitive, imperative, simple present, simple past, simple
  future, and the past participle as an adjective.
- No `-ing` verb forms. An `-ing` word is allowed only as a technical noun or as
  part of one (`load balancing`, `user onboarding`).
- No auxiliary chains (`will have been`, `would be able to`).
- Active voice. Passive only in description, and only when the agent is unknown.
- No phrasal verbs: `set up` becomes `prepare` or `install`, `find out` becomes
  `find`, `carry on` becomes `continue`.

## Sentences and paragraphs

- Procedural sentence (an instruction): 20 words or fewer, imperative, one
  instruction per sentence.
- Descriptive sentence: 25 words or fewer, one topic.
- Paragraph: one topic, six sentences or fewer.
- Keep the articles and the subject: `The service reads the file`, not
  `Reads file`.
- Use a vertical list for a sequence or for more than three items.
- No contractions, no idioms, no metaphors.
- A warning or caution starts with the command: `Do not edit a generated file.`
  Then one sentence on the result.

## Questions and labels

Quiz and question-and-answer sections keep the form of a question. Button labels
are short imperatives (`Next`, `Back`, `Start again`). Feedback words are `Correct.`
and `Incorrect.`

## Conformance

A page written to these rules is a rewrite against STE, not output from a
licensed STE checker such as HyperSTE. Say so in the report.
