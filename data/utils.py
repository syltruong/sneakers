import ast
import re
from math import ceil
from pathlib import Path
from typing import Union

import pandas as pd
import requests
import wget
from loguru import logger

from data.config import (
    BASE_URL,
    DATA_CSV_NAME,
    NEW_PRODUCT_PLACEHOLDER_IMAGE_NAME,
    SMALL_IMAGE_URL_KEY,
    DataSchema,
)


def get_csv_data(count_limit: int = 200) -> pd.DataFrame:
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

    response = requests.get(url=BASE_URL, params={"limit": 10})
    count = min(int(response.json()["count"]), count_limit)

    # 2. Loop through

    limit = min(count, 100)  # limit of returned items per query (< 100)

    list_df = []

    n_pages = ceil(count / limit)

    for page in range(n_pages):
        if page % 10 == 0:
            logger.info(f"Page {page}/{n_pages - 1}")
        response = requests.get(url=BASE_URL, params={"limit": limit, "page": page})

        list_df.append(pd.DataFrame.from_records(response.json()["results"]))

    logger.info(f"Page {page}/{n_pages - 1}")

    df = pd.concat(list_df)
    return df


def load_data_from_csv(
    csv_path: Union[str, Path], schema: DataSchema = DataSchema()
) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df[schema.media] = df[schema.media].apply(ast.literal_eval)
    return df


def download_images(
    df: pd.DataFrame, output_dir: Path, schema: DataSchema = DataSchema()
):

    output_dir.mkdir(parents=True, exist_ok=True)

    for i, row in df.iterrows():
        if i % 50 == 0:
            logger.info(f"Procesing row {i}/{len(df)}")

        id = row[schema.id]
        image_url = row[schema.media][SMALL_IMAGE_URL_KEY]

        if image_url is None:
            # logger.debug(f"Invalid image found for {image_url} | {id}")
            continue

        extension = get_file_extension_from_url(image_url)

        if (extension is None) or (NEW_PRODUCT_PLACEHOLDER_IMAGE_NAME in image_url):
            # logger.debug(f"Invalid image found for {image_url} | {id}")
            continue

        output_path = output_dir / f"{id}.{extension}"
        if output_path.exists():
            output_path.unlink()
        try:
            wget.download(image_url, output_path.as_posix())
        except Exception as e:
            logger.warning(f"{id} | {image_url}")
            logger.warning(e)
            continue


def get_file_extension_from_url(url: str) -> Union[str, None]:

    pattern = r"\.([a-zA-Z]+)\?"

    m = re.search(pattern, url)

    if m is not None:
        return m.group(1)
    else:
        return None
