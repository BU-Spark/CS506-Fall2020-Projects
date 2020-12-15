import pandas as pd
import tabula
import csv


def import_csv(filename):
    df = pd.read_csv(filename)
    return df


def import_pdf(filename, pages):
    tables = []
    for i in range(pages):
        table = tabula.read_pdf(filename, pages=i+1)
        tables.append(table)
    return tables


def write_csv(filename, X, header):
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for x in X:
            writer.writerow(x)