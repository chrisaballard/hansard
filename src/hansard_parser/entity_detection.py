"""Detect entities in a speech"""

from typing import List

from .data_model import Speech, ParagraphEntity, EntityAttributes

from gliner import GLiNER


class EntityDetector:
    """Detect entities in a speech"""

    def __init__(self, labels: List[str]):
        self.model = GLiNER.from_pretrained("urchade/gliner_base")
        self.labels = labels

    def get_speech_entities(self, speech: Speech):
        """Uses GLiNER to detect entities in a speech"""

        for paragraph in speech.text:
            paragraph_entities = self.model.predict_entities(paragraph.text, labels=self.labels)
            for paragraph_entity in paragraph_entities:
                paragraph.entities.append(
                    ParagraphEntity(
                        text=paragraph_entity["text"],
                        label=paragraph_entity["label"],
                        attributes=EntityAttributes(
                            start=paragraph_entity["start"], 
                            end=paragraph_entity["end"]
                        ),
                    )
                )
        
        return speech


    def detect_entities(self, text):
        """Detect entities in a speech"""
        return self.gliners.predict(text)