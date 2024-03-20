from typing import Dict, List, Union, Dict
import xml.etree.ElementTree as ET
from pathlib import Path

from .data_model import (
    Heading, 
    Speech, 
    Person, 
    Paragraph, 
    TagType, 
    EntityAttributes,
    Division,
    PersonVote,
    VoteType
)

HEADING_SPEECHES = Dict[str, Heading]

def extract_division_votes(division: ET.Element) -> List[PersonVote]:
    votes = []
    id = division.attrib["id"]
    mplist = division.find(TagType.MPLIST.value)
    vote_count = division.find(TagType.DIVISION_COUNT.value)
    vote_ayes = vote_count.attrib.get("ayes", 0)
    vote_noes = vote_count.attrib.get("noes", 0)
    for vote in mplist.findall(TagType.MPNAME.value):
        person_id = vote.attrib.get("person_id", None)
        vote_type = vote.attrib.get("vote", None)
        if person_id and vote_type:
            votes.append(
                PersonVote(persion_id=person_id, vote=VoteType[vote_type.upper()].value)
            )
    
    return Division(
        id=id,
        count_aye=vote_ayes,
        count_no=vote_noes,
        votes=votes
    )


def extract_paragraph_text_entities(paragraph: ET.Element) -> List[str]:
    """Given a paragraph element <p> returns the text in the paragraph and any references to entities
    in the paragraph, such as persons"""

    paragraph_person_entities = []
    paragraph_text = [paragraph.text] if paragraph.text else []
    paragraph_position = len(paragraph_text)
    count_tags = 0
    for tag in paragraph:
        if tag.tag == "phrase":
            count_tags += 1
            person_id = tag.attrib.get("person_id", None)
            person_name = tag.attrib.get("name", None)

            person_entity = None

            if tag.text:
                paragraph_text.append(tag.text)
                paragraph_position += len(tag.text)

            if person_id:
                person_attributes = EntityAttributes(
                    start=paragraph_position, 
                    end=paragraph_position + len(tag.text)
                )
                person_entity = Person(
                    id=person_id, 
                    name=person_name, 
                    attributes=person_attributes
                )
            
            if tag.tail:
                paragraph_text.append(tag.tail)
                paragraph_position += len(tag.tail)
            if person_entity:
                paragraph_person_entities.append(person_entity)

    return Paragraph("".join(paragraph_text), paragraph_person_entities)


def parse_hansard_xml_file(file_path: str) -> HEADING_SPEECHES:
    """Parse XML file and return a dictionary representing the hierarchy of Heading and Speech objects."""
    
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    hierarchy = {}
    current_major_heading = None
    current_minor_heading = None
    
    for child in root:
        if child.tag == TagType.MAJOR_HEADING.value:
            # Parse major headings
            current_minor_heading = None
            current_major_heading = Heading(id=child.attrib["id"], name=child.text.strip())
            hierarchy[current_major_heading.name] = current_major_heading
        elif child.tag == TagType.MINOR_HEADING.value:
            # Parse minor headings
            if current_major_heading:
                current_minor_heading = Heading(id=child.attrib["id"], name=child.text.strip())
                current_major_heading.headings.append(current_minor_heading)
        elif child.tag == TagType.SPEECH.value:
            person_name = child.attrib.get("speakername", "")
            person_id = child.attrib.get("person_id", "")
            person = Person(id=person_id, name=person_name) if person_id else None
            speech_type = child.attrib.get("type", "")
            text = [extract_paragraph_text_entities(p) for p in child.findall("p")]
            speech = Speech(id=child.attrib["id"], type=speech_type, person=person, text=text)
            # Parse speeches
            if current_minor_heading:
                current_minor_heading.speeches.append(speech)
            elif current_major_heading:
                current_major_heading.speeches.append(speech)
        elif child.tag == TagType.DIVISION.value:
            # Parse division
            division = extract_division_votes(child)
            if current_minor_heading:
                current_minor_heading.votes.append(division)
            elif current_major_heading:
                current_major_heading.votes.append(division)
        
    
    return hierarchy

