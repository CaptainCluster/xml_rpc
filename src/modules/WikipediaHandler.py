import wikipedia

class WikipediaHandler:
    def search_wikipedia(self, wiki_topic):
        try:
            wikipedia_topics = wikipedia.search(wiki_topic)
            return wikipedia_topics
        except Exception as exception:
            print(f"Exception at 'search_wikipedia' in WikipediaHandler: {exception}")

    def fetch_summary(self, wiki_article_name):
        try:
            wikipedia_summary = wikipedia.summary(wiki_article_name)
            return wikipedia_summary
        except Exception as exception:
            print(f"Exception at 'fetch_summary' in WikipediaHandler: {exception}")
