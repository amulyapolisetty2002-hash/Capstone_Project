import pandas as pd

# Split raw address into number & street name
def split_address(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["street_number"] = df["raw_address"].str.extract(r"^(\d+)")
    df["street_name"] = df["raw_address"].str.replace(r"^\d+\s*", "", regex=True)

    return df


# Normalize text (basic normalization only)
def normalize_series(series: pd.Series) -> pd.Series:
    return (
        series.astype(str)
        .str.lower()
        .str.replace(r"[^\w]", " ", regex=True)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip())
    
    
# Expand abbreviations (domain-aware)
def expand_abbreviations(series: pd.Series) -> pd.Series:
    abbreviation_map = {
        # street types
        r"\bst\b": "street",
        r"\bave\b": "avenue",
        r"\bav\b": "avenue",
        r"\bblvd\b": "boulevard",
        r"\brd\b": "road",
        r"\bdr\b": "drive",
        r"\bln\b": "lane",
        r"\bpl\b": "place",
        r"\bctr\b": "center",
        r"\bhwy\b": "highway",

        # domain-specific examples
        r"\bmg\b": "mahatma gandhi"}

    series = series.copy()

    for pattern, replacement in abbreviation_map.items():
        series = series.str.replace(pattern, replacement, regex=True)

    return series


# Remove duplicated suffixes (street street → street)
def remove_duplicate_suffixes(series: pd.Series) -> pd.Series:
    suffixes = [
        "street", "avenue", "boulevard", "road", "drive",
        "lane", "place", "center", "highway"
    ]

    def clean_suffix(text):
        tokens = text.split()
        cleaned = []
        for token in tokens:
            if not cleaned or token != cleaned[-1] or token not in suffixes:
                cleaned.append(token)
        return " ".join(cleaned)

    return series.apply(clean_suffix)


# Clean listings data
def clean_listings(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Remove null postal codes
    df = df[df["postal_code"].notna()]

    # Normalize postal_code
    df["postal_code"] = df["postal_code"].astype(str).str.strip()
    df["postal_code"] = df["postal_code"].apply(lambda x: x.zfill(5) if len(x) < 5 else x)

    # Create zip_prefix
    df["zip_prefix"] = df["postal_code"].str[:3]

    # Split address
    df = split_address(df)

    # Step 1: normalize street
    df["norm_street"] = normalize_series(df["street_name"])

    # Step 2: expand abbreviations
    df["clean_street"] = expand_abbreviations(df["norm_street"])

    # Step 3: remove duplicate suffixes
    df["clean_street"] = remove_duplicate_suffixes(df["clean_street"])

    # Deduplicate using FINAL cleaned street
    df = df.drop_duplicates(subset=["street_number", "clean_street", "zip_prefix"])

    return df.reset_index(drop=True)


# Clean demographics data
def clean_demographics(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df = df[df["zip_code"].notna()]

    df["zip_code"] = df["zip_code"].astype(str).str.strip()
    df["zip_code"] = df["zip_code"].apply(lambda x: x.zfill(5) if len(x) < 5 else x)

    df["zip_prefix"] = df["zip_code"].str[:3]

    return df.reset_index(drop=True)