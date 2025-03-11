from xmlrpc.server import SimpleXMLRPCServer
from config.settings import Settings
from modules.RequestHandler import RequestHandler
from modules.XmlHandler import XMLHandler

import threading

settings = Settings()
xml_handler = XMLHandler(settings.DB_FILENAME)

def receive_note(note_dict):
    thread = threading.Thread(
            target=xml_handler.create_new_entry,
            args=[note_dict])
    thread.start()
    print(f"{note_dict["name"]} - {note_dict["topic"]} - {note_dict["text"]} - {note_dict["timestamp"]}")
    return note_dict["name"]

def notify_server_start():
    print(f"XML-rpc is serving on port {settings.PORT}.")



def main():
    server = SimpleXMLRPCServer((settings.HOST, settings.PORT), requestHandler=RequestHandler)
    server.register_function(receive_note, "receive_note")
    notify_server_start()
    server.serve_forever()

if __name__ == "__main__":
    main()
