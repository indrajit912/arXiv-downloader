# Script for collecting data from arXiv
#
# Author: Indrajit Ghosh
#
# Created On: Nov 12, 2021
# Modified On: May 20, 2024
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


def display_paper_on_terminal(title, authors, abstract_link, pdf_link, index=None):
    sp = "    "
    index = '-' if index is None else index
    arxiv_link = "arXiv:" + abstract_link.lstrip("https://arxiv.org/abs/")

    print()
    print(f"[{index}] {arxiv_link}")
    print(sp, "Title: ", title)
    print(sp, "Author(s): ", authors)
    print()
    print(sp, f" - Abstract link: {abstract_link}")
    print(sp, f" - PDF link: {pdf_link}")

    print("." * 50)
    print("." * 80)



def get_current_month_papers(category_index="1", option="c"):

    category = ARXIV_CATEGORIES[category_index]
    category_code = category['code']
    category_option = OPTIONS[option]

    category_url = ARXIV + "/list/" + category_code + "/" + category_option

    res = requests.get(category_url)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")
    articles = soup.find("div", id="dlpage").find("dl", id="articles").findAll("dt")
    list_of_infos = soup.find("div", id="dlpage").dl.findAll("div", class_="meta")

    i = 1
    for paper, paper_info in zip(articles, list_of_infos):

        links = paper.findAll('a')[1:5]
        abstract_link, pdf_link, ps_link, html_link = [ARXIV + link['href'] for link in links]
        title = paper_info.find("div", class_="list-title mathjax").get_text().lstrip("Title:").strip()
        authors = paper_info.find("div", class_="list-authors").get_text().strip()

        display_paper_on_terminal(title=title, authors=authors, abstract_link=abstract_link, pdf_link=pdf_link, index=i)

        i += 1


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
    