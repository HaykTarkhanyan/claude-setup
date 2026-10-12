# non_essential/

Reusable scripts that are not needed to build or present the workshop.

| Script | What it does | When to re-run |
|---|---|---|
| `make_beat.py` | Synthesizes the 60 s beat for the Armenian verse (the box at the top of the handout) and writes `assets/verse-beat.mp3`. No samples; seeded noise (509), so reruns give the same file. | After changing the tempo, chords, or arrangement; then run `python build_standalone.py` to re-inline it. |

Added 2026-10-11 with the verse beat.
