from gensim.parsing.preprocessing import STOPWORDS


class stopwords:
    def __init__(self):
        self.stopwords = self.initialize_stpw()
        print(f'instance created: {self}')

    def initialize_stpw(self):
        stopwords = set(STOPWORDS)
        custom_words = {"shall", "", "0", "1", "2",
                        "3", "4", "5", "6", "7", "8", "9", "m"}
        for word in custom_words:
            stopwords.add(word)
        return stopwords

    def __del__(self):
        print(f'instance destroyed: {self}')
