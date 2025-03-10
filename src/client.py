import xmlrpc.client

from config.settings import Settings
from datetime import datetime

settings = Settings()

def generate_note() -> dict[str, str]:
    """ 
    Generating a note entry through the following 
    user inputs:
        1) note topic
        2) note name
        3) note text content
    
    The note will also be given a timestamp pointing 
    to the current time.
    """

    note_topic  = input("The topic: ")
    note_name   = input("The name: ")
    note_text   = input("The text content: ")
    
    # Creating a dictionary, with timestamp pointing to current time
    return {
        "topic":        note_topic,
        "name":         note_name,
        "text":         note_text,
        "timestamp":    datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    }

def main():
    proxy = xmlrpc.client.ServerProxy(f"http://{settings.HOST}:{settings.PORT}")
    while True:
        noteObj = generate_note()
        result = proxy.receive_note(noteObj)
        print("The result of the addition is:", result)


if __name__ == "__main__":
    main()
