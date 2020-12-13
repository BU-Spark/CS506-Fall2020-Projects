import re
import os
import pandas as pd
import PyPDF2


def find_motion(order):
    if order:
        if 'motion' in order:
            return 'motion'
    return 'appeal'


def process_description(description):
    if description:
        return '.'.join(description.split('\n')[:20])
    return description


def process_date(date):
    if date:
        manth_dict = {
            'jan': '01', 'january': '01', 'feb': '02', 'february': '02', 'mar': '03', 'march': '03',
            'apr': '04', 'april': '04', 'may': '05', 'jun': '06', 'june': '06', 'jul': '07', 'july': '07',
            'aug': '08', 'august': '08', 'sep': '09', 'september': '09', 'sept': '09', 'oct': '10', 'october': '10',
            'nov': '11', 'november': '11', 'dec': '12', 'december': '12'
        }
        date = date.lower()
        if ',' in date:
            month_day, year = date.split(',')
            month, day = month_day.strip().split()
            month = manth_dict[month.strip('.')]
        else:
            month, day, year = date.split()
            month = manth_dict[month.strip('.')]
        return '-'.join((year.strip(), month.strip(), day.strip()))
    return date


def get_hyperlink(one_pdf_path):
    """
    function for extracting hyperlink
    one_pdf_path: path of each pdf file
    """
    key = '/Annots'
    uri = '/URI'
    ank = '/A'
    with open(one_pdf_path, mode='rb') as ori_pdf:
        pdf_document = PyPDF2.PdfFileReader(ori_pdf)
        page_num = pdf_document.numPages
        for page in range(page_num):
            page_sliced = pdf_document.getPage(page)
            page_object = page_sliced.getObject()
            if key in page_object:
                ann = page_object[key]
                for a in ann:
                    u = a.getObject()
                    if uri in u[ank]:
                        return u[ank][uri]
    return "NAN"


def parse_by_PyPDF2(one_pdf_path):
    """
    extracting texts from pdf
    one_pdf_path: path of each pdf file
    """
    with open(one_pdf_path, mode='rb') as ori_pdf:
        pdf_document = PyPDF2.PdfFileReader(ori_pdf)
        page_num = pdf_document.numPages
        page_texts = []
        for page in range(page_num):
            txt = pdf_document.getPage(page).extractText()
            page_texts.append(txt)
    return page_texts


