import PyPDF2
import requests
from os import listdir
from os.path import isfile, join


def get_links(file_name):
    if not file_name:
        raise ValueError('Expected Non Empty File Name')
    file = open(file_name, 'r')
    links = file.readline().strip('][\n').split(', ')
    for i in range(len(links)):
        links[i] = links[i].strip("'")
    return links


def get_pdfs(links):
    if not links:
        raise ValueError('Expected Non Empty Links')

    for i in range(len(links)):
        url = links[i]
        response = requests.get(url)

        with open('pdfs/file{}.pdf'.format(i), 'wb') as f:
            f.write(response.content)
    return 0


def main(file_name):
    links = get_links(file_name)
    get_pdfs(links)
    file_number = 0
    for i in range(len(listdir('pdfs/'))):
        if listdir('pdfs/')[i][-3:] == 'pdf':
            pdf_file = open('pdfs/{}'.format(listdir('pdfs/')[i]), 'rb')
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            text = pdf_reader.getPage(0).extractText()
            with open('texts/file{}.txt'.format(file_number), 'w') as f:
                f.write(text)
            file_number += 1
    return 0


if __name__ == '__main__':
    main('tvisa-20pages.txt')
