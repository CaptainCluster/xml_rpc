import xml.etree.ElementTree as ET
from modules.ETWriteHandler import ETWriteHandler
from modules.ETReadHander   import ETReadHandler

class XMLHandler:
    """This class is responsible for gathering functionality that handles
    XML elements and data.
    """
    def __init__(self, filename: str):
        self.filename = filename
        self.tree = ET.parse(self.filename)
        self.root = self.tree.getroot()

    def create_new_entry(self, noteDict, lock):
        try:
            with lock:
                ET_write_handler = ETWriteHandler(noteDict)
                topic_exists = ET_write_handler.check_topic_exists(self.root, noteDict)
                note_exists = False

                if topic_exists:
                    note_exists = ET_write_handler.check_note_exists(self.root, noteDict)

                if topic_exists and note_exists:
                    topic = ET_write_handler.find_topic(self.root, noteDict)
                    note = ET_write_handler.find_note_from_topic(topic, noteDict)
                    if note:
                        note[0] = ET_write_handler.elem_text
                        note[1] = ET_write_handler.elem_timestamp
                    self.tree.write(self.filename)
                    return

                if topic_exists and not note_exists:
                    topic = ET_write_handler.find_topic(self.root, noteDict)
                    if topic:
                        topic.append(ET_write_handler.elem_note)
                    self.tree.write(self.filename)
                    return

                ET_write_handler.elem_topic.append(ET_write_handler.elem_note)
                self.root.append(ET_write_handler.elem_topic)

                self.tree.write(self.filename)

        except Exception as exception:
            print(f"error detected - {exception}")

    def read_by_topic(self, topic, results, lock):
        try:
            with lock:
                ET_read_handler = ETReadHandler(topic)
                notes = ET_read_handler.find_topic_element(self.root, topic)
                results.append(notes)

        except Exception as exception:
            print(f"error detected - {exception}")
