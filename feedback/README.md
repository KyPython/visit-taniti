# Guerrilla feedback workflow (Task 1)

## Rubric (what WGU wants)

| Part | Required? |
|---|---|
| **D1** Summarize qualitative feedback + mark **actionable vs not** | Yes — written |
| **D2** Explain how you incorporate actionable feedback | Yes — written |
| **E** Prototype **must include** the actionable fixes | Yes — **implement**, not notes-only |

So: **collect → classify → implement actionable → document all in Word.**  
Taste-only / out-of-scope items: document + justify why **not** implemented.

Task 2 peer Panopto reviews are separate (formal). This folder is for Task 1 **guerrilla** (friends/family on phone).

---

## Phone → Cursor (easy path)

1. On iPhone open **Files** → **iCloud Drive** → **Visit Taniti Feedback** → **inbox**
2. Have the person use the site: https://visit-taniti-seven.vercel.app/
3. Record a **Voice Memo** (or video) of them thinking aloud while doing the 3 tasks in `PROTOCOL.md`
4. Share the memo → **Save to Files** → that `inbox` folder  
   (or drop a Notes export `.txt` in the same inbox)
5. On Mac run:

```bash
cd ~/visit-taniti/feedback
./ingest.sh
```

6. Tell Cursor: *“Read `~/visit-taniti/feedback/transcripts` and `IMPLEMENT.md` — update the prototype + Task 1 Part D.”*

---

## Folders

| Path | Purpose |
|---|---|
| `inbox/` | Drop audio/video/txt from phone (iCloud-synced) |
| `transcripts/` | Markdown Cursor reads |
| `decisions/` | Actionable vs not per tester |
| `processed/` | Originals after ingest |
| `IMPLEMENT.md` | Queue of code changes to ship |

Local clone of site: `~/visit-taniti`  
Monorepo copy: `apps/demos/portfolio-labs/taniti-tourism`
