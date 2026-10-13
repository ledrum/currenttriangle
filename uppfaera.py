"""Sækir vind og straum og skrifar niðurstöðuna í JSON-skrá fyrir vefsíðuna."""
import json
import os
import sys
from datetime import datetime, timezone

from punktur import punktur_a_midi
from straumur import straumur_nuna
from vindur import vindur_nuna


def main(slod):
    lat, lon = punktur_a_midi(6)
    vindur = vindur_nuna()
    straumur = straumur_nuna(lat, lon)

    gogn = {
        "uppfaert": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "punktur": {"lat": lat, "lon": lon},
        "vindur": {
            "hradi_ms": vindur["hradi_ms"],
            "hradi_kt": vindur["hradi_kt"],
            "att": vindur["att"],          # áttin sem vindurinn kemur FRÁ
            "timi": vindur["timi"],
        },
        "straumur": {
            "hradi_kt": straumur["hradi_kt"],
            "att_til": straumur["att_til"],  # stefnan sem straumurinn fer TIL
            "sjavarfoll_kt": straumur["sjavarfoll_kt"],
            "timi": straumur["timi"],
        },
    }

    # Skrifa í bráðabirgðaskrá og skipta svo, svo vefsíðan sjái aldrei hálfskrifaða skrá
    tmp = slod + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(gogn, f, ensure_ascii=False, indent=2, default=float)
    os.replace(tmp, slod)


if __name__ == "__main__":
    main(sys.argv[1])