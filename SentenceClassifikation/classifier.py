from flair.data_fetcher import NLPTaskDataFetcher
from flair.embeddings import WordEmbeddings, FlairEmbeddings, DocumentLSTMEmbeddings, DocumentRNNEmbeddings
from flair.models import TextClassifier
from flair.trainers import ModelTrainer
from pathlib import Path
from flair.data import Corpus
from flair.datasets import ClassificationCorpus, CSVClassificationCorpus
from multiprocessing import Process, freeze_support
import torch
import sys

if __name__ == '__main__':

    #freeze_support()

    data_folder = 'data2'

    # column format indicating which columns hold the text and label(s)
    column_name_map = {1: "text", 0: "label_topic"}

    # load corpus containing training, test and dev data and if CSV has a header, you can skip it
    corpus: Corpus = CSVClassificationCorpus(data_folder,
                                             column_name_map,
                                             skip_header=True,
                                             delimiter='\t',  # tab-separated files
                                             )

    # load corpus containing training, test and dev data
    # corpus: Corpus = ClassificationCorpus(data_folder,
    #                                     test_file='test.csv',
    #                                    dev_file='dev.csv',
    #                                   train_file='train.csv')

    # orpus = NLPTaskDataFetcher.load_classification_corpus(Path('./'), test_file='data/test.csv', dev_file='data/dev.csv', train_file='data/train.csv')
    word_embeddings = [WordEmbeddings('de'), FlairEmbeddings('de-forward'), FlairEmbeddings('de-backward')]
    document_embeddings = DocumentRNNEmbeddings(word_embeddings, hidden_size=512, reproject_words=True,
                                                reproject_words_dimension=256)
    classifier = TextClassifier(document_embeddings, label_dictionary=corpus.make_label_dictionary(), multi_label=True)
    trainer = ModelTrainer(classifier, corpus)
    trainer.train(data_folder, max_epochs=10)
