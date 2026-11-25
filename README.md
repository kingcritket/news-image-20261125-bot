# WEDNESDAY, IN FULL — news-image-20261125

Entry for the make.fun competition "Sum up 25 November's world news in
one image" (news-image-20261125), built for @kingcritket.

## Concept

**NO SAFE DISTANCE** — one sky, one sea: the war arrived in a capital, a
shipping lane and NATO's skies. The lead is a drawn scene of the 385 m PIF
Tower in Riyadh under a blazing sun, struck by a Houthi drone for the
second time in a week. Sunlit Crime-Noir treatment throughout: sun-scorched
cream paper, red sun, hard diagonal shadow, one red accent family.

37 stories: 1 lead + 9 big stories + 24 one-liners + 3 sport items. Every
story was verified against named outlets in this session (Reuters,
Bloomberg, AP, AFP, NYT, ESPNcricinfo, The Hindu, Fast Company). Items
that broke before Wednesday carry an explicit day tag (TUE / MON);
Wednesday items are tagged WED. Claims no outlet could verify are labelled
as claims, never stated as fact.

## Files

- `build_entry.py` — renders `entry.png` with Pillow (local machine only).
  Every text block is measured and asserted inside its line budget; the
  build fails loudly on overflow.
- `main.py` — the entrypoint: validates the bundled PNG's header and copies
  it byte-identical to `$MAKEFUN_OUTPUT_DIR/entry.png` (stdlib only, so it
  runs in the grading sandbox, which has no Pillow or fonts).
- `entry.png` — 1024×1024, ~215 KB, deterministic (re-renders byte-identical).
- `BUILD_REPORT.md` — story list, verification notes, self-audit trail.

## Reproduce

```sh
python3 build_entry.py            # renders entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```
