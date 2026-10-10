<div align="center">

<h3 align="center">agent-skills</h3>

<p align="center">Skills for Claude Code and other agents that load <code>SKILL.md</code> files.</p>

[![Stars][stars-shield]][stars-url] [![Last commit][commit-shield]][commit-url]

</div>

## Skills

| Skill | What it does |
|---|---|
| [`interactive-explainer`](interactive-explainer/SKILL.md) | Builds a single-file HTML page that teaches how a system, process or codebase area works end to end. The page has clickable diagrams, a step-through walkthrough and a quiz, and its text is written in ASD-STE100 Simplified Technical English. |

## Installation

1. Clone the repository.

   ```sh
   git clone https://github.com/prahack/agent-skills.git
   ```

2. Link a skill into your personal skills directory, so a `git pull` updates it.

   ```sh
   ln -s "$PWD/agent-skills/interactive-explainer" ~/.claude/skills/interactive-explainer
   ```

To install it for one project only, link it into that project's `.claude/skills/` directory instead.

## Usage

Ask the agent to explain something end to end, for example:

```text
Build me an interactive explainer of how the checkout service processes an order.
```

The skill reads the real sources, writes the page, then runs `scripts/verify.sh`, which checks that the page script parses, renders a screenshot and lints the text against STE.

<details>
<summary>Requirements for the verify step</summary>

- **Python 3**: extracts the inline script and runs the STE lint (`scripts/ste_lint.py`).
- **Node.js**: `node --check` parses the page script.
- **Google Chrome or Chromium**: renders the headless screenshot.

</details>

[stars-shield]: https://img.shields.io/github/stars/prahack/agent-skills.svg?style=for-the-badge
[stars-url]: https://github.com/prahack/agent-skills/stargazers
[commit-shield]: https://img.shields.io/github/last-commit/prahack/agent-skills.svg?style=for-the-badge
[commit-url]: https://github.com/prahack/agent-skills/commits/main
