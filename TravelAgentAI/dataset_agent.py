import pandas as pd


def get_dataset_summary(df):
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns),
        "numeric_columns": list(df.select_dtypes(include="number").columns),
        "text_columns": list(df.select_dtypes(include="object").columns)
    }


def answer_question(df, question):
    q = question.lower()

    # Basic dataset info
    if "row" in q or "record" in q:
        return f"Total rows/records: {df.shape[0]}"

    if "column" in q:
        return f"Total columns: {df.shape[1]}\nColumns: {', '.join(df.columns)}"

    # Male/Female
    gender_cols = [c for c in df.columns if "gender" in c.lower()]
    if gender_cols:
        col = gender_cols[0]
        if "male" in q:
            count = df[df[col].astype(str).str.lower() == "male"].shape[0]
            return f"Total male count: {count}"

        if "female" in q:
            count = df[df[col].astype(str).str.lower() == "female"].shape[0]
            return f"Total female count: {count}"

    # Country/Nationality
    country_cols = [
        c for c in df.columns
        if "country" in c.lower() or "nationality" in c.lower()
    ]
    if ("country" in q or "nationality" in q) and country_cols:
        col = country_cols[0]
        return "Top country/nationality:\n" + df[col].value_counts().head(10).to_string()

    # Vehicle/Transport
    transport_cols = [
        c for c in df.columns
        if "vehicle" in c.lower() or "transport" in c.lower()
    ]
    if ("vehicle" in q or "transport" in q) and transport_cols:
        col = transport_cols[0]
        return "Top vehicle/transport:\n" + df[col].value_counts().head(10).to_string()

    # Most common / popular for any column
    if "most" in q or "popular" in q or "common" in q:
        for col in df.columns:
            if col.lower() in q:
                value = df[col].value_counts().idxmax()
                count = df[col].value_counts().max()
                return f"Most common {col}: {value} ({count} times)"

    # Average for numeric columns
    if "average" in q or "mean" in q:
        for col in df.select_dtypes(include="number").columns:
            if col.lower() in q:
                return f"Average {col}: {round(df[col].mean(), 2)}"

    # Sum for numeric columns
    if "sum" in q or "total" in q:
        for col in df.select_dtypes(include="number").columns:
            if col.lower() in q:
                return f"Total {col}: {round(df[col].sum(), 2)}"

    return (
        "I can answer questions like:\n"
        "- How many rows are there?\n"
        "- How many columns are there?\n"
        "- How many male/female?\n"
        "- Which country is most common?\n"
        "- Which vehicle is most used?\n"
        "- Average of any numeric column\n"
        "- Most common value of any column"
    )