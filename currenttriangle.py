import math
import matplotlib.pyplot as plt

# --- Inntak ---------------------------------------------------------
stefna = 90             # stefna bátsins, þ.e. hvert stefnið vísar (°)
bat_hradi = 6.0         # hraði bátsins í sjó (kt)

straumur_stefna = 180   # stefnan sem straumurinn fer TIL (°)
straumur_hradi = 2.0    # hraði straums (kt)

vindatt = 45            # áttin sem vindurinn kemur FRÁ (°)
vindur_ms = 10.0        # vindhraði (m/s)

leeway_studull = 0.03   # hluti af hliðarvindi sem rekur bátinn (3 %)

MS_I_KT = 1.94384       # 1 m/s = 1,94384 hnútar
vindur_kt = vindur_ms * MS_I_KT

# --- Hjálparföll ----------------------------------------------------
def vektor(hradi, stefna):
    """(austur, norður) fyrir hraða og stefnu í gráðum."""
    horn = math.radians(stefna)
    return hradi * math.sin(horn), hradi * math.cos(horn)

def stefna_vektors(x, y):
    """Stefna vektors í gráðum, 0-360, réttsælis frá norðri."""
    return math.degrees(math.atan2(x, y)) % 360

# --- Útreikningar ---------------------------------------------------
# 1. Báturinn í sjó, í þá stefnu sem stefnið vísar
hx, hy = vektor(bat_hradi, stefna)

# 2. Leeway: aðeins hliðarhluti vindsins rekur bátinn
vindur_x, vindur_y = vektor(vindur_kt, vindatt + 180)   # vindurinn FER til
hx1, hy1 = vektor(1, stefna)                            # einingarvektor stefnis
langs = vindur_x * hx1 + vindur_y * hy1                 # hluti vindsins eftir bátnum
lx = leeway_studull * (vindur_x - langs * hx1)
ly = leeway_studull * (vindur_y - langs * hy1)

# 3. Stefna í gegnum sjó (með leeway)
cx, cy = hx + lx, hy + ly
stefna_i_sjo = stefna_vektors(cx, cy)
leeway_horn = (stefna_i_sjo - stefna + 180) % 360 - 180

# 4. Bæta straumnum við: raunstefna og hraði yfir botn
sx, sy = vektor(straumur_hradi, straumur_stefna)
rx, ry = cx + sx, cy + sy
raunstefna = stefna_vektors(rx, ry)
hradi_yfir_botn = math.hypot(rx, ry)

print(f"Leeway: {leeway_horn:+.1f}°  (+ er til stjórnborða, - til bakborða)")
print(f"Stefna í sjó: {stefna_i_sjo:.0f}°")
print(f"Raunstefna: {raunstefna:.0f}°")
print(f"Hraði yfir botn: {hradi_yfir_botn:.1f} kt")

# --- Teikning -------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 7))

def teikna(x0, y0, x1, y1, litur, texti):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="->", color=litur, lw=2))
    ax.text((x0 + x1) / 2, (y0 + y1) / 2, texti, color=litur)

teikna(0, 0, hx, hy, "blue", f"Stefna {stefna:03d}° {bat_hradi:.1f} kt")
teikna(hx, hy, cx, cy, "orange", f"Leeway {leeway_horn:+.1f}°")
teikna(cx, cy, rx, ry, "green", f"Straumur {straumur_stefna:03d}° {straumur_hradi:.1f} kt")
teikna(0, 0, rx, ry, "red", f"Raun {raunstefna:03.0f}° {hradi_yfir_botn:.1f} kt")

punktar_x = [0, hx, cx, rx]
punktar_y = [0, hy, cy, ry]
ax.set_xlim(min(punktar_x) - 2, max(punktar_x) + 2)
ax.set_ylim(min(punktar_y) - 2, max(punktar_y) + 2)
ax.set_aspect("equal")
ax.set_xlabel("Austur (kt)")
ax.set_ylabel("Norður (kt)")
ax.grid(True)
ax.set_title(f"Vindur {vindatt:03d}° {vindur_ms:.0f} m/s ({vindur_kt:.1f} kt)")
plt.show()