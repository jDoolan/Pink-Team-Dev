from django.shortcuts import render

from gensim import corpora, models, similarities
from pprint import pprint

import logging
from gensim import corpora


from collections import defaultdict
from pprint import pprint   # pretty-printer

from .corpus import documents

# Create your views here.
import gensim
from gensim.models import tfidfmodel


documents = ["Human machine interface for lab abc computer applications",
            "A survey of user opinion of computer system response time",
           "The EPS user interface management system",
             "System and human system engineering testing of EPS",
            "Relation of user perceived response time to error measurement",
              "The generation of random binary unordered trees",
             "The intersection graph of paths in trees",
             "Graph minors IV Widths of trees and well quasi ordering",
              "Graph minors A survey"]






def gensimTest():

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)




    stoplist = set('for a of the and to in abc'.split())

    texts = [[word for word in document.lower().split() if word not in stoplist]
            for document in documents]

    # print(texts)

    from collections import defaultdict
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            print(frequency[token])
            frequency[token] += 1

    texts = [[token for token in text if frequency[token] > 1]
             for text in texts]

    pprint(texts)





    dictionary = corpora.Dictionary(texts)
    dictionary.save('/tmp/deerwester.dict') # store the dictionary, for future reference
    print(dictionary)

    dictionary = corpora.Dictionary.load('/tmp/deerwester.dict')
    corpus = corpora.MmCorpus('/tmp/deerwester.mm') # comes from the first tutorial, "From strings to vectors"
    print(corpus)
    print(dictionary.token2id)

    new_doc = "Human computer interaction"
    new_vec = dictionary.doc2bow(new_doc.lower().split())
    print(new_vec) # the word "interaction" does not appear in the dictionary and is ignored


    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('/tmp/deerwester.mm', corpus) # store to disk, for later use
    print(corpus)

    class MyCorpus(object):
        def __iter__(self):
            for line in open('mycorpus.txt'):
                 # assume there's one document per line, tokens separated by whitespace
                yield dictionary.doc2bow(line.lower().split())




    corpus_memory_friendly = MyCorpus() # doesn't load the corpus into memory!
    print(corpus_memory_friendly)
    
    
    for vector in corpus_memory_friendly: # load one vector into memory at a time
        print(vector)
    
     # collect statistics about all tokens
    dictionary = corpora.Dictionary(line.lower().split() for line in open('mycorpus.txt'))
    # remove stop words and words that appear only once
    stop_ids = [dictionary.token2id[stopword] for stopword in stoplist
        if stopword in dictionary.token2id]
    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
    dictionary.filter_tokens(stop_ids + once_ids) # remove stop words and words that appear only once
    dictionary.compactify() # remove gaps in id sequence after words that were removed
    print(dictionary)

    corpora.SvmLightCorpus.serialize('/tmp/corpus.svmlight', corpus)
    corpora.BleiCorpus.serialize('/tmp/corpus.lda-c', corpus)
    corpora.LowCorpus.serialize('/tmp/corpus.low', corpus)

    corpora.SvmLightCorpus.serialize('/tmp/corpus.svmlight', corpus)
    corpora.BleiCorpus.serialize('/tmp/corpus.lda-c', corpus)
    corpora.LowCorpus.serialize('/tmp/corpus.low', corpus)

    corpus = corpora.MmCorpus('/tmp/corpus.mm')

    print(corpus)

    # one way of printing a corpus: load it entirely into memory
    print(list(corpus)) # calling list() will convert any sequence to a plain Python list


    # another way of doing it: print one document at a time, making use of the streaming interface
    for doc in corpus:
        print(doc)

    corpora.BleiCorpus.serialize('/tmp/corpus.lda-c', corpus)

    # corpus = gensim.matutils.Dense2Corpus(numpy_matrix)
    # numpy_matrix = gensim.matutils.corpus2dense(corpus, num_terms=number_of_corpus_features)
    #
    #
    # corpus = gensim.matutils.Sparse2Corpus(scipy_sparse_matrix)
    # scipy_csc_matrix = gensim.matutils.corpus2csc(corpus)

def gensimTopics():

    from gensim import corpora, models, similarities
    dictionary = corpora.Dictionary.load('/tmp/deerwester.dict')
    corpus = corpora.MmCorpus('/tmp/deerwester.mm')
    print(corpus)

    tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model

    doc_bow = [(0, 1), (1, 1)]
    print(tfidf[doc_bow]) # step 2 -- use the model to transform vectors

    corpus_tfidf = tfidf[corpus]
    for doc in corpus_tfidf:
            print(doc)

    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2) # initialize an LSI transformation
    corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi

    lsi.print_topics(2)

    for doc in corpus_lsi: # both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly
            print(doc)

    lsi.save('/tmp/model.lsi') # same for tfidf, lda, ...
    lsi = models.LsiModel.load('/tmp/model.lsi')

    # model = tfidfmodel.TfidfModel(bow_corpus, normalize=True)
    #
    # model = lsimodel.LsiModel(tfidf_corpus, id2word=dictionary, num_topics=300)
    #
    #
    # model.add_documents(another_tfidf_corpus) # now LSI has been trained on tfidf_corpus + another_tfidf_corpus
    # lsi_vec = model[tfidf_vec] # convert some new document into the LSI space, without affecting the model
    # ...
    # model.add_documents(more_documents) # tfidf_corpus + another_tfidf_corpus + more_documents
    # lsi_vec = model[tfidf_vec]
    # ...
    #
    # model = rpmodel.RpModel(tfidf_corpus, num_topics=500)
    #
    # model = ldamodel.LdaModel(bow_corpus, id2word=dictionary, num_topics=100)
    #
    # model = hdpmodel.HdpModel(bow_corpus, id2word=dictionary)


def liam_dev(request):

    title = "Home Page"
    user = request.user

    context = {
        "template_title" : title,
        "user" :user,
    }


    gensimTest()

    gensimTopics()


    return render(request, "temp/liamdev.html", context)





def liam_dev2(request):
    title = "Test Page 1"
    user = request.user


    context = {
        "template_title" : title,
        "user" :user,
    }

    return render(request, "temp/liamdev2.html", context)


def liam_dev3(request):
    title = "Test Page 2"
    user = request.user


    context = {
        "template_title" : title,
        "user" :user,
    }

    return render(request, "temp/liamdev3.html", context)