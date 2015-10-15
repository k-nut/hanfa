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
    saved["Approved activites"] = details_2[0].text.split(", ")
    saved["Court register"] = details_2[1].find("a")["href"]

    return saved

if __name__ == "__main__":
    main()
