import os
import csv


class CsvData:

    def __init__(self, location='', title=''):
        self.location = location
        self.title = title
        self.filename = title + '.csv'
        self.file = location + '/' + self.filename

        if self.__get_accessibel_to_locate():
            pass
        else:
            self.__create_new_file()

    def __create_new_file(self):
        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, self.location)
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)

        f = open(self.file, "x")

        header = ['author', 'publish', 'title']

        # create the csv writer
        writer = csv.writer(f)

        # write a row to the csv file
        writer.writerow(header)

        # close the file
        f.close()

    def add_row(self, row=None):
        with open(self.file, 'a', newline='') as f_object:
            # Pass the CSV file object to the writer() function
            writer_object = csv.writer(f_object)

            writer_object.writerow(row)

        f_object.close()

    def add_rows(self, rows):
        with open(self.file, 'a', newline='') as f_object:
            # Pass the CSV file object to the writer() function
            writer_object = csv.writer(f_object)

            writer_object.writerows(rows)

        f_object.close()

    def recreate_new_file(self, header=['author', 'publish', 'title']):
        # open the file in the write mode
        f = open(self.file, 'w')

        # create the csv writer
        writer = csv.writer(f)

        # write a row to the csv file
        writer.writerow(header)

        # close the file
        f.close()

    def __get_accessibel_to_locate(self):
        tree = os.walk(self.location)

        for address, dirs, files in tree:
            for title in files:
                if (title == self.filename):
                    return True
                pass
            return False
