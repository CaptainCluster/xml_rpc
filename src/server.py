from xmlrpc.server import SimpleXMLRPCServer
from config.settings import Settings
from modules.RequestHandler import RequestHandler
from modules.XmlHandler import XmlHandler

settings = Settings()
xml_handler = XmlHandler(settings.DB_FILENAME)

def receive_note(noteObj):
    print(f"{noteObj["name"]} - {noteObj["topic"]} - {noteObj["text"]} - {noteObj["timestamp"]}")
    xml_handler.create_new_entry(noteObj)
    return noteObj["name"]

def notify_server_start():
    print(f"XML-rpc is serving on port {settings.PORT}.")

def main():
    server = SimpleXMLRPCServer((settings.HOST, settings.PORT), requestHandler=RequestHandler)
    server.register_function(receive_note, "receive_note")
    notify_server_start()
    server.serve_forever()

if __name__ == "__main__":
    main()
