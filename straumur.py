import copernicusmarine

DATASET = "cmems_mod_glo_phy_anfc_merged-uv_PT1H-i_202211"

ds = copernicusmarine.open_dataset(dataset_id=DATASET)
print(ds)