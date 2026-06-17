import pandas as pd


def load_and_clean_data():
    # Dataset Load
    df = pd.read_csv("Travel details dataset.csv")

    # Remove duplicates
    df = df.drop_duplicates()

    # Remove extra spaces from text columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    # Convert cost columns to numeric
    if "Accommodation cost" in df.columns:
        df["Accommodation cost"] = pd.to_numeric(
            df["Accommodation cost"],
            errors="coerce"
        )

    if "Transportation cost" in df.columns:
        df["Transportation cost"] = pd.to_numeric(
            df["Transportation cost"],
            errors="coerce"
        )

    # Fill missing values
    df = df.fillna(0)

    # Create Total Cost column
    if (
        "Accommodation cost" in df.columns
        and "Transportation cost" in df.columns
    ):
        df["Total Cost"] = (
            df["Accommodation cost"]
            + df["Transportation cost"]
        )

    return df