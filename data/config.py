from dataclasses import dataclass

BASE_URL = "https://api.thesneakerdatabase.com/v1/sneakers"
DATA_CSV_NAME = "data.csv"
NEW_PRODUCT_PLACEHOLDER_IMAGE_NAME = "New-Product-Placeholder-Default.jpg"
SMALL_IMAGE_URL_KEY = "smallImageUrl"


@dataclass
class DataSchema:
    id: str = "id"    
    brand: str = "brand"
    colorway: str = "colorway"
    gender: str = "gender"
    name: str = "name"
    release_date: str = "releaseDate"
    retail_price: str = "retailPrice"
    shoe: str = "shoe"
    style_id: str = "styleId"
    title: str = "title"
    year: str = "year"
    media: str = "media"
    image_path: str = "image_path"
