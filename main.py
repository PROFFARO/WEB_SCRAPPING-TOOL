import os
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv


def scrape_html_content(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def scrape_text_content(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()


def scrape_connected_pages(url, num_pages):
    texts = []
    for _ in range(num_pages):
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()
        texts.append(text)
        next_page = soup.find("a", href=True)
        if next_page:
            url = next_page["href"]
        else:
            break
    return "\n".join(texts)


def scrape_specific_tags(url, tag_name):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    tags = soup.find_all(tag_name)
    return [tag.get_text() for tag in tags]


def scrape_email_addresses(url):
    response = requests.get(url)
    response.raise_for_status()
    text = response.text
    email_pattern = r"\S+@\S+"
    emails = re.findall(email_pattern, text)
    return "\n".join(emails)


def scrape_phone_numbers(url):
    response = requests.get(url)
    response.raise_for_status()
    text = response.text
    phone_pattern = r"(\d{3}[-\.\s]??\d{4}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{4}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
    phone_numbers = re.findall(phone_pattern, text)
    return phone_numbers


def scrape_addresses(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    addresses = []

    # Find elements that contain address information
    address_elements = soup.find_all(["address", "span"], text=True)

    for element in address_elements:
        address_text = element.get_text().strip()
        addresses.append(address_text)

    return addresses


# ... (Rest of the code)
def scrape_html_content_and_store(url, folder_path):
    response = requests.get(url)
    response.raise_for_status()
    html_content = response.text

    try:
        os.mkdir(folder_path)
    except FileExistsError:
        pass

    file_path = os.path.join(folder_path, "scraped_content.html")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)


def scrape_text_and_store_as_txt(url, file_path):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text()

    # Split the text into paragraphs
    paragraphs = text.split("\n\n")

    with open(file_path, "w", encoding="utf-8") as f:
        for paragraph in paragraphs:
            f.write(paragraph + "\n\n")  # Add double newline after each paragraph


def main():
    print(
        "\t\t******************************************WEB_SCRAPPER_TOOL*****************************************\n\t\t"
        "******************************************MADE_BY_DAYANANDA*****************************************"
    )


while True:
    url = input("Enter the URL you want to Scrap: ")
    if url == "0":
        break
    option = int(
        input(
            "[$]Select an option:\n"
            "[1] Scrap only the HTML content of the URL\n"
            "[2] Scrap only the text from the URL\n"
            "[3] Scrap text from multiple connected webpages\n"
            "[4] Scrap particular tags from the URL\n"
            "[5] Scrap Email Address from the URL\n"
            "[6] Scrap Phone Number from the URL\n"
            "[7] Scrap Address from the URL\n"
            "[8] Scrap the HTML content from the URL and store in a folder\n"
            "[9] Scrap the text from the URL and store as txt\n"
            "[0] Exit.\n"
            "##################################################################\n"
            "Enter option number: \n"
            "------------------>> "
        )
    )

    if option == 1:
        html_content = scrape_html_content(url)
        print(html_content)
    elif option == 2:
        text_content = scrape_text_content(url)
        print(text_content)
    elif option == 3:
        num_pages = int(input("Enter the number of pages to scrape: "))
        multi_page_text = scrape_connected_pages(url, num_pages)
        print(multi_page_text)
    elif option == 4:
        tag_name = input("Enter the tag name to scrape (e.g., 'p', 'h1', 'a'): ")
        tags_text = scrape_specific_tags(url, tag_name)
        for text in tags_text:
            print(text)
    elif option == 5:
        emails = scrape_email_addresses(url)
        print(emails)
    elif option == 6:
        phone_numbers = scrape_phone_numbers(url)
        for phone_number in phone_numbers:
            print(phone_number)
    elif option == 7:
        addresses = scrape_addresses(url)
        for address in addresses:
            print(address)
    elif option == 8:
        folder_path = input(
            "Enter the path to the folder to store the HTML content:(e.g.: add the path without using of the double inverted comma) "
        )
        scrape_html_content_and_store(url, folder_path)
        print("HTML content saved in the folder:", folder_path)
    elif option == 9:
        txt_file_path = input("Enter the path where you want to save the text file: ")

        scrape_text_and_store_as_txt(url, txt_file_path)
        print("Scraped text has been saved to the text file.")
    elif option == 0:
        exit()
    else:
        print("Invalid option.")


if __name__ == "__main__":
    main()
