import xml.etree.ElementTree as ET
from modules.ETDataHandler import ETDataHandler

class XMLHandler:
    def __init__(self, filename: str):
        self.filename = filename
        self.tree = ET.parse(self.filename)
        self.root = self.tree.getroot()

    def create_new_entry(self, noteDict):
        try:
            ET_data_handler = ETDataHandler(noteDict)
            topic_exists = ET_data_handler.check_topic_exists(self.root, noteDict)
            note_exists = False

            if topic_exists:
                note_exists = ET_data_handler.check_note_exists(self.root, noteDict)

            if topic_exists and note_exists:
                topic = ET_data_handler.find_topic(self.root, noteDict)
                note = ET_data_handler.find_note_from_topic(topic, noteDict)
                if note:
                    note[0] = ET_data_handler.elem_text
                    note[1] = ET_data_handler.elem_timestamp
                self.tree.write(self.filename)
                return

            if topic_exists and not note_exists:
                topic = ET_data_handler.find_topic(self.root, noteDict)
                if topic:
                    topic.append(ET_data_handler.elem_note)
                self.tree.write(self.filename)
                return

            ET_data_handler.elem_topic.append(ET_data_handler.elem_note)
            self.root.append(ET_data_handler.elem_topic)

            self.tree.write(self.filename)

        except Exception as exception:
            print(f"error detected - {exception}")
