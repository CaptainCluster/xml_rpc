"""NOTE! This file is merely for testing the multithread functionality
of the application. Its existence is based on ensuring the application
functions properly before being submitted as part of the course
assignment it is intended for.
"""
import threading
import xmlrpc.client
from datetime import datetime
from config.settings import Settings

settings = Settings()

def ask_number_of_threads():
    """An input determines the amount of spawned threads. The
    upper cap and lower cap are defined in the Settings object.
    """
    threads_amount = 0
    while threads_amount <= settings.TEST_LOWERCAP or threads_amount > settings.TEST_UPPERCAP:
        try:
            user_input = input("How many threads do you want to spawn: ")
            threads_amount = int(user_input)
        except Exception as exception:
            print(f"Exception in 'main' function of 'test_case.py' file: {exception}")
    return threads_amount

def thread_work(thread_id):
    """The function each test thread executes. The function
    sends a call to the server for the write function, meaning
    that each thread writes a note entry.
    """
    try:
        proxy = xmlrpc.client.ServerProxy(f"http://{settings.HOST}:{settings.PORT}")
        note_text = f"Written via {thread_id}."
        note_dict = {
            "topic":        "tests_thread",
            "name":         thread_id,
            "text":         note_text,
            "timestamp":    datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        }
        proxy.write_note(note_dict)
    except Exception as exception:
        print(f"Exception in 'main' function of 'test_case.py' file: {exception}")

def main():
    print(f"This application generates a desired amount of threads. The upper cap is {settings.TEST_UPPERCAP}, and it can't be exceeded.")
    threads_amount = ask_number_of_threads()
    threads = []

    for i in range(1, threads_amount+1):
        thread = threading.Thread(
            target=thread_work,
            args=[f"test-thread-{i}"]
        )
        threads.append(thread)

    for thread in threads:
       thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
