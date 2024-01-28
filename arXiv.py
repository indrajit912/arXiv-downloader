# Script for collecting data from arXiv
#
# Author: Indrajit Ghosh
#
# Date: Nov 12, 2021
#

import requests, pprint, os
from bs4 import BeautifulSoup

ARXIV = "https://arxiv.org"

ARXIV_CATEGORIES = {
    '1': {
        "category": "Operator Algebras",
        "code": "math.OA"
    },
    '2': {
        "category": "Spectral Theory",
        "code": "math.SP"
    },
    '3': {
        "category": "K-Theory and Homology",
        "code": "math.KT"
    },
    '4': {
        "category": "General Topology",
        "code": "math.GN"
    },
    '5': {
        "category": "Algebraic Geometry",
        "code": "math.AG"
    },
}


OPTIONS = {
    "n": "new",
    "r": "recent",
    "c": "current" # current month
}


def display_categories():
    
    print("\n ---> Available categories and their indices:\n")
    print("\t" + "-"*35)
    print("\t Index\t|   Category")
    print("\t" + "-"*35)
    print()
    for index, category in ARXIV_CATEGORIES.items():
        print(f"\t {index}\t|  {category['category']}\n")

    print()


def get_current_month_papers(category_index="1"):

    category = ARXIV_CATEGORIES[category_index]
    category_code = category['code']
    category_option = OPTIONS['c']

    category_url = ARXIV + "/list/" + category_code + "/" + category_option

    res = requests.get(category_url)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")
    list_of_papers = soup.find("div", id="dlpage").dl.findAll("span", class_="list-identifier")
    list_of_infos = soup.find("div", id="dlpage").dl.findAll("div", class_="meta")


    for paper, paper_info in zip(list_of_papers, list_of_infos):

        pdf_link = ARXIV + paper.findAll('a')[1]['href']
        title = paper_info.find("div", class_="list-title mathjax").get_text().strip()
        authors = paper_info.find("div", class_="list-authors").get_text().strip()
        
        print()
        print(title)
        print()
        print(authors)
        print(f"\n - Pdf link: {pdf_link}")

        print("." * 50)
        print("." * 80)
        


def get_recent_papers(category_index="1"):
    pass


def get_new_papers(category_index="1"):
    pass


def main():

    os.system("clear")

    print("\n\t\t\t\t\t\t##### ArXiv ####\n")

    display_categories()

    print("\nNOTE: Type the 'index' of the category to get papers related to that category" 
            " or (if you don't have a specific choice) simply hit <ENTER> !")

    response = input("Waiting for your response:")

    if response == '':
        os.system('clear')
        print("\nGetting your articles ....\n")
        print("."*150)
        print("."*150)
        print()
        get_current_month_papers()

    elif response not in ARXIV_CATEGORIES.keys():
        print(f"\nERROR: '{response}' is not a valid index! Try again later.")
            
    else:
        os.system('clear')
        print("\nGetting your articles ....\n")
        print("."*150)
        print("."*150)
        print()

        get_current_month_papers(response)


if __name__ == '__main__':
    main()
    