SECTOR_NORMALIZATION = {
    # Financial variants → Bank
    "Nifty Financial Services": "Nifty Bank",
    "Nifty Financial Services 25/50": "Nifty Bank",
    "Nifty Financial Services Ex Bank": "Nifty Bank",
    "Nifty Private Bank": "Nifty Bank",
    "Nifty PSU Bank": "Nifty Bank",
    "Nifty MidSmall Financial Services": "Nifty Bank",

    # Healthcare variants → Healthcare
    "Nifty500 Healthcare": "Nifty Healthcare",
    "Nifty MidSmall Healthcare": "Nifty Healthcare",

    # IT variants → IT
    "Nifty MidSmall IT & Telecom": "Nifty IT",
}

def normalize_sector(sector):
    if not sector:
        return None
    return SECTOR_NORMALIZATION.get(sector, sector)

def load_canonical_sectors(path="mapping/canonical_sectors.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())
