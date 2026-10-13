"""Straumur frá Copernicus Marine (global líkan, um 9 km, yfirborðsstraumar).

Gagnasafn: klukkutíma yfirborðsstraumar sem sameina haf, sjávarföll og bylgjur.
Heimild: E.U. Copernicus Marine Service Information.
"""
import math
from datetime import datetime, timedelta, timezone

import copernicusmarine

DATASET = "cmems_mod_glo_phy_anfc_merged-uv_PT1H-i"
MS_I_KT = 1.94384    # 1 m/s = 1,94384 hnútar
RAMMI = 0.25         # hálf breidd svæðisins sem sótt er (gráður)


def hradi_og_att(u, v):
    """Hraði (m/s) og stefna (°) sem straumurinn fer TIL, út frá austur- og norðurhluta."""
    return math.hypot(u, v), math.degrees(math.atan2(u, v)) % 360


def straumur_nuna(lat, lon):
    """Nýjasti straumur næst punktinum (lat, lon).

    Skilar orðabók með:
      hradi_kt      heildarstraumur í hnútum
      hradi_ms      heildarstraumur í m/s
      att_til       stefnan sem straumurinn fer TIL (°)
      sjavarfoll_kt sá hluti sem er sjávarföll, í hnútum
      timi          tími gagnanna (UTC)
      grid_lat, grid_lon  hnit rist-reitsins sem var notaður
    """
    nu = datetime.now(timezone.utc).replace(tzinfo=None)
    snid = "%Y-%m-%dT%H:%M:%S"

    ds = copernicusmarine.open_dataset(
        dataset_id=DATASET,
        variables=["utotal", "vtotal", "utide", "vtide"],
        minimum_latitude=lat - RAMMI, maximum_latitude=lat + RAMMI,
        minimum_longitude=lon - RAMMI, maximum_longitude=lon + RAMMI,
        start_datetime=(nu - timedelta(hours=2)).strftime(snid),
        end_datetime=(nu + timedelta(hours=2)).strftime(snid),
    )
    p = ds.sel(latitude=lat, longitude=lon, time=nu, method="nearest").squeeze().load()

    u, v = float(p["utotal"]), float(p["vtotal"])
    if math.isnan(u) or math.isnan(v):
        raise ValueError("Engin gögn í næsta reit (líklega land). Prófaðu punkt lengra frá landi.")

    hradi_ms, att_til = hradi_og_att(u, v)
    sjavarfoll_ms, _ = hradi_og_att(float(p["utide"]), float(p["vtide"]))
    return {
        "hradi_ms": hradi_ms,
        "hradi_kt": hradi_ms * MS_I_KT,
        "att_til": att_til,
        "sjavarfoll_kt": sjavarfoll_ms * MS_I_KT,
        "timi": str(p["time"].values)[:16],
        "grid_lat": float(p["latitude"]),
        "grid_lon": float(p["longitude"]),
    }


if __name__ == "__main__":
    from punktur import punktur_a_midi

    lat, lon = punktur_a_midi(6)
    s = straumur_nuna(lat, lon)
    print(f"Punktur á miði: {lat:.4f}, {lon:.4f}")
    print(f"Næsti reitur:   {s['grid_lat']:.3f}, {s['grid_lon']:.3f}")
    print(f"Straumur kl. {s['timi']} UTC:")
    print(f"  {s['hradi_kt']:.2f} kt ({s['hradi_ms']:.2f} m/s) í {s['att_til']:.0f}°")
    print(f"  þar af sjávarföll: {s['sjavarfoll_kt']:.2f} kt")