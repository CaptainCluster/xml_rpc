import xmlrpc.client
from config.settings import Settings
from datetime import datetime
import xml.etree.ElementTree as ET

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
        user_input = input("1) Write a note | 2) Read notes (based on topic) | 3) Wikipedia search | 0) Exit: ")
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

def request_wikipedia(proxy):
    try:
        wiki_article_name = input("The name of the article: ")
        wikipedia_search_results = proxy.search_wikipedia(wiki_article_name)

        # No results? Then the function will return
        if len(wikipedia_search_results) == 0:
            print("No articles found from Wikipedia. Try another topic.")
            return
    
        print("The Wikipedia search yields the following potential articles:")
        for i in range(1, len(wikipedia_search_results)+1):
            print(f"{i}) {wikipedia_search_results[i-1]}")

        while True:
            chosen_article_index = int(input("Which one will you choose: "))
            if chosen_article_index < 1 or chosen_article_index > len(wikipedia_search_results):
                print(f"The input '{chosen_article_index}' is not within the bounds (upper cap is {len(wikipedia_search_results)})")
                continue
            break

        wikipedia_result = proxy.fetch_summary(wikipedia_search_results[chosen_article_index-1])

        # Handling in case the server sends an error
        summary = wikipedia_result["summary"]
        article_url = wikipedia_result["article_url"]

        if (not summary or len(summary) == 0) and (not article_url or len(article_url) == 0):
            print("Failed to fetch an adequate result! Try another topic.")
            return

        print("\nFound the following content:\n")
        print(f"\nURL: {article_url}")
        print(f"\nSummary: {summary}\n")


        while True:
            confirmation = input("Would you like to write the summary? y=yes, n=no ")
            print(f"you gave '{confirmation}'")
            if confirmation.lower() != "n" and confirmation.lower() != "y":
                print("You gave an incorrect input! y=yes, n=no!")
                continue
            if confirmation.lower() == "n":
                print("Cancelling the procedure.")
                return
            break
        
        text_content = f"""
        URL: {article_url}

        Summary: {summary}
        """
        
        note_topic = input("What will be the topic of the note: ")
        
        note_dict = {
            "topic":        note_topic,
            "name":         wiki_article_name,
            "text":         text_content,
            "timestamp":    datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        }
        return proxy.write_note(note_dict)


    except Exception as exception:
        print(f"Error in function 'request_wikipedia': {exception}")

def read_xml(xml_content):
    root = ET.fromstring(f"{xml_content}")
    for note in root:
        print(note.tag, note.attrib["name"])
        for elem_child in note:
            print(f"{elem_child.tag}: {elem_child.text}")
    


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
                read_xml(result)
            case 3:
                result = request_wikipedia(proxy)
            case _:
                print("Invalid option. Try again!")
    print("Bye!")


if __name__ == "__main__":
    main()