def extract_single_pdf_info(page_texts):
    """Extract the required text information from a single pdf"""
    # step1: Extract id or Case number: extraction from first page (In Re: 9435010 information) or extraction from last page (ID# 1940904 information)
    match_ID1 = re.search('In Re: (\d+)', page_texts[0], re.IGNORECASE | re.S)
    match_ID2 = re.search('# (\d+)', page_texts[-1], re.IGNORECASE | re.S)
    if match_ID1:
        ID = match_ID1.group(1).strip()
    elif match_ID2:
        ID = match_ID2.group(1).strip()
    else:
        ID = None

    # step2: Extract date: extraction from the home page: Date: (MAY 23, 2013) or Administrative Appeals Office\n()\n the next line
    match_date1 = re.search('DA\s*TE.*?:(.*?\d{4})', page_texts[0], re.IGNORECASE)
    match_date2 = re.search('Administrative Appeals Office\n(.*?\d{4})\n', page_texts[0], re.IGNORECASE)
    match_date3 = re.search('Decision of the Board of Immigration Appeals\n(.*?\d{4})\n', page_texts[0], re.IGNORECASE)
    match_date4 = re.search('Board of Immigration Appeals\n(.*?\d{4})\n', page_texts[0], re.IGNORECASE)
    if match_date1:
        date = match_date1.group(1).strip()
    elif match_date2:
        date = match_date2.group(1).strip()
    elif match_date3:
        date = match_date3.group(1).strip()
    elif match_date4:
        date = match_date4.group(1).strip()
    else:
        date = None

    # step3: extract decision from files
    match_decision = re.search('(appeal|motion).*?decision', page_texts[0], re.IGNORECASE | re.S)
    decision = match_decision.group(1) if match_decision else None

    # step4: extract status from files
    match_status1 = re.search('FORM [i1l]-914.*?status', page_texts[0], re.IGNORECASE | re.S)
    match_status2 = re.search('APPLICATION:(.*?Status)', page_texts[0], re.IGNORECASE | re.S)
    match_status3 = re.search('PETITION:(.*?Status)', page_texts[0], re.IGNORECASE | re.S)
    if match_status1:
        status = match_status1.group().strip()
    elif match_status2:
        status = match_status2.group(1).strip()
    elif match_status3:
        status = match_status3.group(1).strip()
    else:
        status = 'application for T nonimmigrant status'

    # step5: extract order from files
    match_order1 = re.search('ORDER.*?:.*?(The.*?)\.', page_texts[-1], re.IGNORECASE | re.S)
    match_order2 = re.search('ORDER.*?:.*?(The.*?)\.', page_texts[-2], re.IGNORECASE | re.S)
    if match_order1:
        order = match_order1.group(1).strip()
    elif match_order2:
        order = match_order2.group(1).strip()
    else:
        order = None

    # step6: extract description from files
    match_desc1 = re.search('(The Applicant.*?)(\s+I\.|$)', page_texts[0], re.IGNORECASE | re.S)
    match_desc2 = re.search('(The Applicant.*?)(\s+I\.|$)', page_texts[1], re.IGNORECASE | re.S)
    match_desc3 = False
    if len(page_texts) > 3:
        match_desc3 = re.search('(The Applicant.*?)(\s+I\.|$)', page_texts[2], re.IGNORECASE | re.S)
    if match_desc1:
        desc = match_desc1.group(1).strip()
    elif match_desc2:
        desc = match_desc2.group(1).strip()
    elif match_desc3:
        desc = match_desc3.group(1).strip()
    else:
        desc = None

    # step: extract is_family from files
    match_is_family = re.search('FAMILY MEMBER', page_texts[0], re.IGNORECASE | re.S)
    is_family = True if match_is_family else False

    # step8: extract LEXIS Citation from files
    match_citation = re.search('Reporter\n(.*?)\*\n', page_texts[0], re.IGNORECASE | re.S)
    citation = match_citation.group(1).strip() if match_citation else None

    return {
        'ID': ID,
        'date': date,
        'decision': decision,
        'status': status,
        'order': order,
        'is_family': is_family,
        'desc': desc,
        'citation': citation
    }


def parse_all_pdf_info(data_file='Lexis Dataset -- Non-precedent AAO Decisions/'):
    """
    Main function for extracting information in pdf
    data_file: pdf folder, can be multiple folders
    """
    # 1. Define the variables to be extracted
    urls = []
    file_names = []
    ids = []
    dates = []
    types = []
    statuses = []
    orders = []
    is_families = []
    descriptions = []
    citations = []
    doc_files = []

    # 2. Iterate each pdf
    for root, dirs, files in os.walk(data_file):
        for filename in files:
            # Remove the pdf and hidden files of Cases. DS_Store
            if filename[:5] != 'Cases' and filename != '.DS_Store':
                file_path = root + '/' + filename
                # step0: extract file_name
                file_names.append(filename)
                doc_files.append(root)
                # step1: Extract hyperlink
                urls.append(get_hyperlink(file_path))
                # step2: Extract the other information
                page_texts = parse_by_PyPDF2(file_path)
                extract_dict = extract_single_pdf_info(page_texts)
                ids.append(extract_dict['ID'])
                dates.append(extract_dict['date'])
                types.append(extract_dict['decision'])
                statuses.append(extract_dict['status'])
                orders.append(extract_dict['order'])
                is_families.append(extract_dict['is_family'])
                descriptions.append(extract_dict['desc'])
                citations.append(extract_dict['citation'])

    # 3. Define the remaining data to be saved
    res = pd.DataFrame()
    res["url"] = urls
    res["file_name"] = file_names
    res["path"] = doc_files
    res["ID"] = ids
    res["date"] = dates
    res["type"] = types
    res["status"] = statuses
    res["order"] = orders
    res["is_family"] = is_families
    res['description'] = descriptions
    res['LEXIS Citation'] = citations

    # 4. additional processing
    # 4.1 date processing
    res["date"] = res["date"].apply(process_date)

    # 4.2 type processing
    res["type"] = res["order"].apply(find_motion)

    # 4.3 description processing
    res["description"] = res["description"].apply(process_description)

    res.to_csv("pdf_info_data.csv", encoding="utf-8")


if __name__ == "__main__":
    parse_all_pdf_info()  # Process all pdf file information
