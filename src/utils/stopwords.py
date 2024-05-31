from gensim.parsing.preprocessing import STOPWORDS


class stopwords:
    def __init__(self):
        print('stopwords class object created...')
        self.stopwords = self.initialize_stpw()

    def initialize_stpw(self):
        stopwords = set(STOPWORDS)
        custom_words = {"shall", "", "0", "1", "2",
                        "3", "4", "5", "6", "7", "8", "9", "m"}
        for word in custom_words:
            stopwords.add(word)
        return stopwords

    def __del__(self):
        print(f'{self} instance destroyed.')
