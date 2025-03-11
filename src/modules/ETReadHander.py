import xml.etree.ElementTree as ET

class ETReadHandler:
    def __init__(self, topic) -> None:
        self.topic = topic

    def find_topic_element(self, root, note_topic):
        """Finding the topic element based on the string value
        in its name"""
        for topic in root.iter("topic"):
            if topic.attrib["name"] == note_topic:
                return ET.tostring(topic)
        return f"Topic '{note_topic}' does not exist!"
