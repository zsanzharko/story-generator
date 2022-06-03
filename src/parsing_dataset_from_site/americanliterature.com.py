import requests
import tqdm
from bs4 import BeautifulSoup
from csv_worker import CsvData
from text_story import Book

basic_csv_location = 'dataset/csv_parse'

main_url_site = 'https://americanliterature.com'

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}


def get_novel_books():
    classic_Books_Novels = []

    url = main_url_site + '/books'
    request = requests.get(url, headers)
    soup = BeautifulSoup(request.content, features="html.parser")
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    div_books = soup.findAll('div', {'class': 'col-xs-6 col-md-4'})

    for book in div_books:
        # book_link = ''
        # if main_url_site in book.find('a').get('href'):
        #     book_link = book.find('a').get('href')
        # else:
        #     books_link = main_url_site + book.find('a').get('href')

        classic_Books_Novels.append({
            'title': book.find('a').getText(),
            'link': main_url_site + book.find('a').get('href')})

    return classic_Books_Novels


def get_summary_chapters(books_link):
    # for index in range(len(books_link)):
    #     if 'bio-books-stories' in books_link[index]['link']:
    #         print('{index} link: "{link}"'.format(index=index, link=books_link[index]['link']))
    # return
    # for index in range(len(books_link)):
    #     if index < 148:
    #         books_link.pop(0)

    for link in tqdm.tqdm(books_link):
        try:
            url = link['link']
            request = requests.get(url, headers)
            soup = BeautifulSoup(request.content, features="html.parser")
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()  # rip it out

            p_s = soup.findAll('p')

            summary_chapters = []
            for p in p_s:
                a_link = p.find('a')
                if a_link is None:
                    continue
                if a_link.get('href') is None:
                    continue
                if "/author" not in a_link.get('href'):
                    continue

                c_link = a_link.get('href')

                if main_url_site in a_link.get('href'):
                    summary_chapters.append({
                        'title': a_link.getText(),
                        'link': a_link.get('href')})
                    continue

                summary_chapters.append({
                    'title': a_link.getText(),
                    'link': main_url_site + a_link.get('href')})

            chapter_content = []
            for chapter_link in summary_chapters:
                url = chapter_link['link']
                request = requests.get(url, headers)
                soup = BeautifulSoup(request.content, features="html.parser")

                content = ''
                for p in soup.find('div', {'class': 'jumbotron'}).findAll('p'):
                    if len(p) == 0:
                        continue
                    content += p.getText()

                if content is not None and len(content) > 0:
                    for pre in soup.find('div', {'class': 'jumbotron'}).findAll('pre'):
                        if len(pre) == 0:
                            continue
                        content += pre.getText()

                chapter_content.append([chapter_link["title"], content])

            Book(book_title=link['title'], contents=chapter_content).transaction()
        except:
            print('Have problem with site. ')


def main():
    books_link = get_novel_books()
    get_summary_chapters(books_link)


if __name__ == '__main__':
    main()
