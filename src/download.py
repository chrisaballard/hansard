"""
Main script for downloading Hansard XML files from the TheyWorkForYou website.
"""


from datetime import datetime
import argparse

from tqdm import tqdm

from hansard_parser.utils import generate_date_range
from hansard_parser.xml_retriever import download_xml_file

HANSARD_XML_URL = "https://www.theyworkforyou.com/pwdata/scrapedxml/debates/"


def main(start_date: str, end_date: str, output_dir: str):
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    download_pbar = tqdm(generate_date_range(start_date, end_date))
    for xml_file_date in download_pbar:
        download_pbar.set_description(f"Downloading {xml_file_date}")
        download_xml_file(HANSARD_XML_URL, xml_file_date, output_dir)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--start-date",
        type=str,
        required=True
    )
    parser.add_argument(
        "--end-date",
        type=str,
        required=True
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        required=False,
        default="..\\data"
    )
    args = parser.parse_args()

    main(args.start_date, args.end_date, args.output_dir)
