import pathlib
from math import ceil
from loguru import logger
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

    n_pages = ceil(count / limit)
    
    for page in range(n_pages):
        if page % 10 == 0:
            logger.info(f"Page {page}/{n_pages - 1}")
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
    
    logger.info(f"Page {page}/{n_pages - 1}")

    df = pd.concat(list_df)
    return df


if __name__ == "__main__":
    df = main(count_limit=40000)
    df.to_csv(pathlib.Path(__file__).parent / DATA_CSV_NAME , index=False)
