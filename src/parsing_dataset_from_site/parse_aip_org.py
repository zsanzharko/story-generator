import requests
from bs4 import BeautifulSoup
from csv_worker import CsvData
from text_story import OralTranscription

basic_csv_location = 'dataset/csv_parse'

main_url_site = 'https://www.aip.org'
browse_url_path = main_url_site + '/history-programs/niels-bohr-library/oral-histories/browse/'

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

def main():
    pass
    # browse_links = browse_parse()
    # links_transcripts = browse_list_parse(browse_links)
    # browse_oral_history_transcripts(links_transcripts)


def browse_parse():
    url = browse_url_path
    request = requests.get(url, headers)
    soup = BeautifulSoup(request.content, features="html.parser")
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    # getting 'span' tag with 'a' links
    browses = soup.findAll('span', {'class': "views-summary views-summary-unformatted"})

    links = {}

    for browse in browses:
        # finding children tag 'a' with link
        children = browse.findChildren("a" , recursive=False)
        for child in children:
            # add link with text to links
            link = main_url_site + child.get('href')
            links.update({child.getText(): link})

    return links


def browse_list_parse(links):
    header = ['title', 'publish', 'link']
    csv = CsvData(location=basic_csv_location, title="history_lists_transcripts")
    csv.recreate_new_file(header=header)

    links_send = []

    for key in links:
        request = requests.get(links[key], headers)
        soup = BeautifulSoup(request.content, features="html.parser")
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        views_row = soup.findAll('div', {'class': 'views-row'})

        for browse in views_row:
            div_name = browse.find('div', {'class': 'views-field views-field-field-interviewee-name'})
            div_date = browse.find('div', {'class': 'views-field views-field-field-interview-date'})

            #  Get Link
            link_content = div_name.find('div', {'class':'field-content'})
            link_content_a_link = link_content.find("a" , recursive=False)
            link = main_url_site + link_content_a_link.get('href')
            # Get Publish Date
            div_content_date = div_date.find('div', {'class', 'field-content'})
            publish_date = div_content_date.find('time', {'class':'datetime'})

            if (publish_date == None):
                publish_date = 'null'
            else: publish_date = publish_date.getText()

            # Save to Csv
            csv.add_row([link_content_a_link.getText(), publish_date, link])
            links_send.append(link)

        print('{key} is finished'.format(key=key))

    return links_send


def browse_oral_history_transcripts(links_transcripts):

    for link_transcripts in links_transcripts:
        print("STARTED, Link: {link}".format(link=link_transcripts))
        url = link_transcripts
        request = requests.get(url, headers)
        soup = BeautifulSoup(request.content, features="html.parser")
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        if (soup.find('h1', {'class': 'page-title'}).getText() == 'Page not found'):
            print('Page not found, continue')
            continue

        # getting title
        div_title = soup.find('span', {'class', 'field field--name-title field--type-string field--label-hidden'})
        title = 'null'
        if div_title is not None:
            title = div_title.getText()

        # getting author
        div_author = soup.find('div', {'class', 'field field--name-field-interviewer field--type-string field--label-inline clearfix'})
        author_title = 'null'
        if div_author is not None and div_author.find('div', {'class': 'field__item'}) != None:
            author_title = div_author.find('div', {'class': 'field__item'}).getText()

        # getting location
        div_location = soup.find('div', {'class': 'field field--name-field-interview-location field--type-string field--label-inline clearfix'})
        location_title = 'null'
        if div_location is not None and div_location.find('div', {'class': 'field__item'}) != None:
            location_title = div_location.find('div', {'class': 'field__item'}).getText()

        # getting publish date
        div_date = soup.find('div', {'class': 'class="field field--name-field-interview-date field--type-datetime field--label-inline clearfix"'})
        date_title = 'null'
        if div_date is not None and div_date.find('div', {'class', 'field__item'}) != None:
            date_title = div_date.find('div', {'class', 'field__item'}).getText()

        # getting 'abstract_title'
        div_abstract = soup.find('div', {'class': "clearfix text-formatted field field--name-field-interview-abstract field--type-text-long field--label-hidden field__item"})
        abstract_title = 'null'
        if div_abstract is not None and div_abstract.find('p') != None:
            abstract_title = div_abstract.find('p').getText()

        #getting transcription

        transcription = []

        div_labels = soup.findAll('div', {'class': 'field__label'})
        index_label = 0
        for i in range(len(div_labels)):
            if(div_labels[i].getText() == 'Transcript'):
                index_label = i
                break

        div_transcription_item = div_labels[index_label].parent

        div_transcription_item_speakers = div_transcription_item.findAll('h3')
        div_transcription_item_text = div_transcription_item.findAll('p')

        for i in range(len(div_transcription_item_speakers)):
            speaker = 'null'
            text = 'null'
            try:
                speaker = div_transcription_item_speakers[i].getText().replace(':', '')
                text = div_transcription_item_text[i].getText()
            except:
                print('have error with index')
            transcription.append([speaker, text])

        OT = OralTranscription(title=title, author=author_title, location=location_title, publish=date_title, abstract_title=abstract_title)
        OT.add_transcription(transcription)
        OT.transaction()
        print('{file}, saved'.format(file=title))







if __name__ == '__main__':
    main()
