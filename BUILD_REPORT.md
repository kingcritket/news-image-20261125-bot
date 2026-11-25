# Build report — WEDNESDAY, IN FULL (news-image-20261125)

Built from scratch in a clean session: every line of code and every
headline was written fresh here. No file from any earlier entry was copied
or executed; the previous day's entry was read only as a reference for the
render pattern (Pillow locally, copy-only entrypoint in the sandbox).

## Concept

Editorial angle, set before any story was picked: **NO SAFE DISTANCE**.
One sky, one sea — the war arrived in a capital (a drone hits Riyadh's
tallest tower), a shipping lane (a Russian cargo ship hit in the Gulf of
Finland, tankers mined off Hormuz) and NATO's own skies (Russian missiles
landed in Poland, AWACS sent). This answers the benchmark finding that the
generic 43-story newspaper format plateaued in NI24 (round 1: 812/7302,
64.1%; round 2: 4414/9063, 51.3%): one sharp idea, one drawn hero scene,
fewer but more specific stories (37), each dated and sourced.

## Story list (37 total)

Date tags: WED = Wednesday 25 Nov · TUE = Tuesday 24 Nov · MON = Monday
23 Nov. Sources are the outlets the facts were verified against in this
session (each story checked in at least two named outlets).

### Lead (1) — drawn scene

1. **Drone hits Riyadh's tallest tower — 11 wounded** (TUE) — Houthi drone
   struck the 385 m PIF Tower, the Saudi capital's tallest, the second hit
   in under a week (first 19 Nov, no injuries); coalition vowed a
   "decisive" response; Houthis had not claimed it by Tuesday evening.
   Reuters / Saudi Civil Defense / AFP.

### The day's big stories (9)

2. **Zelenskiy: "We did everything right"** (TUE) — Kyiv confirmed the
   drone hit on the Russian cargo ship Sparta II in the Gulf of Finland;
   Norway urged caution. Reuters / Bloomberg.
3. **NATO sends its eyes to Poland** (MON) — AWACS forward-deployed after
   three Russian Kh-101 missiles landed in Poland on Friday. Reuters.
4. **Putin: retaliation "inevitable"** (TUE) — after Ukraine struck Russian
   oil plants. Reuters.
5. **Iran claims a fourth tanker mined** (TUE) — IRGC Navy says a tanker hit
   a mine Tuesday, five claimed in two days. Labelled UNVERIFIED in the
   deck; UKMTO links the incidents to projectiles. IRGC/Tasnim, UKMTO.
6. **CIA and ODNI breached** (TUE) — hackers hit an unclassified
   open-source intelligence network; no classified systems touched;
   attacker unknown. NYT (first) / Reuters / AP.
7. **Sarkozy and Bruni ordered to trial** (TUE) — witness-tampering case
   over the 2007 campaign; 11 defendants face 10 years. Reuters / AFP.
8. **Nvidia gives back a third of its surge** (TUE) — shares −7% Tuesday
   after Monday's +31% jump. Motley Fool / Reuters. (Only the price moves
   are stated; no CEO narrative is asserted — see the NI24 lesson.)
9. **Anthropic slips below its $83 IPO price** (TUE) — −6.5%, four days
   after a $111.50 debut; largest IPO ever, $81.3bn. Fast Company /
   TechCrunch.
10. **Dell doubles sales on AI servers** (TUE) — Q3 revenue $54.9bn;
    AI-server forecast raised to $78bn; $25bn buyback. Bloomberg.

### The day in lines (24)

11. Aden — Houthis 60 km from Aden but will not take it, Yemen's military
    says. Reuters.
12. Tariffs — Trump readies new Section 301 tariffs; China, EU + 14 others
    in view. Reuters.
13. Giuliani — Trump awards the Presidential Medal of Freedom. WaPo.
14. Turkeys — Freedom and Feathers pardoned on Thanksgiving eve. Reuters.
15. Sweden — parliament votes today on Kristersson staying PM. Reuters.
16. Nepal — 5.6 quake shakes Taplejung near the Tibet border; no
    casualties reported. The Hindu / NEMRC.
17. India — BJP and Akali Dal reunite for the 2027 Punjab polls after a
    six-year split. Indian press.
18. Fort Hood — Hasan seeks a stay of execution set for next week. Reuters.
19. O'Hare — radar fault delays flights at Chicago O'Hare, FAA says.
    Reuters.
20. Gaza — US envoy "not certain" military aid to Israel ends this year as
    promised. Reuters.
