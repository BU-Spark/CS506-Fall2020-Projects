import re
import requests
import os
from bs4 import BeautifulSoup
import pandas as pd
import subprocess
from tqdm import tqdm

import PyPDF2
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

# Global variable
INDEX_FILE = './pdf_name_url.csv'
PDF_DIR = './download_pdf'
if not os.path.exists(PDF_DIR):
    os.mkdir(PDF_DIR)
RESULT_FILE = './result.csv'

# spider
def spider_url_and_download_pdf(update_index=True):
    """loop through the target site

    update_index: True: scrape again; False: no need update
    """
    PAGE_NUM = 1  # page number
    NULL_PAGE_DISP = 'Sorry, no results found'
    TITLE_MUST_DISP = 'Application for T Nonimmigrant Status'

    if os.path.exists(INDEX_FILE):
        DATA_HIST = [(na, url) for na, url in pd.read_csv(INDEX_FILE).values]
    else:
        DATA_HIST = []

    # update_index == True, the crawl will loop through the site again, and check if there is any updates
    if update_index:
        DATA_NEW = []
        while True:
            url = f'https://search.usa.gov/search?affiliate=uscis-aao&dc=1847&page={PAGE_NUM}&query=form+I-914&search=Search&utf8=%E2%9C%93'
            try:
                res = requests.get(url)

                # no more data
                if NULL_PAGE_DISP in res.text:
                    print('No more data, spider done.')
                    break

                soup = BeautifulSoup(res.text, 'html.parser')
                divs = soup.find_all('div', attrs={'class': 'content-block-item result'})

                title_urls = [re.split('\n+', d.text.strip())[1:3] for d in divs]
                valid_title_urls = [(title, url) for title, url in title_urls
                                    if TITLE_MUST_DISP in title]
                new_data = [tup for tup in valid_title_urls if tup not in DATA_HIST]
                print(f'Page {PAGE_NUM}, find {len(new_data)} new url.')

                DATA_NEW.extend(new_data)
                PAGE_NUM += 1

            except Exception:
                import traceback
                traceback.print_exc()
                import ipdb
                ipdb.set_trace()

        # update hist_file
        DATA_HIST.extend(DATA_NEW)
        pd.DataFrame(DATA_HIST, columns=['title', 'url']).drop_duplicates().to_csv(INDEX_FILE,
                                                                                   index=None)

    # download pdf file
    df_hist = pd.read_csv(INDEX_FILE)
    for title, url in tqdm(df_hist.values, desc='pdf download'):
        try:
            fname = os.path.basename(url)
            fpath = os.path.join(PDF_DIR, fname)
            if os.path.exists(fpath):
                continue
            subprocess.check_call(['wget', url], cwd=PDF_DIR, stderr=subprocess.DEVNULL)

        except Exception:
            print(f'{url} download failed')


def parse_by_pdfminer(pdf_path):

    praser = PDFParser(open(pdf_path, 'rb'))
    doc = PDFDocument()
    praser.set_document(doc)
    doc.set_parser(praser)

    doc.initialize()

    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        page_txts = []
        for page in doc.get_pages():
            interpreter.process_page(page)
            layout = device.get_result()
            layout_txts = []
            for x in layout:
                if isinstance(x, LTTextBox):
                    layout_txts.append(x.get_text().strip())
            page_txts.append('\n'.join(layout_txts))

        return page_txts


def parse_by_PyPDF2(pdf_path):

    mypdf = open(pdf_path, mode='rb')

    pdf_document = PyPDF2.PdfFileReader(mypdf)

    page_num = pdf_document.numPages
    page_txts = []
    for page in range(page_num):
        txt = pdf_document.getPage(page).extractText()
        page_txts.append(txt)

    return page_txts


def extract_info(page_txts):

    # 1. get id
    # Get match in first page: "In Re: 9435010" or last page: "ID# 1940904"
    match1 = re.search('In Re: (\d+)', page_txts[0], re.IGNORECASE)
    match2 = re.search('# (\d+)', page_txts[-1], re.IGNORECASE)

    if match1:
        ID = match1.group(1)
    elif match2:
        ID = match2.group(1)
    else:
        ID = None

    # 2. date decision status
    # match_date = re.search('DA\s*TE.*?:(.*?\d{4})', page_txts[0], re.IGNORECASE)
    # date = match_date.group(1).strip() if match_date else None

    match_decision = re.search('(appeal|motion).*?decision', page_txts[0], re.IGNORECASE)
    decision = match_decision.group() if match_decision else None

    match_status = re.search('FORM [i1l]-914.*?status', page_txts[0], re.IGNORECASE)
    status = match_status.group() if match_status else None
    status = re.sub('[il1]-', 'I-', status, re.IGNORECASE)

    match_order = re.search('ORDER:.*?(The.*?\.)', page_txts[-1], re.IGNORECASE)
    order = match_order.group(1).strip() if match_order else None

    match_desc = re.search('(The Applicant.*?)(\s+I\.|$)', page_txts[0], re.IGNORECASE | re.S)
    desc = match_desc.group(1).strip() if match_desc else None
    # if not desc:
    #     raise ValueError

    match_is_family = re.search('FAMILY MEMBER', page_txts[0], re.IGNORECASE)
    is_family = True if match_is_family else False

    return {
        'ID': ID,
        'decision': decision,
        'status': status,
        'order': order,
        'is_family': is_family,
        'desc': desc,
    }


def parse_pdf_info(tool='PyPDF2'):

    tool2func = {'pdfminer': parse_by_pdfminer, 'PyPDF2': parse_by_PyPDF2}

    BASE_INFO = {
        'url': None,
        'file_name': None,
        'ID': None,
        'date': None,
        'decision': None,
        'status': None,
        'order': None,
        'is_family': None,
    }
    ALL_DATA = []
    urls = pd.read_csv(INDEX_FILE).url
    for url in tqdm(urls, desc='Parse pdf file'):

        data = BASE_INFO.copy()

        fname = os.path.basename(url)
        data['file_name'] = fname
        data['url'] = url
        data['date'] = fname.split('_')[0]

        fp = os.path.join(PDF_DIR, fname)
        try:
            page_txts = tool2func[tool](fp)
            extrat_dict = extract_info(page_txts)
            data.update(extrat_dict)

            ALL_DATA.append(data)

        except:
            import traceback
            traceback.print_exc()
            print(f'{fname}failed')
            import ipdb
            ipdb.set_trace()

    pd.DataFrame(ALL_DATA).to_csv(RESULT_FILE, index=None)


if __name__ == "__main__":
    spider_url_and_download_pdf(update_index=True)
    parse_pdf_info()
