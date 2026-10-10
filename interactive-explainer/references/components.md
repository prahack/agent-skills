# Components

Each section of [../assets/template.html](../assets/template.html): what it
teaches, the data it reads, the function that renders it, and the known traps.
Every section is data-driven: change the data, keep the renderer.

## Page frame

- **Tokens.** Colours live on `:root`, redefined under
  `@media (prefers-color-scheme: dark)` guarded by `:root:not([data-theme="light"])`,
  and again under `:root[data-theme="dark"]`. `--z1` to `--z4` (each with a
  `-soft` partner) are the subject's areas. Give each area one token and use that
  token for the area in every section.
- **Sticky bar** of section links, one per section kept.
- **`codeify(text)`** escapes text and wraps paths and file names in `<code>`.
  Pass every data string through it or `esc`, never raw into `innerHTML`.
- **`store`** wraps `localStorage` in `try/catch`. A `file://` page in a private
  window throws on access.

## Model

Three to five cards (`.facts`), each a leading concept with one or two sentences.
These are the words the rest of the page builds on; the glossary repeats them.

## Architecture diagram (`drawArch`)

Teaches what exists and how it connects.

- `ZONES`: `{x, y, w, h, c, t}`, dashed areas for each place things live. The
  legend is built from the zones.
- `NODES`: `{key: {x, y, w, h, c, t, s, d, dashed?}}`. `t` title, `s` subtitle,
  `d` panel description. `dashed` marks an optional component or one present in
  one variant only.
- `EDGES`: `[from, to, description, dashed?]`. The array index plus one is the
  badge number. Point each arrow from the component that starts the connection.
- Click a node: `focusNode` dims everything else and lists its connections. Click
  a badge or a list item: `focusEdge`. `resetArch` restores the view. Nodes and
  badges answer Enter and Space.
- Set the SVG `viewBox` height to the lowest zone plus 30.

Traps:

- Keep the detail panel **below** the diagram. Beside it, the panel squeezes the
  SVG below its `min-width` and cuts off the right-hand zones.
- Keep a zone title short enough for its zone width; a long one is clipped.
- Badges are placed by searching along each line for a point outside every node
  and at least 24 px from earlier badges, then 17 px, then anywhere outside a
  node. Keep that three-pass search. A single midpoint lands on node labels.
- Lay nodes so the busiest node sits beside the nodes it connects to most. A line
  through a third node is hidden under it, which is acceptable; its badge is not.

## Process map (`renderLanes`, `selectProcess`)

Teaches which process does what, and in which order.

- `LANES`: `{title, hint, items: [key]}`, read left to right. Lane `n` takes the
  colour `--z(n)`.
- `PROCESSES`: `{key: {name, file, what, when, inputs: [[name, meaning]], steps,
  produces, fails, links: [key], note?, isNew?}}`. A step is a string, or
  `[variant, text]` to tag it with a variant pill.
- The panel shows steps, when it starts, inputs, result, error behaviour and
  related processes as chips that jump to each other.
- The **exploration counter** above the lanes counts the processes the reader
  opened, kept in `store`, and says when all are explored.

## Step-through walkthrough (`initJourney`, `drawStep`)

Teaches one end-to-end run as a story. This is the main gamified piece.

- `ACTORS`: up to six `[name, subtitle]`, drawn as a row of boxes.
- `STEPS`: `{ph, from, to, label, t, b: [sentence]}`. `from` and `to` index
  `ACTORS`; equal values draw a loop on one actor. `ph` groups steps into phase
  buttons.
- Controls: Back, Next (it becomes `Start again` on the last step), a progress
  track of clickable segments, phase pills, and the arrow keys while the panel is
  in view.
- Twelve to eighteen steps for a real subject. Fewer skips detail; more loses the
  reader.

## Comparison toggle (`initCompare`, `showCmp`)

`CMP`: `{variantName: [[heading, text]]}`. Give every variant the same headings
in the same order, so a reader can flip and compare one cell at a time. Two to
four variants.

## Reference tables

Static HTML tables inside `.tablewrap` (scrolls on a phone). Columns that answer
"what is it, where does it live, who changes it, what comes next".

## Glossary (`renderTerms`)

`TERMS`: `[term, definition, source]`. The filter matches all three fields. The
source column shows where the term lives in the subject.

## Quiz (`renderQuiz`)

`QUIZ`: `[question, [options], correctIndex, reason]`. One answer per question
locks it, marks the correct option, shows the reason and updates the score line.
Ask what a person would get wrong; a question nobody misses teaches nothing.

## Questions and answers (`renderFaq`)

`FAQ`: `[question, [answer sentence]]`, rendered as `<details>`. Take the
questions from the fact sheet's newcomer list and from what the user asked
during the conversation.

## Accessibility and motion

Components and badges are focusable (`tabindex="0"`, `role="button"`). Panels that
change carry `aria-live="polite"`. The flow animation and smooth scrolling stop
under `prefers-reduced-motion`.
