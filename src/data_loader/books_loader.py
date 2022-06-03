import os
import tqdm
import sys
import os
import pandas as pd
from keras.preprocessing.text import Tokenizer
import nltk


class BooksDataLoader:

    def __init__(self, location=os.path.dirname(os.path.abspath(os.getcwd())) + '/dataset/csv_parse/books',
                 limit=0):
        self.location = location
        self.limit = limit
        pass

    def __book_load(self):
        dataframes = []
        files = os.listdir(self.location)
        if 0 < self.limit < len(files):
            for i in range(len(files) - self.limit):
                files.pop(len(files) - 1)
                pass
            pass
        for file in tqdm.tqdm(files):
            csv_book = pd.read_csv(self.location + '/' + file, names=['label', 'text'], skiprows=[0])
            dataframes.append({'label': csv_book['label'], 'text': csv_book['text']})
            pass

        return dataframes

    def loader(self, chapter_split=2):
        books = self.__book_load()
        data_loader = []

        for book in books:
            counter_limiter = -1
            for i in range(len(book['label'])):
                if 0 <= counter_limiter < chapter_split:
                    data_loader[len(data_loader) - 1] \
                        .append({'label': book['label'][i], 'text': book['text'][i]})
                else:
                    data_loader.append([{'label': book['label'][i], 'text': book['text'][i]}])
                    counter_limiter = 0
                counter_limiter += 1

        return data_loader

    @staticmethod
    def dataframe_loader_to_text(data_loader=None):
        if data_loader is None:
            data_loader = []
            pass
        dataframe_text_loader = [[]]
        for book in data_loader:
            for chapters in book:
                texts = '\n\n\n\n\n' + str(chapters['text']) + '\n'
                dataframe_text_loader[len(dataframe_text_loader) - 1].append(texts)
                pass
            dataframe_text_loader.append([])
        return dataframe_text_loader
