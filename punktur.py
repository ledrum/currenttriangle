import math

R_SJOMILUR = 3440.065   # radíus jarðar í sjómílum

# Vitarnir á Garðskaga (hnit úr korti)
GAMLI_VITI = (64.082994, -22.693798)   # gamli vitinn (1897), yst á tánni
NYI_VITI = (64.081982, -22.689966)     # nýi vitinn (1944), nokkru innar


def punktur_fra(lat, lon, stefna, sjomilur):
    """Staðsetning sem er `sjomilur` frá (lat, lon) í stefnu `stefna` (°)."""
    d = sjomilur / R_SJOMILUR
    t = math.radians(stefna)
    la1, lo1 = math.radians(lat), math.radians(lon)
    la2 = math.asin(math.sin(la1) * math.cos(d) +
                    math.cos(la1) * math.sin(d) * math.cos(t))
    lo2 = lo1 + math.atan2(math.sin(t) * math.sin(d) * math.cos(la1),
                           math.cos(d) - math.sin(la1) * math.sin(la2))
    return math.degrees(la2), math.degrees(lo2)


def stefna_milli(lat1, lon1, lat2, lon2):
    """Stefna (°) frá punkti 1 til punkts 2."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dl = math.radians(lon2 - lon1)
    x = math.sin(dl) * math.cos(p2)
    y = math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl)
    return math.degrees(math.atan2(x, y)) % 360


def fjarlaegd(lat1, lon1, lat2, lon2):
    """Fjarlægð í sjómílum milli tveggja punkta."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dl = math.radians(lon2 - lon1)
    a = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R_SJOMILUR * math.asin(math.sqrt(a))


def stefna_mids():
    """Stefna miðsins "vitarnir saman", frá vitunum og út á sjó (°)."""
    return stefna_milli(*NYI_VITI, *GAMLI_VITI)


def punktur_a_midi(sjomilur=6):
    """Punktur á miðinu, `sjomilur` frá gamla vitanum (yst á landi)."""
    return punktur_fra(*GAMLI_VITI, stefna_mids(), sjomilur)


if __name__ == "__main__":
    # Keyrist aðeins þegar skráin er keyrð beint, ekki þegar hún er flutt inn
    print(f"Fjarlægð milli vita: {fjarlaegd(*NYI_VITI, *GAMLI_VITI) * 1852:.0f} m")
    print(f"Stefna á miði: {stefna_mids():.1f}°")
    lat, lon = punktur_a_midi(6)
    print(f"6 sjómílur á miði: {lat:.4f}, {lon:.4f}")