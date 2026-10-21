"""Straumþríhyrningur með raungögnum.

Vindur: Veðurstofa Íslands (stöð 1453, Garðskagaviti).
Straumur: E.U. Copernicus Marine Service Information.
Punktur: 6 sjómílur frá landi á miðinu "Vitarnir saman" á Garðskaga.
"""
import math

import matplotlib.pyplot as plt

from punktur import punktur_a_midi
from straumur import straumur_nuna
from vindur import vindur_nuna

LEEWAY_STUDULL = 0.03   # hluti af hliðarvindi sem rekur bátinn (3 %)


def vektor(hradi, stefna):
    """(austur, norður) fyrir hraða og stefnu í gráðum."""
    horn = math.radians(stefna)
    return hradi * math.sin(horn), hradi * math.cos(horn)


def stefna_vektors(x, y):
    """Stefna vektors í gráðum, 0-360, réttsælis frá norðri."""
    return math.degrees(math.atan2(x, y)) % 360


def reikna(stefna, bat_hradi, vindatt, vindur_kt,
           straumur_stefna, straumur_kt, leeway_studull=LEEWAY_STUDULL):
    """Reiknar straumþríhyrninginn.

    stefna           stefna bátsins (°)
    bat_hradi        hraði bátsins í sjó (kt)
    vindatt          áttin sem vindurinn kemur FRÁ (°)
    vindur_kt        vindhraði (kt)
    straumur_stefna  stefnan sem straumurinn fer TIL (°)
    straumur_kt      straumhraði (kt)
    """
    hx, hy = vektor(bat_hradi, stefna)

    vx, vy = vektor(vindur_kt, vindatt + 180)      # vindurinn FER til
    ex, ey = vektor(1, stefna)                     # einingarvektor stefnis
    langs = vx * ex + vy * ey                      # hluti vindsins eftir bátnum
    lx = leeway_studull * (vx - langs * ex)
    ly = leeway_studull * (vy - langs * ey)

    cx, cy = hx + lx, hy + ly
    stefna_i_sjo = stefna_vektors(cx, cy)
    leeway_horn = (stefna_i_sjo - stefna + 180) % 360 - 180

    sx, sy = vektor(straumur_kt, straumur_stefna)
    rx, ry = cx + sx, cy + sy

    return {
        "hx": hx, "hy": hy, "cx": cx, "cy": cy, "rx": rx, "ry": ry,
        "leeway_horn": leeway_horn,
        "stefna_i_sjo": stefna_i_sjo,
        "raunstefna": stefna_vektors(rx, ry),
        "hradi_yfir_botn": math.hypot(rx, ry),
    }
def reikna_ofugt(oskastefna, bat_hradi, vindatt, vindur_kt,
                  straumur_stefna, straumur_kt):
    stefna = oskastefna
    for i in range(20):
        r = reikna(stefna, bat_hradi, vindatt, vindur_kt,
                   straumur_stefna, straumur_kt)
        villa = (oskastefna - r["raunstefna"] + 180) % 360 - 180
        if abs(villa) < 0.01:
            break
        stefna = stefna - villa
    return stefna % 360, r

def teikna(r, stefna, bat_hradi, straumur_stefna, straumur_kt, titill):
    fig, ax = plt.subplots(figsize=(7, 7))

    def ora(x0, y0, x1, y1, litur, texti):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="->", color=litur, lw=2))
        ax.text((x0 + x1) / 2, (y0 + y1) / 2, texti, color=litur)

    ora(0, 0, r["hx"], r["hy"], "blue", f"Stefna {stefna:03.0f}° {bat_hradi:.1f} kt")
    ora(r["hx"], r["hy"], r["cx"], r["cy"], "orange", f"Drift {r['leeway_horn']:+.1f}°")
    ora(r["cx"], r["cy"], r["rx"], r["ry"], "green",
        f"Straumur {straumur_stefna:03.0f}° {straumur_kt:.2f} kt")
    ora(0, 0, r["rx"], r["ry"], "red",
        f"Raun {r['raunstefna']:03.0f}° {r['hradi_yfir_botn']:.1f} kt")

    xs = [0, r["hx"], r["cx"], r["rx"]]
    ys = [0, r["hy"], r["cy"], r["ry"]]
    ax.set_xlim(min(xs) - 2, max(xs) + 2)
    ax.set_ylim(min(ys) - 2, max(ys) + 2)
    ax.set_aspect("equal")
    ax.set_xlabel("Austur (kt)")
    ax.set_ylabel("Norður (kt)")
    ax.grid(True)
    ax.set_title(titill, fontsize=10)
    plt.show()


def spyrja(texti, sjalfgefid):
    """Spyr notanda um tölu. Enter án svars gefur sjálfgefna gildið."""
    svar = input(f"{texti} [{sjalfgefid}]: ").strip()
    return float(svar.replace(",", ".")) if svar else sjalfgefid


if __name__ == "__main__":
    stefna = spyrja("Stefna bátsins (°)", 90)
    bat_hradi = spyrja("Hraði bátsins í sjó (kt)", 6.0)

    lat, lon = punktur_a_midi(6)
    vindur = vindur_nuna()
    straumur = straumur_nuna(lat, lon)

    r = reikna(stefna, bat_hradi,
               vindur["att"], vindur["hradi_kt"],
               straumur["att_til"], straumur["hradi_kt"])

    print()
    print(f"Punktur: {lat:.4f}, {lon:.4f}")
    print(f"Vindur kl. {vindur['timi']}: {vindur['hradi_ms']} m/s úr {vindur['att']}°")
    print(f"Straumur kl. {straumur['timi']} UTC: {straumur['hradi_kt']:.2f} kt í {straumur['att_til']:.0f}°")
    print(f"Drift: {r['leeway_horn']:+.1f}°  (+ er til stjórnborða, - til bakborða)")
    print(f"Stefna í sjó: {r['stefna_i_sjo']:.0f}°")
    print(f"Raunstefna: {r['raunstefna']:.0f}°")
    print(f"Hraði yfir botn: {r['hradi_yfir_botn']:.1f} kt")

    titill = (f"Vindur {vindur['att']:03.0f}° {vindur['hradi_ms']:.1f} m/s · "
              f"Straumur {straumur['att_til']:03.0f}° {straumur['hradi_kt']:.2f} kt")
    teikna(r, stefna, bat_hradi, straumur["att_til"], straumur["hradi_kt"], titill)