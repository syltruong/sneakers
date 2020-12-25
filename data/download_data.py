import argparse
from pathlib import Path
from data.config import DATA_CSV_NAME
from data.utils import get_csv_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_dir", "-o", type=str, required=True)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)


    df = get_csv_data(count_limit=40000)
    df.to_csv(output_dir / DATA_CSV_NAME , index=False)