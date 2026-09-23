def fetch_contract_files(portfolio_id: str) -> str:
    """
    Fetches unique contract files from the API and returns them as a formatted
    text string.

    Args:
        portfolio_id (str): The process ID to filter by
            (e.g., 'CO1.BDOS.10764169')

    Returns:
        str: A markdown table containing distinct file names, sizes,
        and extensions.
    """
    import pandas as pd
    import requests

    url = (
        "https://www.datos.gov.co/resource/dmgg-8hin.json"
        f'?$where=proceso="{portfolio_id}"'
    )

    response = requests.get(url)

    if response.status_code != 200 or not response.json():
        return "No files found for the provided ID."

    df = pd.DataFrame(response.json())

    required_cols = {
        "nombre_archivo": "File Name",
        "tamanno_archivo": "Size (Bytes)",
        "extensi_n": "Extension",
    }

    available_cols = [
        col
        for col in required_cols.keys()
        if col in df.columns
    ]

    if not available_cols:
        return (
            "Expected file metadata columns are missing "
            "from the API response."
        )

    df_distinct = (
        df
        .drop_duplicates(subset=["nombre_archivo"])[available_cols]
        .rename(columns=required_cols)
    )

    return df_distinct.to_string(index=False)
