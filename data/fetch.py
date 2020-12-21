import pathlib
from math import ceil

import pandas as pd
import requests

from data.config import BASE_URL, DATA_CSV_NAME


def main(count_limit: int = 200) -> pd.DataFrame:
    """
    Download sneaker data from the API

    Parameters
    ----------
    count_limit : int, optional
        by default 200

    Returns
    -------
    pd.DataFrame
        sneaker data as dataframe
    """
    
    # 1. Probe number of items
    
    response = requests.get(url=BASE_URL, params={"limit":10})
    count = min(int(response.json()["count"]), count_limit)
    
    
    # 2. Loop through
    
    limit = min(count, 100)  # limit of returned items per query (< 100)

    list_df = []

    for page in range(ceil(count / limit)):
        print(page)
        response = requests.get(
            url=BASE_URL,
            params={
                "limit": limit,
                "page": page
            }
        )

        list_df.append(
            pd.DataFrame.from_records(response.json()["results"])
        )
    
    df = pd.concat(list_df)
    return df


if __name__ == "__main__":
    df = main(count_limit=40000)
    df.to_csv(pathlib.Path(__file__).parent / DATA_CSV_NAME , index=False)
