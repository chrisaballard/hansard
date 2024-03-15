from typing import Dict, List, Union, Dict
import xml.etree.ElementTree as ET
from pathlib import Path

from .data_model import Heading, Speech

HEADING_SPEECHES = Dict[str, Heading]


def parse_hansard_xml_file(file_path: str) -> HEADING_SPEECHES:
    """Parse XML file and return a dictionary representing the hierarchy of Heading and Speech objects."""
    
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    hierarchy = {}
    current_major_heading = None
    
    for child in root:
        if child.tag == "major-heading":
            # Parse major headings
            current_major_heading = Heading(id=child.attrib["id"], name=child.text.strip())
            hierarchy[current_major_heading.name] = current_major_heading
            current_major_heading.headings = []
            current_major_heading.speeches = []
        elif child.tag == "minor-heading":
            # Parse minor headings
            if current_major_heading:
                current_minor_heading = Heading(id=child.attrib["id"], name=child.text.strip())
                current_major_heading.headings.append(current_minor_heading)
        elif child.tag == "speech":
            if not child.attrib.get("nospeaker", None):
                speakername = child.attrib.get("speakername", "")
                speech_type = child.attrib.get("type", "")
                person_id = child.attrib.get("person_id", "")
                text = [p.text for p in child.findall("p")]
                speech = Speech(id=child.attrib["id"], speakername=speakername, type=speech_type, person_id=person_id, text=text)
                # Parse speeches
                if current_minor_heading:
                    current_minor_heading.speeches.append(speech)
                elif current_major_heading:
                    current_major_heading.speeches.append(speech)
    
    return hierarchy

