from currenttriangle import reikna_ofugt

st, r = reikna_ofugt(0, 5, 0, 0, 90, 2)
print(st, r["hradi_yfir_botn"])   # á að gefa ca. 336.4 og 4.58
# 1. Enginn straumur, enginn vindur: stefnan á að vera óbreytt
print("Próf 1:", reikna_ofugt(90, 5, 0, 0, 0, 0)[0])

# 2. Með vindi: nú kemur drift við sögu
st, r = reikna_ofugt(0, 5, 270, 15, 90, 2)
print("Próf 2:", st, r["raunstefna"], r["hradi_yfir_botn"])

# 3. Straumur sterkari en báturinn: engin lausn
st, r = reikna_ofugt(0, 5, 0, 0, 90, 6)
print("Próf 3:", st, r["raunstefna"])