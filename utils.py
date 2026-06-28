import numpy as np
import pandas as pd
import re

def load_data(file_name: str) -> pd.DataFrame:

    def handle_factor(factor: str, clean_data = None, raw_data: pd.DataFrame = None)-> pd.DataFrame:
    
        date_col = f"DATE-{factor}"
        val_col = f"VAL-{factor}"
        factor_data = raw_data[[date_col, val_col]].copy()
        factor_data[date_col] = pd.to_datetime(factor_data[date_col]).dt.date
        factor_data = factor_data[~pd.isnull(factor_data[val_col])]

        if clean_data is None:
            clean_data = pd.DataFrame()
            clean_data["DATE"] = factor_data[date_col]
            clean_data[val_col] = factor_data[val_col]
        else: 
            clean_data = clean_data.merge(factor_data, left_on="DATE", right_on=date_col, how="outer")
            clean_data["DATE"] = np.where(
                pd.isnull(clean_data["DATE"]),
                clean_data[date_col],
                clean_data["DATE"]
            )
            clean_data = clean_data.drop(date_col, axis=1)

        return clean_data

    
    data = pd.read_csv(file_name)
    factors = [re.sub("DATE-","",c) for c in data.columns if "DATE" in c]
    clean_data = None
    for f in factors:
        clean_data = handle_factor(f, clean_data, data)

    clean_data.set_index("DATE", inplace=True)
    clean_data.rename(columns = {c: re.sub("VAL-", "", c) for c in clean_data.columns}, inplace=True)
    clean_data.ffill(inplace=True)
    clean_data.bfill(inplace=True)
    return clean_data