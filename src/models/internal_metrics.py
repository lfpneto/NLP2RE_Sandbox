from gensim.models.ldamodel import LdaModel
from gensim.corpora.dictionary import Dictionary


def perplexity(model, BOW):
    # Calculate perplexity
    if not all(isinstance(item, tuple) and len(item) == 2 for item in BOW):
        raise ValueError("BOW must be a list of tuples (term_id, frequency)")
    perplexity = model.log_perplexity(BOW)
    print(f'Perplexity: {perplexity}')
    return perplexity
