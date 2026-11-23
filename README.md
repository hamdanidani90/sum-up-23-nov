# Sum up 23 November 2026's world news in one image

Entry for the make.fun bounty
[Sum up 23 November's world news in one image](https://make.fun/bounty/news-image-20261123)
— total prize $100 for 50 places, 1st place $20, paid in USDC on Solana.
Account: @dani-hamdani.

## How to run

Requires Python 3.13, standard library only (no external packages).

```sh
python3 main.py
```

The program writes one image to `/output/entry.png` when `/output`
exists (the competition runtime), otherwise to `output/entry.png`
next to `main.py`. An explicit path can also be given:

```sh
python3 main.py output/entry.png
```

The program needs no network. It is deterministic: running it twice
produces byte-identical output.

## The image

1024 x 1024 PNG, "THE WORLD TODAY — Monday, 23 November 2026",
six stories in a 2 x 3 grid. Each story names its region/topic,
gives a short headline and a 1–2 sentence summary, and is worded
from the sources below. Claims that are contested are attributed
(for example, "President Zelenskyy said … sank …", while Libyan
officials described the ship as severely damaged).

## Stories and sources

All six stories were reported on Monday, 23 November 2026.

1. **COP31 ends with no deal (Antalya, Türkiye).** UN climate
   talks closed after two weeks with no overall pact; the draft
   omitted fossil fuels and the EU rejected it. UN Secretary-General
   António Guterres called it "deeply disappointing". It was the
   longest COP ever.
   Sources: UN News — https://news.un.org/en/story/2026/11/1168855
   ; CNN — https://www.cnn.com/2026/11/22/climate/cop31-summit-collapses-in-fossil-fuel-failure?cid=external-feeds_iluminar_meta
   ; Reuters (Erdogan statement, 23 Nov) — https://www.reuters.com/sustainability/cop/turkeys-erdogan-says-cop31-laid-groundwork-more-climate-talks-despite-lack-deal-2026-11-23/

2. **Ukraine hits Russian ships in Libya (Benghazi).** President
   Zelenskyy said on Monday that seven Ukrainian sea drones sank
   the Russian corvette Merkury in Benghazi and hit the cargo ship
   MV Angara; a Ka-27 helicopter was destroyed. Libyan officials
   said at least 10 people were wounded.
   Sources: AP via WVLT — https://www.wvlt.tv/2026/11/23/zelenskyy-hails-ukraines-attack-russian-warship-docked-naval-base-libya/
   ; CNN — https://www.cnn.com/2026/11/22/africa/russian-vessel-libya-suspected-drone-attack-intl?cid=external-feeds_iluminar_meta

3. **Asian chip stocks slide.** South Korea's Kospi fell as much
   as 5.8% on Monday before closing down 3.3%. Samsung fell 3.1%
   and SK Hynix 2.5% after a Wall Street rout driven by doubts
   over AI spending.
   Source: Algenom daily briefing, 23 Nov 2026 — https://www.algenom.com/news

4. **Iran strikes widen; tankers hit (Middle East).** President
   Trump said on Monday that Iran wants a deal but not one
   acceptable to him. Iranian attacks hit a civilian site in
   Bahrain, injuring two, and at least three tankers were
   attacked in the Strait of Hormuz.
   Sources: Just Security Early Edition, 23 Nov 2026 — https://www.justsecurity.org/165610/early-edition-november-23-2026/
   ; Nexus Europa — https://nexuseuropa.eu/en/top-news/2026-11-23-0000

5. **Delta outage delays 1,600 flights (USA).** A weight-and-balance
   system outage delayed more than 1,600 Delta flights to and from
   Atlanta as Thanksgiving travel began. About 49% of Delta flights
   on Sunday were delayed by more than 15 minutes.
   Source: Frequent Business Traveler, 23 Nov 2026 — https://www.frequentbusinesstraveler.com/2026/11/george-on-monday-requiem-for-the-penny-delta-says-outage-that-delayed-over-1600-flights-has-been-resolved-trump-signs-common-cents-act-pilot-who-thwarted-1994-hijacking-of-fedex-dc-10-dies-at-82/

6. **Lebanese villagers return home (Lebanon).** Villagers began
   returning to destroyed homes in southern Lebanon after an
   Israeli military pullback and the deployment of Lebanese Army
   forces under a pilot ceasefire arrangement.
   Source: News Digest, 23 Nov 2026 — https://digest.leoszeto.com/

## Verification (23 Nov 2026, local test)

- `python3 main.py output/entry.png` — wrote 22,919 bytes.
- Ran twice: both outputs byte-identical
  (SHA-256 `65a7ecd77c3c59566ecfeb50b47ecd948fec24fe868b951e2228aeaa6dd5bbb9`).
- Dimensions 1024 x 1024, size 22,919 bytes, well under the
  1,048,576-byte (1 MiB) limit.
- PNG signature and structure verified; image opened and visually
  checked — all six stories complete, no text cut off.
- Imports in `main.py`: `os`, `struct`, `sys`, `zlib` — standard
  library only. The PNG encoder and the 5x7 bitmap font are
  implemented by hand in the file; no PIL or other external
  library is used.

## Files

- `main.py` — the entry program (stdlib only).
- `README.md` — this file.
- `LICENSE` — MIT.
- `output/entry.png` — preview output from a local run.

## Still needed to submit (not done here)

Per the task instructions, this was NOT submitted and no GitHub
repo was created. To submit, the parent agent still needs to:

1. Create a public GitHub repo (created after the competition
   opened) containing `main.py`, `README.md`, `LICENSE`, and an
   agent session transcript, with an OSI-approved licence (MIT
   is included here).
2. Use the linked Solana wallet (@dani-hamdani — wallet linking
   was in progress at the time of writing) to sign the entry,
   because the bounty requires "Signed in with the wallet that
   gets paid" and a wallet-signed entry message.
3. Submit before Round 2 closes: 24 Nov 2026 07:00 WIB.
   Final: 25 Nov 2026 07:00 WIB.
