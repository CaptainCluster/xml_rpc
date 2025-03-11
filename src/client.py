import xmlrpc.client
from config.settings import Settings
from datetime import datetime

settings = Settings()

def welcome_user():
    print("Welcome! This application allows you to read and write notes!")

def ask_user_option():
    """Asks an input from the user in order to determine what kind of interaction
    the client will have with the server. Contains exception handling, in case
    the input can't be parsed into an interger.

    Returns
    =======
    The user input as an integer
    """
    print("What would you like to do?")
    try:
        user_input = input("1) Write a note | 2) Read notes (based on topic) | 0) Exit: ")
        return int(user_input)
    except Exception as exception:
        print(f"Error in function 'ask_user_option': {exception}")


def request_write(proxy):
    """Generating a note entry through the following
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
    note_dict = {
        "topic":        note_topic,
        "name":         note_name,
        "text":         note_text,
        "timestamp":    datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    }
    return proxy.write_note(note_dict)

def request_read(proxy):
    note_topic = input("The topic: ")
    return proxy.read_note(note_topic)

def main():
    proxy = xmlrpc.client.ServerProxy(f"http://{settings.HOST}:{settings.PORT}")
    welcome_user()

    while True:
        match ask_user_option():
            case 0:
                break
            case 1:
                result = request_write(proxy)
                print(f"Server response: {result}")
            case 2:
                result = request_read(proxy)
                print(f"Found the following content: {result}")
            case _:
                print("Invalid option. Try again!")
    print("Bye!")


if __name__ == "__main__":
    main()
