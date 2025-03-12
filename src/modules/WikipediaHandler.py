import wikipedia
import requests

class WikipediaHandler:
    
    def search_wikipedia(self, wiki_topic, results, lock):
        with lock:
            try:
                wikipedia_topics = wikipedia.search(wiki_topic)
                results.append(wikipedia_topics)
            except Exception as exception:
                print(f"Exception at 'search_wikipedia' in WikipediaHandler: {exception}")

    def fetch_summary(self, wiki_article_name, results, lock):
        with lock: 
            # The summary fetching is error-prone and thus needs good error handling 
            wikipedia_summary = None
            try:
                wikipedia_summary = wikipedia.summary(wiki_article_name)
            except Exception as exception:
                print(f"Exception at 'fetch_summary' in WikipediaHandler: {exception}")

            finally:
                wiki_article_name = self.format_term(wiki_article_name)
                proposed_url = f"https://en.wikipedia.org/wiki/{wiki_article_name}"

                response = requests.get(f"https://en.wikipedia.org/w/api.php?action=opensearch&search={wiki_article_name}&limit=9&format=json").json()

                # Avoiding index error
                if len(response) < 4:
                    print("The response structure is unexpected. Exiting.")
                    results.append({
                        "article_url":  "",
                        "summary":      ""
                        })
                    return

                # Checking whether the proposed URL matches any entry in the response
                for url in response[3]:
                    if proposed_url == url and wikipedia_summary:
                        results.append({
                                "article_url":  proposed_url,
                                "summary":      wikipedia_summary 
                                })
                        return
                    if proposed_url == url:
                        results.append({
                                "article_url":  proposed_url,
                                "summary":      ""
                                })
                        return
                results.append({
                        "article_url":  "",
                        "summary":      ""
                        })


    def format_term(self, term):
        article_list = list(term)

        for i in range(0, len(article_list)-1):
            if article_list[i] == " ":
                article_list[i] = '_'
        return "".join(article_list) 

