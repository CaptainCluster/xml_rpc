import xml.etree.ElementTree as ET

class XmlHandler:
    def __init__(self, filename: str):
        self.filename = filename
        self.tree = ET.parse(self.filename)
        self.root = self.tree.getroot()
        for child in self.root:
            print(str(child.tag) + " - " + str(child.attrib))

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

        if self.check_entry_exists(""):
           return
        
        elem_topic.append(elem_note)
        self.root.append(elem_topic)

        self.tree.write(self.filename)
        


    def check_entry_exists(self, searched_name) -> bool:
        for child in self.root:
            if child.attrib == searched_name:
                return True
        return False

