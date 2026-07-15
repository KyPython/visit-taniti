#!/usr/bin/env bash
# Ingest phone voice/text from inbox → transcripts + decision stubs Cursor can read.
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
INBOX="$DIR/inbox"
TRANS="$DIR/transcripts"
PROC="$DIR/processed"
DEC="$DIR/decisions"
VENV="$DIR/.venv"

mkdir -p "$INBOX" "$TRANS" "$PROC" "$DEC"

shopt -s nullglob
files=("$INBOX"/*)
if [[ ${#files[@]} -eq 0 ]]; then
  echo "Inbox empty: $INBOX"
  echo "Drop Voice Memos / .txt from iPhone Files → iCloud Drive → Visit Taniti Feedback → inbox"
  exit 0
fi

ensure_whisper() {
  if [[ -x "$VENV/bin/whisper" ]] || "$VENV/bin/python" -c "import whisper" 2>/dev/null; then
    return 0
  fi
  echo "==> First run: installing openai-whisper into $VENV (one-time)…"
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q -U pip
  "$VENV/bin/pip" install -q openai-whisper
}

transcribe_audio() {
  local src="$1"
  local base="$2"
  local wav="$PROC/${base}.wav"
  local out_txt="$TRANS/${base}.raw.txt"
  ensure_whisper
  ffmpeg -y -i "$src" -ar 16000 -ac 1 "$wav" >/dev/null 2>&1
  "$VENV/bin/whisper" "$wav" --model base --language en --output_dir "$TRANS" --output_format txt >/dev/null
  # whisper names output after wav stem
  if [[ -f "$TRANS/${base}.txt" ]]; then
    mv "$TRANS/${base}.txt" "$out_txt"
  elif [[ -f "$TRANS/${base}.wav.txt" ]]; then
    mv "$TRANS/${base}.wav.txt" "$out_txt"
  fi
  [[ -f "$out_txt" ]] || { echo "Transcription failed for $src" >&2; return 1; }
  echo "$out_txt"
}

stamp="$(date +%Y%m%d-%H%M%S)"

for f in "${files[@]}"; do
  [[ -f "$f" ]] || continue
  name="$(basename "$f")"
  ext="${name##*.}"
  ext_lc="$(printf '%s' "$ext" | tr '[:upper:]' '[:lower:]')"
  stem="${name%.*}"
  safe="$(printf '%s' "$stem" | tr -cs 'A-Za-z0-9._-' '_' )"
  id="${stamp}-${safe}"

  echo "==> Ingesting $name"

  body=""
  case "$ext_lc" in
    txt|md)
      body="$(cat "$f")"
      ;;
    m4a|mp3|wav|aac|caf|mp4|mov|webm)
      raw="$(transcribe_audio "$f" "$id")"
      body="$(cat "$raw")"
      ;;
    *)
      echo "    Skip unsupported type:.$ext_lc"
      continue
      ;;
  esac

  md="$TRANS/${id}.md"
  cat > "$md" <<EOF
# Guerrilla session transcript

- **Source file:** \`$name\`
- **Ingested:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
- **Prototype:** https://visit-taniti-seven.vercel.app/

## Tester

- Name: _(fill first name)_
- Context: _(friend / family / classmate)_

## Raw transcript / notes

$body

## Cursor / human: classify next

Edit \`../decisions/${id}.md\` — mark each point **actionable** or **not**, then update \`../IMPLEMENT.md\`.
EOF

  cat > "$DEC/${id}.md" <<EOF
# Decisions — $id

For each finding from the transcript, choose one:

| Finding | Actionable? | Implement? | Notes |
|---|---|---|---|
| _(example)_ | yes/no | yes/no | |

## Rubric reminder

- **Actionable → implement in prototype** + describe in Task 1 D2/E
- **Not actionable → document + justify** (taste, out of scope, one-month limit)

## Implement queue entries to add

- [ ] …
EOF

  mv "$f" "$PROC/$name"
  echo "    Wrote $md"
  echo "    Wrote $DEC/${id}.md"
done

echo ""
echo "Next: open transcripts/ + decisions/, update IMPLEMENT.md, then tell Cursor to ship actionable items."
