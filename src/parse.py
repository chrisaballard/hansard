"""Parse the set of XML files in ParlParse format and store as json"""

import argparse
from pathlib import Path
from glob import glob
from dataclasses import asdict
import json

from tqdm import tqdm

from hansard_parser.xml_parser import parse_hansard_xml_file


def main(xml_file_path, output_path):
    for xml_file in tqdm(
        glob(f"{xml_file_path}\\*.xml")
    ):
        print(xml_file)
        parsed_hansard_file = parse_hansard_xml_file(xml_file)
        xml_file = Path(xml_file)
        json_output_file = Path(output_path) / xml_file.with_suffix(".json").name
        headings = [asdict(heading) for heading in parsed_hansard_file.values()]
        if headings:
            with open(json_output_file, "wt") as json_f:
                    json.dump(headings, json_f, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--xml-file-path",
        type=str,
        required=False,
        default="data"
    )
    parser.add_argument(
        "--output-path",
        type=str,
        required=False,
        default="data\\output"
    )
    args = parser.parse_args()

    main(args.xml_file_path, args.output_path)