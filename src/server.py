from xmlrpc.server import SimpleXMLRPCServer
from config.settings import Settings
from modules.RequestHandler import RequestHandler
from modules.WikipediaHandler import WikipediaHandler
from modules.XmlHandler import XMLHandler
import threading

lock = threading.Lock()

settings = Settings()
xml_handler = XMLHandler(settings.DB_FILENAME)
wikipedia_handler = WikipediaHandler()

def write_note(note_dict):
    thread = threading.Thread(
            target=xml_handler.create_new_entry,
            args=[note_dict, lock])
    thread.start()
    thread.join()
    print(f"""The following data was successfully written:
        Note name: {note_dict["name"]}
        Topic: {note_dict["topic"]}
        Text content: {note_dict["text"]}
        Timestamp: {note_dict["timestamp"]}""")
    return "Success"

def read_note(note_topic):
    results = []
    thread = threading.Thread(
            target=xml_handler.read_by_topic,
            args=[note_topic, results, lock])
    thread.start()
    thread.join()
    
    if len(results) == 0:
        return ""
    return results[0]

def search_wikipedia(wiki_topic):
    results = []
    thread = threading.Thread(
        target=wikipedia_handler.search_wikipedia,
        args=[wiki_topic, results, lock]
    )
    thread.start()
    thread.join()
    return results[0]

def fetch_summary(wiki_article_name):
    results = []
    thread = threading.Thread(
        target=wikipedia_handler.fetch_summary,
        args=[wiki_article_name, results, lock]
    )
    thread.start()
    thread.join()
    return results[0]


def notify_server_start():
    print(f"The server is serving on port {settings.PORT}.")

def main():
    server = SimpleXMLRPCServer((settings.HOST, settings.PORT), requestHandler=RequestHandler)
    server.register_function(write_note, "write_note")
    server.register_function(read_note, "read_note")
    server.register_function(search_wikipedia, "search_wikipedia")
    server.register_function(fetch_summary, "fetch_summary")
    notify_server_start()
    server.serve_forever()

if __name__ == "__main__":
    main()