21. Iraq — Baghdad ordered to run Kurdish oilfields; Kurds reject it.
    Reuters.
22. Women — today is the International Day for the Elimination of Violence
    against Women. UN.
23. Sensex — drops 1,484 points; Nifty below 25,400. Indian press.
24. Germany — Modi holds talks with Chancellor Merz. Indian press.
25. Hormuz — crude shipments through the strait appear down since early
    November. AP.
26. Zimbabwe — a Zimbabwean convicted in South Africa of trying to fight
    in Ukraine. Reuters.
27. Poland — prosecutors say the missiles were made in Dubna, Russia, in
    Oct–Nov 2026. Reuters.
28. UK — ministers consult the public on changing the age of consent. BBC.
29. UK — nuclear test veterans will get the "full truth", PM Burnham says.
    BBC.
30. Sarkozy — appeal verdict in the Libya financing case due 30 November.
    AFP / Reuters.
31. Nvidia — Huang due to testify to the Senate Banking Committee on
    3 December. Reuters.
32. Man Utd — Pochettino fumes at the handling of Yoro's red card. BBC.
33. HP — shares jump 14% after hours; Emma Walmsley named chief executive.
    Press reports.
34. Kyiv — Kyiv says the Sparta II was carrying weapons; Bloomberg could
    not verify the claim. Bloomberg.

### Sport strip (3)

35. Cricket — Donald 85 (32) and Salt 58 (30) power England past Australia
    by 8 wickets; 185 chased in 13.1 overs. ESPNcricinfo / Cricbuzz.
36. Cricket — New Zealand hold India to a draw in the first Test in
    Wellington. ESPNcricinfo.
37. Cricket — Sooryavanshi smashes the fastest List A double hundred.
    BCCI / Cricbuzz.

## Verification

- `python3 build_entry.py` — renders 1024×1024, 214,959 bytes (limit
  1,048,576). Re-render gives the identical sha256
  `13c4947168c9602aad3d12a3a0bb8e59b6bed849a72808c636a574dac2f9a9f0`.
- `MAKEFUN_OUTPUT_DIR=out1 python3 main.py` vs `out2` — both exit 0,
  outputs byte-identical (`cmp` clean), IHDR 1024×1024, and identical to
  the bundled `entry.png`.
- Layout assertions in `build_entry.py` enforce every headline/deck/line
  item inside its line budget and the page bottom inside the 1024 px
  bound; the build fails loudly otherwise (it did three times during
  development, and the text was shortened until it passed).

## Self-audit trail

1. First render: lead block overflowed its height budget (bottom 356 vs
   336) — shrank the lead headline to 32 pt and the deck to 14 pt;
   re-rendered.
2. Deck overflow caught by assertion (Sparta II deck wrapped to 3 lines)
   — shortened all nine middle decks to fit two lines; re-rendered.
3. Visual inspection of the full page: the drawn tower merged into the
   diagonal shadow (both charcoal) and read as a black wedge — redrew the
   scene with the shadow first and the tower on top, cream-outlined, with
   lit windows, a red wound and smoke; re-rendered.
4. Visual inspection: the one-line grid's second lines collided with the
   row below (row height 22 px vs 2×12 px lines) — raised the row height
   to 25 px; re-rendered and re-inspected.
5. Visual inspection of the scene crop: the tower read as a short stub —
   raised its crown to the panel top and shrank the smoke; re-rendered.
6. Final check: every item is Wednesday-dated or carries an explicit
   TUE / MON tag; the footer states the tag key and the sources; the
   Hormuz and Sparta II weapons claims are labelled as claims, not facts;
   no Nvidia CEO narrative is asserted (NI24 lesson).

## Pairwise advantages vs the NI24 top 10

- **One idea in 3 seconds:** "NO SAFE DISTANCE" plus the drawn tower
  scene tells the day's story before any text is read; the winning NI24
  entries were mostly undifferentiated story lists.
- **A drawn hero scene:** the PIF Tower under a red sun is a picture, not
  a wall of type — the benchmark winners that beat us had "drawn scenes"
  and "illustrated heroes".
- **Verified, dated, and honest about claims:** every story carries a day
  tag and named sources; unverified claims (Hormuz mines, Sparta II cargo)
  are labelled as claims, where rivals state single-source claims as fact.
- **Weakness that remains:** the page is still a newspaper grid, so at
  300 px the small lines are texture more than reading; and the tower
  scene, while clear, is flat vector art, not a rich illustration.
