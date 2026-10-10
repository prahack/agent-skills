#!/usr/bin/env bash
# Verify an explainer page: the script parses, the page renders, the text passes the STE lint.
# Usage: verify.sh <page.html> [out-dir] [--allow word,word]. Writes <out-dir>/explainer.png, prints the lint.
set -euo pipefail

page="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
out="${2:-${TMPDIR:-/tmp}/explainer-verify}"
here="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$out"

python3 - "$page" "$out/page.js" <<'PY'
import re, sys
html = open(sys.argv[1], encoding="utf-8").read()
blocks = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", html, re.S)
if not blocks:
    sys.exit(f"no inline <script> in {sys.argv[1]}")
open(sys.argv[2], "w", encoding="utf-8").write("\n;\n".join(blocks))
PY
node --check "$out/page.js"
echo "script: parses"

chrome=""
for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" google-chrome chromium chromium-browser; do
  if command -v "$c" >/dev/null 2>&1 || [ -x "$c" ]; then chrome="$c"; break; fi
done
if [ -z "$chrome" ]; then
  echo "render: no Chrome or Chromium found, so no screenshot and no lint of rendered text" >&2
  exit 1
fi
"$chrome" --headless=new --disable-gpu --window-size=1280,2600 --screenshot="$out/explainer.png" "file://$page" 2>/dev/null
"$chrome" --headless=new --disable-gpu --dump-dom "file://$page" 2>/dev/null > "$out/dom.html"
echo "render: $out/explainer.png"

python3 "$here/ste_lint.py" "$out/dom.html" "${@:3}"
