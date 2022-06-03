import os
from csv_worker import CsvData


class Book():
    """docstring for Book."""

    # csv_location = 'dataset/csv_parse/books'
    csv_location = '/home/sanzharrko/Рабочий стол/Atom/creation_story/dataset/csv_parse/books'

    def __init__(self, book_title='null', contents=None):
        if contents is None:
            contents = []
        self.book_title = book_title
        self.contents = contents

    def transaction(self):
        header = ['chapter_type', 'text']
        csv = CsvData(location=self.csv_location, title=self.book_title)
        csv.recreate_new_file(header)
        csv.add_rows(self.contents)


class OralTranscription:
    csv_location = 'dataset/csv_parse/oral_transcription'

    def __init__(self, title='null', author='null', location='null',
                 publish='null', abstract_title='null'):
        self.title = title
        self.author = author
        self.location = location
        self.publish = publish
        self.abstract_title = abstract_title
        self.data = []

    def add_transcription(self, data=None):
        if data is None:
            data = []
        self.data = data
        pass

    def transaction(self):
        header = ['speaker', 'text']
        csv = CsvData(location=self.csv_location, title=self.title)
        csv.recreate_new_file(header)
        csv.add_rows(self.data)
