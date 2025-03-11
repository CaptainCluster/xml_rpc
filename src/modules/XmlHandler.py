import xml.etree.ElementTree as ET

class XmlHandler:
    def __init__(self, filename: str):
        self.filename = filename
        self.tree = ET.parse(self.filename)
        self.root = self.tree.getroot()


    def create_new_entry(self, noteDict):
        
        elem_topic = ET.Element("topic")
        elem_topic.set("name", noteDict["topic"])

        elem_note = ET.Element("note")
        elem_note.set("name", noteDict["name"])

        elem_text = ET.Element("text")
        elem_text.text = noteDict["text"]

        elem_timestamp = ET.Element("timestamp")
        elem_timestamp.text = noteDict["timestamp"]

        elem_note.append(elem_text)
        elem_note.append(elem_timestamp)

        try:
            topic_exists = self.check_topic_exists(noteDict)
            note_exists = False

            if topic_exists:
                note_exists = self.check_note_exists(noteDict)

            if topic_exists and note_exists:
                topic = self.find_topic(noteDict)
                note = self.find_note_from_topic(topic, noteDict)
                if note:
                    note[0] = elem_text
                    note[1] = elem_timestamp
                self.tree.write(self.filename)
                return

            if topic_exists and not note_exists:
                topic = self.find_topic(noteDict)
                if topic: 
                    topic.append(elem_note)
                self.tree.write(self.filename)
                return

            elem_topic.append(elem_note)
            self.root.append(elem_topic)

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

    def find_topic(self, note_dict):
        for topic in self.root.findall("topic"):
            if topic.attrib["name"] == note_dict["topic"]:
                return topic

    def find_note(self, note_dict):
        for topic in self.root.findall("topic"):
            if topic.attrib["name"] != note_dict["topic"]:
                continue
            for note in topic.findall("note"):
                if note.attrib["name"] == note_dict["name"]:
                    return note

    def find_note_from_topic(self, elem_topic, note_dict):
        for note in elem_topic:
            if note.attrib["name"] == note_dict["name"]:
                return note

