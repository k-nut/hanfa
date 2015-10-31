# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import datetime

URL = "http://www.hanfa.hr/EN/registar/2?&page=0"


def main():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text)
    nr_of_pages = get_number_of_pages(soup)
    for i in range(nr_of_pages * 1):
        url = "http://www.hanfa.hr/EN/registar/2?&page={}".format(i)
        parse_page(url)


def get_number_of_pages(soup):
    paginations = soup.find(attrs={"class": "pagination"})

    return len(paginations.findAll("a")[2:-2])


def parse_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text)

    table = soup.find(attrs={'class': "table-data"})

    links = table.findAll(attrs={"class": "expand"})
    contents = soup.findAll(attrs={'class': "switchable-content"})

    for i, link in enumerate(links):
        data = extract_details(contents[i])
        data["Name"] = link.text.strip()
        data['OID'] = link.parent.parent.findAll("span")[-2].text.replace('OIB', '').strip()
        data["source_url"] = URL
        data["sample_date"] = datetime.datetime.now().isoformat()

        print json.dumps(data)


def extract_details(part):
    columns = part.findAll(attrs={"class": "column"})
    details_1 = columns[0].findAll("li")
    details_2 = columns[1].findAll("li")

    saved = {}

    saved["Address"] = " ".join(details_1[0].text.split(" ")[1:])
    saved["Phone"] = " ".join(details_1[1].text.split(" ")[1:])
    saved["Website"] = " ".join(details_1[2].text.split(" ")[1:])
    if len(details_1) > 3:
        saved["BIC"] = details_1[3].text
    activities =  details_2[0].text.split(", ")
    saved["Approved activites"] = [get_name_for_symbol(activity) for activity in activities]
    saved["Court register"] = details_2[1].find("a")["href"]

    return saved


def get_name_for_symbol(symbol):
    # taken from the bottom of http://www.hanfa.hr/en/registar/2
    mapping = {
        '1-01': 'reception and transmission of orders in relation to one or more financial instruments',
        '1-02': 'execution of orders on behalf of clients',
        '1-03': 'dealing on own account',
        '1-04': 'portfolio management',
        '1-05': 'investment advice',
        '1-06': 'underwriting of financial instruments and/or placing of financial instruments on a firm commitment basis',
        '1-07': 'placing of financial instruments without a firm commitment basis',
        '1-08': 'operation of Multilateral Trading Facilities.',
        '2-01': 'safekeeping and administration of financial instruments for the account of clients, including custodianship and related services such as cash/collateral management',
        '2-02': 'granting credits or loans to an investor to allow him to carry out a transaction in one or more financial instruments, where the firm granting the credit or loan is involved in the transaction',
        '2-03': 'advice to undertakings on capital structure, industrial strategy and related matters and advice and services relating to mergers and the purchase of undertakings',
        '2-04': 'foreign exchange services where these are connected to the provision of investment services',
        '2-05': 'investment research and financial analysis or other forms of general recommendation relating to transactions in financial instruments',
        '2-06': 'services related to services under 1-06',
        '2-07': 'investment services and activities as well as ancillary services related to the underlying of the derivatives where these investment services and activities are connected to the provision of investment or ancillary services.',
        '3-01': 'organisation and implementation of the educational programme for capital market participants and users',
        '3-02': 'insurance representation business',
        '3-03': 'marketing of investment fund units',
        '3-04': 'offering of pension schemes',
        '3-05': 'other activities which, in Hanfa’s view, do not have any negative impact on the compliance with the Capital Market Act and relating regulations'
    }
    return mapping[symbol]


if __name__ == "__main__":
    main()
