import xml.etree.ElementTree as ET
from modules.ETDataHandler import ETDataHandler

class XmlHandler:
    def __init__(self, filename: str):
        self.filename = filename
        self.tree = ET.parse(self.filename)
        self.root = self.tree.getroot()

    def create_new_entry(self, noteDict):
        try:
            ET_data_handler = ETDataHandler(noteDict)
            topic_exists = self.check_topic_exists(noteDict)
            note_exists = False

            if topic_exists:
                note_exists = self.check_note_exists(noteDict)

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


    def check_topic_exists(self, note_dict) -> bool:
        for topic in self.root.findall("topic"):
            if topic.attrib["name"] == note_dict["topic"]:
                return True
        return False

    def check_note_exists(self, note_dict) -> bool:
        for topic in self.root.findall("topic"):
            if topic.attrib["name"] != note_dict["topic"]:
                continue
            for note in topic.findall("note"):
                print(note.attrib["name"])
                if note.attrib["name"] == note_dict["name"]:
                    return True
        return False
