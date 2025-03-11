import xml.etree.ElementTree as ET

class ETDataHandler:
    def __init__(self, note_dict: dict[str, str]) -> None:
        self.elem_topic = ET.Element("topic")
        self.elem_topic.set("name", note_dict["topic"])

        self.elem_note = ET.Element("note")
        self.elem_note.set("name", note_dict["name"])

        self.elem_text = ET.Element("text")
        self.elem_text.text = note_dict["text"]

        self.elem_timestamp = ET.Element("timestamp")
        self.elem_timestamp.text = note_dict["timestamp"]

        self.elem_note.append(self.elem_text)
        self.elem_note.append(self.elem_timestamp)

    def find_topic(self, root, note_dict):
        for topic in root.findall("topic"):
            if topic.attrib["name"] == note_dict["topic"]:
                return topic

    def find_note_from_topic(self, topic, note_dict):
        for note in topic:
            if note.attrib["name"] == note_dict["name"]:
                return note

    def check_topic_exists(self, root, note_dict) -> bool:
        for topic in root.findall("topic"):
            if topic.attrib["name"] == note_dict["topic"]:
                return True
        return False

    def check_note_exists(self, root, note_dict) -> bool:
        for topic in root.findall("topic"):
            if topic.attrib["name"] != note_dict["topic"]:
                continue
            for note in topic.findall("note"):
                print(note.attrib["name"])
                if note.attrib["name"] == note_dict["name"]:
                    return True
        return False
