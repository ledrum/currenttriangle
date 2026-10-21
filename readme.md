# Straumþríhyrningur / Current Triangle

**Íslenska** | [English](#english)

Lítið Python-verkefni sem reiknar *straumþríhyrning* fyrir bát úr rauntíma vind- og straumgögnum við Garðskaga: hvaða raunstefnu og hraða yfir botn báturinn fær, og öfugt, hvaða stefnu þarf að stýra til að halda óskaðri raunstefnu.

Þetta er námsverkefni. Ég er að læra Python og smíðaði þetta með hjálp Claude (Anthropic).

> **Fyrirvari:** Gögnin eru líkangögn og mælingar frá einni stöð. Verkefnið er **ekki ætlað til siglinga** og á aldrei að koma í stað réttra siglingagagna og skynsemi.

## Hvað gerir það?

- **Áfram:** þú gefur upp stefnu sem þú stýrir og hraða bátsins í sjó. Forritið reiknar drift (3% af þverkomponent vindsins), stefnu í sjó, raunstefnu og hraða yfir botn.
- **Öfugt:** þú gefur upp óskaða raunstefnu. Forritið leitar að stýrðri stefnu með því að giska, mæla villuna og leiðrétta, allt að 20 umferðir. Ef straumurinn er of sterkur miðað við hraða bátsins er engin lausn til og forritið segir frá því.

Stefnur eru í gráðum réttsælis frá norðri. Vindátt er sú átt sem vindurinn kemur **úr**, straumstefna sú átt sem straumurinn fer **til**.

## Gögn og heimildir

- Vindur: [Veðurstofa Íslands](https://www.vedur.is), stöð 1453 (Garðskagaviti).
- Straumur: [Copernicus Marine Service](https://marine.copernicus.eu), gagnasafnið `cmems_mod_glo_phy_anfc_merged-uv_PT1H-i`.

Báðum heimildum þarf að geta þar sem niðurstöðurnar eru birtar.

## Uppsetning

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Straumgögnin krefjast ókeypis aðgangs hjá Copernicus Marine (innskráning með `copernicusmarine login`).

## Notkun

```bash
python currenttriangle.py          # gagnvirkt, áfram
python uppfaera.py data.json       # sækir gögn og skrifar JSON-skrá
```

`uppfaera.py` er hugsað til að keyra reglulega (t.d. með systemd timer) og skrifa `data.json`, sem vefsíða les og reiknar úr í vafranum.

## Skrár

| Skrá | Hlutverk |
|---|---|
| `currenttriangle.py` | Útreikningar (`reikna`, `reikna_ofugt`) og teikning |
| `vindur.py` | Sækir vindgögn frá Veðurstofunni |
| `straumur.py` | Sækir straumgögn frá Copernicus |
| `punktur.py` | Staðsetningarpunktur |
| `uppfaera.py` | Skrifar `data.json` |
| `reikna_ofugt.py` | Próf fyrir öfuga reikninginn |

## Leyfi

MIT, sjá `LICENSE`.

---

<a id="english"></a>

# currenttriangle (English)

A small Python project that computes a *current triangle* for a boat from live wind and ocean-current data off Garðskagi, Iceland: the course and speed over ground you get from a given heading, and, in reverse, the heading you must steer to make good a desired course over ground.

This is a learning project. I'm learning Python and built it with help from Claude (Anthropic).

> **Disclaimer:** The data is model output and readings from a single station. This project is **not intended for navigation** and must never replace proper nautical information and good judgement.

## What it does

- **Forward:** enter the heading you steer and your boat speed through the water. The program computes drift (3% of the cross-wind component), course through water, course over ground and speed over ground.
- **Inverse:** enter the desired course over ground. The program finds the heading to steer by guessing, measuring the error and correcting, for up to 20 iterations. If the current is too strong for the boat speed there is no solution, and the program says so.

Directions are in degrees clockwise from north. Wind direction is the direction the wind blows **from**; current direction is the direction the current flows **to**.

## Data and attribution

- Wind: [Icelandic Met Office](https://en.vedur.is), station 1453 (Garðskagaviti).
- Current: [Copernicus Marine Service](https://marine.copernicus.eu), dataset `cmems_mod_glo_phy_anfc_merged-uv_PT1H-i`.

Both sources must be credited wherever results are published.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The current data requires a free Copernicus Marine account (log in with `copernicusmarine login`).

## Usage

```bash
python currenttriangle.py          # interactive, forward
python uppfaera.py data.json       # fetches data and writes a JSON file
```

`uppfaera.py` is meant to run on a schedule (for example a systemd timer) and write `data.json`, which a web page reads and computes from in the browser.

## License

MIT, see `LICENSE`.
