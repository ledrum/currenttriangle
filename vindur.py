"""Vindur frá Veðurstofu Íslands (opin gögn, ODC-BY: Veðurstofa Íslands).

Sækir nýjustu klukkutímaathugun frá sjálfvirkri stöð.
"""
import json
import urllib.request

URL = "https://api.vedur.is/weather/observations/aws/hour/latest?parameters=basic"
GARDSKAGAVITI = 1453   # stöðvarnúmer

MS_I_KT = 1.94384      # 1 m/s = 1,94384 hnútar


def saekja(url):
    beidni = urllib.request.Request(url, headers={"User-Agent": "currenttriangle (nam)"})
    with urllib.request.urlopen(beidni, timeout=20) as svar:
        return json.load(svar)


def vindur_nuna(stod=GARDSKAGAVITI):
    """Nýjasta vindathugun frá stöðinni.

    Skilar orðabók með:
      hradi_ms  vindhraði í m/s
      hradi_kt  vindhraði í hnútum
      hviður_ms mesta hviða í m/s (getur verið None)
      att       áttin sem vindurinn kemur FRÁ, í gráðum
      att_txt   áttin sem texti, t.d. "SSE"
      timi      tími athugunar
    """
    gogn = saekja(URL)
    faerslur = [f for f in gogn if f.get("station") == stod]
    if not faerslur:
        raise ValueError(f"Engin gögn fundust fyrir stöð {stod}")
    f = faerslur[0]
    if f.get("f") is None or f.get("d") is None:
        raise ValueError(f"Stöð {stod} er ekki með vindmælingu í nýjustu athugun")
    return {
        "hradi_ms": f["f"],
        "hradi_kt": f["f"] * MS_I_KT,
        "hviður_ms": f.get("fg"),
        "att": f["d"],
        "att_txt": f.get("d_txt"),
        "timi": f["time"],
    }


if __name__ == "__main__":
    v = vindur_nuna()
    print(f"Vindur við Garðskagavita kl. {v['timi']}:")
    print(f"  {v['hradi_ms']} m/s ({v['hradi_kt']:.1f} kt) úr {v['att']}° ({v['att_txt']})")
    if v["hviður_ms"] is not None:
        print(f"  hviður allt að {v['hviður_ms']} m/s")